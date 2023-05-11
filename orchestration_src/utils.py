import requests
import google.auth.transport.requests
import google.oauth2.id_token
from config import logger, LOCAL_TESTING
import glob
import yaml
from prefect import get_run_logger


def trigger_cloud_function_with_http_post(endpoint, post_body):
    """Sends an authenticated post request to another cloud function
    Note: when run locally it just prints the request body and endpoint in the logs
    """

    if LOCAL_TESTING == "LOCAL_ONLY":
        logger.info(
            f"Fake http post request with body: {post_body} to endpoint: {endpoint}"
        )
        response = {"status": 200, "detail": "local fake http invoke"}

    else:
        auth_req = google.auth.transport.requests.Request()
        id_token = google.oauth2.id_token.fetch_id_token(auth_req, endpoint)
        headers = {
            "Authorization": f"Bearer {id_token}",
            "Content-Type": "application/json",
        }
        response = requests.post(endpoint, json=post_body, headers=headers)
        logger.info(f"Cloud function triggered at:{endpoint}")

    if response.status_code != 200:
        raise Exception(
            "Triggered function encountered an error, see logs for further details"
        )

    return response


def multiple_files_yaml_loader(path_pattern):
    """Given a path pattern loads all yaml files that fit the pattern as items in a python list
    examples:
        path_pattern = "pipelines/raw_to_bronze/transforms/*.yaml"
        path_pattern = "./transforms/*.yaml"
    """

    files = glob.glob(path_pattern)

    my_list = []
    for file in files:
        with open(file) as f:
            loaded_dict = yaml.load(f, Loader=yaml.FullLoader)
            my_list.append(loaded_dict)

    return my_list

def pipeline_completion_handler(pipeline_name:str , is_completed: bool):
    """
    Receives a boolean named is_completed:
            True if the pipeline finished without errors
            False if it run with erros
    Results:
        Logs with prefect logger:
            - info: if all went well
            - error: if something went wrong
        Raises exception in case of errors

    """
    prefect_logger = get_run_logger()

    if is_completed:
        prefect_logger.info(f"| {pipeline_name} | Pipelined completed without errors")  
    else:
        prefect_logger.error(f"| {pipeline_name} | Pipelined did not complete as expected")
        raise Exception(f'Something went wrong in {pipeline_name}, all downstream pipelines did not run.')
    