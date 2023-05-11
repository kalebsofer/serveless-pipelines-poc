## GCP Internal Forecast Solution

### TERRAFORM

Some notes on the terraform modules for this solution:
- They are all stored in the /terraform folder
- They deploy all resources needed for the solution, except:
    - the project itself (should be created manually)
    - default VPC (should be created with project by default)
    - secrets manager (should be created manually, see details on summary of resources)
- Backend: **NOTE** that the backend is being stored locally (see file backend.tf) this mean Terraform state and locks are all stored locally and saved into the github repo. **Consequence**: If one developer makes changes to the terraform modules and deploy the changes but doesnt push the state and locks files to github, any other developer will be unable to make changes until the first developer pushes the files, this happens because the other developers won't have the latest state which will keep them out of sync with the real deployment in the cloud. Ideally the backend could be moved to a bucket of its own if this is to be avoided, at present for simplicity we kept this way as very few devs are working on the solution and we can trust each other to push states right after any changes are deployed.
- Variables: at present the variables are stored in "variables.tf" but not many variables are used, later if there are more parts of the solution that need configuration we may move them there.


### SUMMARY OF TERRAFORM RESOURCES

- SECRET MANAGER
    - This has to be created manually and Sales Force token and secrets stored in it with following secret names (the ingestion function retrieves them via secret env variables
    but this retrieval depends on their names):
        - SALESFORCE_CLIENT_ID
        - SALESFORCE_CLIENT_SECRET
        - SALESFORCE_PASSWORD
        - SALESFORCE_SECURITY_TOKEN
        - SALESFORCE_USERNAME

- SERVICE ACCOUNT
    - access to secret manager
    - access to storage buckets
    - cloud functions invoker
    - cloud run invoker (to use cloud functions 2nd gen)
    - access to big query to create tables, import data, run jobs

- CLOUD FUNCTIONS 2ND GEN
    - INGESTION FUNCTION
        - Google Function with simple_salesforce package
        - Secret Manager
        - Storage

    - DUCKDB QUERY TO PARQUET FUNCTION
        - Storage
        - Duckdb
        - Big Query

    - BIGQUERY QUERY TO TABLE FUNCTION
        - Big Query

    - ORCHESTRATION FUNCTION
        - Gen2 Cloud Function to allow longer timeout (3600 seconds = 1h)
        - Receives URLs of other functions as env variables via terraform
        - Triggers other functions to respect dependency 
            -e.g. (ingestion >> conversion >> bronze_to_silver >> silver_to_gold)   

    **NOTE**: All Cloud Function Gen2 require functions-framework dependency and running them
    locally may require installing emulators to emulate a local http server and trigger, 
    for the present solution for simplicity we are not using local emulators, which means 
    local testing requires some special attention (see item TO RUN THE FUNCTIONS LOCALLY in this readme for details)

- STORAGE BUCKETS
    - Raw: as close to json received as possible - just drop PII and flatten)
    - Bronze: just convert to parquet and drop unnecessary fields
    - Silver: join tables to build logical structure that makes sense for solution
    - Gold: source feed for BI dashboards
    - Function codebase: Stores the zips of all cloud functions for deployment via terraform
    - Prefect logs: stores prefect.db sqlite database after each time the orchestration function is run

- WAREHOUSE
    - Big Query   

- REPORTING
    - Looker studio (links to Big Query)

### Connecting to Salesforce
To establish a connection with Salesforce we must setup a Connected App. We currently have this supported in our dev environment which points to our SF sandbox (called forecast_supply_demand), however we will need to do the same in production once our service account has access. The following steps outline how to create a Connected App: 
1. From the Salesforce UI, head to Setup and click Create | Apps, and click New to start defining a connected app.
2. Enter the name of your application.
3. Enter the contact email information and other details.
4. Select Enable OAuth Settings.
5. Add "Full access" to selected auth scopes.
6. Save

**Once created the consumer_key and consumer_secret will be displayed temporarily, make sure to note them down and add to Google Secrets Manager**

[For more detail visit here]('https://help.salesforce.com/s/articleView?id=sf.connected_app_create_basics.htm&type=5')


