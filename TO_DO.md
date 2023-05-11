### TODO 

# MUST
- IMPROV: Add specific versions to all dependencies used in the Cloud Functions requirements.txt to avoid new versions breaking the solution, use versions we have on local machines and test that all still works in the cloud after that
- DEVOPS: Plan and implement how we will manage 2 environments   
- Test new Sales Force credentials.
- Document solution
    - document the transformations
- Connect dashboard to live tables
- Give Viewer access to dashboard to testing users
- Give Editor access to dashboard to Data team maintainers

# SHOULD
- FIX: Times of some logs are showing one hour earlier than London time, check and fix if possible
- Plan Production setup with CircleCI, maybe 2 GCP projects (DEV/PROD) and a friendly way to run local exploration if needed
- Write tests for parts of the code that are not just use of package functionality

# MAYBE
- Tooling: think of what to do about prefect UI container as a folder
- Think of possible integration test
- Think of data validation test

# NOT NOW
- Tooling: create local script that mount historic tables in BQ
- Write up plan to scale up solution with always-on prefect as a VM or signup to prefect cloud free tier and setup orchestration function to send logs to the chosen server (cloud or vm)
