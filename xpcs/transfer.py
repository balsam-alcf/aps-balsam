import subprocess
import os
def transfer(src_endp, dest_endp, transfer_paths):
    cmd = f'globus transfer {src_endp} {dest_endp} --batch'
    stdin = '\n'.join(f'{src} {dest}' for src,dest in transfer_paths)

    print("Starting Globus Transfer...")

    env = os.environ.copy()
    env['LC_ALL'] = 'C.UTF-8'
    env['LANG'] = 'C.UTF-8'
    p = subprocess.run(
        args = cmd.split(),
        shell = False,
        input = stdin,
        encoding = 'utf-8',
        stdout = subprocess.PIPE,
        stderr = subprocess.STDOUT,
        env=env,
    )
    if p.returncode != 0:
        raise RuntimeError(
            f'''Globus transfer nonzero return: {p.returncode}
            Cmd: {cmd}
            Stdin:\n {stdin}
            Stdout/Stderr:\n {p.stdout}
            '''
        )

    task_id = None
    for line in p.stdout.split('\n'):
        if line.strip().startswith('Task ID'):
            task_id = line.split()[-1]
            break

    if task_id is None:
        raise RuntimeError(
            f'''Could not parse transfer Task ID from stdout:
            {p.stdout}
            '''
        )

    print(f"Transfer initiated OK (Task ID {task_id})")
    print("Waiting on task completion now...")
    p = subprocess.run(
        f'globus task wait {task_id}'.split(),
        shell = False,
        check = True
    )
    if p.returncode == 0:
        print("Transfer success!")
    else:
        raise RuntimeError("Transfer Task Wait returned", p.returncode)