### LOCAL DEV: 

**Prerequisites**

To run this solution you will need:
- Terraform installed on your local machine.
- Google Cloud SDK installed on your local machine (https://cloud.google.com/sdk/docs/install)
- a Google Cloud Platform project set up and attached to a billing account. Make sure the Cloud Functions API is Enabled.

**Get your local dev ready to run the functions**

At present the functions are not completely adapted to run locally, you can run most of them locally with effects on the cloud, but remember that this means files will be created and changed in your GCP project in the cloud. To avoid issues we suggest running your dev using a different and separate GCP project.

Configs, env variables and terraform variables all need to be checked before deploying and before running, we remind you of the following files:
- .env
- terraform/variables.tf
- orchestration_src/config.py
- ingestion_src/config.py
- duckdb_query_to_parquet_src/config.py
- bigquery_query_to_table_src/config.py

**Before running locally you will also need:**

1) to install the following dependencies in your local python environment

        python3 -m pip install google-cloud-storage simple_salesforce duckdb \
        functions-framework google-cloud-bigquery requests google \
        google-api-python-client google-auth google-auth-httplib2 google-auth-oauthlib §
        prefect PyYAML

2) to deploy the terraform module to a project. To do that you will need the appropriate IAM roles, we suggest the following roles:
- BigQuery Data Owner
- Cloud Functions Admin
- Cloud Run Invoker
- Editor
- Project IAM Admin
- Source Repository Administrator

and you will need to authenticate with gcloud:

        gcloud auth application-default login


**Before deploying or running any code locally**

Remember to make sure that config values reflect your GCP project and any general setup:
- .env
- terraform/variables.tf
- orchestration_src/config.py
- ingestion_src/config.py
- duckdb_query_to_parquet_src/config.py
- bigquery_query_to_table_src/config.py

### TO DEPLOY ON THE CLOUD:

Make sure your ENV variable GOOGLE_APPLICATION_CREDENTIALS is empty, otherwise it will try to deploy resources using service account instead of using your **gcloud auth application-default login** authentication:

    export GOOGLE_APPLICATION_CREDENTIALS=''

Go to terraform folder:

    cd terraform

Init terraform:

    terraform init

Planning, deploying or destroying terraform:

    terraform plan
    terraform apply
    terraform destroy


### TO RUN THE FUNCTIONS LOCALLY

An example of how to run the functions locally without using emulators is given in each function in the respective **test_main.py** file. This is made basically by having 2 entry points, one for the cloud (that needs a special GCP decorator) and one for the local function (without the decorator). But some notes are worth mentioning:

The functions: **ingestion, duckdb_query_to_parquet and bigquery_query_to_parquet** can be run locally but they need to have a project and all resources in your GCP cloud, as well as the configs pointing to them, which means they can run locally but when this is done they still send results and effects of their activity to the respective cloud buckets and big query datasets. When running them in this manner remember to confirm that your local .env variable LOCAL_TESTING is set to "LOCAL_WITH_CLOUD_EFFECTS" and that you are ok with the changes that they will generate in your cloud (e.g. don't run dev/test work pointing at the wrong project in the cloud)


The function **orchestration** can be run in two modes:
- **LOCAL_ONLY** instead of triggering the other cloud functions it will just print in the logs a string that says *"Fake http post request with body: {post_body} to endpoint: {endpoint}"*. If you want to run it in this mode remember to change the .env variable LOCAL_TESTING to "LOCAL_ONLY"
- **LOCAL_WITH_CLOUD_EFFECTS** this will run locally but triggering the other functions that it orchestrates in the cloud. To do so you will need to take 2 steps:
    - create an access key for the service account and point the env variable GOOGLE_APPLICATION_CREDENTIALS to it (see more details on orchestration_src/local_dev.env)
    - set the LOCAL_TESTING is set to "LOCAL_WITH_CLOUD_EFFECTS"
    - after you finish running the function in this mode you may want to set GOOGLE_APPLICATION_CREDENTIALS='' again otherwise your terraform commands will not work.
