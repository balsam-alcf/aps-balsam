import argparse
from yaml import load as _yaml_load
try: from yaml import CLoader as Loader
except ImportError: from yaml import Loader
from pprint import pprint
import sys
from jinja2 import Template, Environment, FileSystemLoader

def yaml_load(s):
    return _yaml_load(s, Loader=Loader)

def parse(path):
    with open(path) as fp:
        raw_text = fp.read()
    dat = yaml_load(raw_text)
    placeholders = dat.get('PLACEHOLDERS', [])
    
    parser = argparse.ArgumentParser()
    first_letters = []
    for key in placeholders:
        first_letter = key[0]
        if first_letter not in first_letters:
            first_letters.append(first_letter)
            parser.add_argument('-'+first_letter, '--'+key, required=True)
    namespace, extra = parser.parse_known_args()
    template = Template(raw_text)
    result = template.render(vars(namespace))
    return yaml_load(result)

if __name__ == "__main__":
    pprint(parse(sys.argv[1]))
