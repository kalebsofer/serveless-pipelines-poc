# Setup 

Make sure your terminal is in the folder of this tool (the folder where you find the present readme file)

Build the image:

    docker build -t local_explorer_img .

To create and run the local_explorer container:

    docker run -it --name local_explorer_cont -p 4200:4200 -v `pwd`/shared_home/.prefect:/root/.prefect/ -v `pwd`/sharing_area:/local_explorer/sharing_area local_explorer_img

# Get the prefect logs

- Download the prefect.db file from your GCP bucket.
- If your downloaded file name has any additional prefix, rename it to exactly "prefect.db"
- Copy the downloaded file to the folder of this project "shared_home/.prefect/" overwriting it if it already exists

# Start the UI

Make sure you have the container running. If you don't have it running use:

    docker start -ai local_explorer_cont

Inside the docker container, make sure you are in the **local_explorer** folder and activate the virtual env shell:

    cd /local_explorer
    pipenv shell

To start the prefect server use:

    prefect server start --host "0.0.0.0"

In your browser go to:

    http://127.0.0.1:4200/
    

# Useful snippets

To re-use a container you created before:

    docker start -ai local_explorer_cont

To open a second terminal of same container:

    docker exec -it local_explorer_cont bash
