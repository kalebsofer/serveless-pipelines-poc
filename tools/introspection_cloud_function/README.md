# Introspection cloud function

This function is was written to run a list dir and a search of a pattern in that dir all inside the Cloud Function environment.

It receives a post request similar to the one below (the URL can change at each deployment):

    curl -m 70 -X POST <YOUR_FUNCTION_TRIGGER_URL_HERE> \
    -H "Authorization: bearer $(gcloud auth print-identity-token)" \
    -H "Content-Type: application/json" \
    -d '{
        "my_dir": "/",
        "expression":"*prefect.db"
    }'

The function returns something similar to:

    {
        "listed_dir":["var","bin","boot","cnb","config","dev","etc","home","layers","lib","lib32","lib64","libx32","media","mnt","opt","proc","root","run","sbin","serve","srv","start","sys","tmp","usr","workspace","www-data-home"],
        
        "results":["prefect.db"],
        
        "status":200
    }
         
Where:
- listed_dir is the result of ls for the directory sent in my_dir
- results is a list with the names of the files found in that directory that match the pattern sent on "expression".

This function also prints the following in the logs:
- the whole path of the files found in the function logs
- the entire prefect context config "prefect.context.GLOBAL_SETTINGS_CONTEXT"
- the results of pip freeze command to allow to see all versions of python packages running in the cloud function env

# IMPORTANT:

- When looking for prefect.db inside the cloud function environment one has to have run a prefect flow to force its automatic creation using the defaults of that environment. For this reason we also added a very simple task and flow that are called before anything else is done.

# NOTES:

- In older versions of 2nd gen cloud functions the .prefect folder with its database was being created at:

        /www-data-home/.prefect/prefect.db

- Newer versions are now more consistent with Cloud Functions in the sense that all is written in /tmp, so the db is in:

        /tmp/.prefect/prefect.db

# Deployment

- We did not write a tf module to deploy this function, the code in main.py and the requirements in requirements.txt were manually pasted into the deployment via Google Cloud's web UI. 
- We suggest deploying with a 2GB ram to avoid any memory issues if the pattern and dir you are searching on have a considerable amount of files.