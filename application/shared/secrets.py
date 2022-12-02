"""
Secrets for the application.
"""
from pathlib import Path
from json import loads


ROOT_DIR = Path(__file__).resolve().parent.parent.parent

secrets = dict()

# Reading secret files
with open(f'{ROOT_DIR}/secrets.json', 'r') as file:
    secrets = loads(file.read())

if secrets['dev_server']:
    print('Running on development server')
    secrets = secrets['dev_params']
else:
    print('Running on production server')
    secrets = secrets['prod_params']