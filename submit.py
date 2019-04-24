import argparse
import getpass
import json
import time
import subprocess
import os
import pexpect

def connect(thetahost, thetaport):
    uname = getpass.getuser()
    ps_check = subprocess.run(
         f'ps aux | grep {uname} | grep "ssh -f -N -L {thetaport}" | grep -v grep',
         stdout=subprocess.PIPE,
         stderr=subprocess.STDOUT,
         shell=True,
         encoding="utf-8",
    )
    if thetahost in ps_check.stdout:
        print("Detected already-running SSH tunnel:\n", ps_check.stdout.strip())
        return

    print("Please authenticate to Theta.")
    X = getpass.getpass('Password: ')
    cmd = f"ssh -f -N -L {thetaport}:localhost:{thetaport} {uname}@{thetahost}.alcf.anl.gov"
    tunnel = pexpect.spawn(cmd)
    tunnel.expect('Password:')
    time.sleep(0.1)
    tunnel.sendline(X)
    time.sleep(0.1)
    return tunnel

parser = argparse.ArgumentParser()
parser.add_argument('--db', required=True, help="path to directory containing server-info")
parser.add_argument('--images', required=True, action='append')
args = parser.parse_args()

# load db/server-info
assert os.path.isdir(args.db)
info_path = os.path.join(args.db, 'server-info')
assert os.path.isfile(info_path)
with open(info_path) as fp: info = json.load(fp)

# modify host; export BALSAM_DB_PATH
thetaport = info["port"]
thetahost = info.get("thetahost", info["host"])
info["thetahost"] = thetahost
info["host"] = "localhost"
with open(info_path, 'w') as fp: fp.write(json.dumps(info))
os.environ['BALSAM_DB_PATH'] = os.path.abspath(args.db)

# create SSH background tunnel
tunnel = connect(thetahost, thetaport)

print("Running App sanity check...")
# sanity check balsam ls apps
from balsam.core.models import ApplicationDefinition as App
required_apps = ["find_rst", "register", "align"]
found_apps = []
for app in App.objects.all():
    print(app)
    found_apps.append(app.name)
assert all(app in found_apps for app in required_apps)
print(f"Got all required apps ({required_apps}): OK!")

# create DAG for each images/ folder on commandline

# ssh: submit-launch command
