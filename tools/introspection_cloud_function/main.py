import functions_framework
import time
from prefect import task, flow
from os import listdir
from pathlib import Path
import command 
import prefect
import subprocess, sys

@functions_framework.http
def hello_http(request):
    
    request_json = request.get_json(silent=True)

    my_dir = request_json['my_dir']
    expression = request_json['expression']

    my_flow()

    print(f'prefect settings: {prefect.context.GLOBAL_SETTINGS_CONTEXT}')    
    
    listed_dir = listdir(my_dir)

    results = []
    for path in Path(my_dir).rglob(expression):
        print(path)
        results.append(path.name)

    pip_freeze_versions = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
    
    print(pip_freeze_versions)

    return {"status":200, "listed_dir":listed_dir, "results":results}

@task
def print_values(values):
    for value in values:
        time.sleep(0.5)
        print(value, end="\r")

@flow
def my_flow():
    print_values.submit(["AAAA"] * 3)
    print_values.submit(["BBBB"] * 1)
