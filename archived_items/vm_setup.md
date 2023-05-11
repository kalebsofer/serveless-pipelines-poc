## Some thoughts on using Prefect on a VM for simplicity
**NOTE**: This was used when we were considering using Prefect on a VM for orchestration. For now, we decided to keep it simpler and orchestrate with a Cloud Function Gen2

- VM created in the terraform "vm_example.tf"
- **IMPORTANT:** At this first stage of POC access to the prefect UI is controlled via network, you have to create a firewall rule in the VPC that allows TCP on the instances with tag "prefect-server" on ports 80 and 4200 and with the IPs of the developers or users of the solution (if you set to the Made Tech VPN ip anyone in the made tech VPN can access it)


Installing and setting up Prefect:

- ssh into it and run:

        DEBIAN_FRONTEND=noninteractive
        sudo add-apt-repository ppa:deadsnakes/ppa -y
        sudo apt-get update -y
        sudo apt-get install python3-pip python3.8-distutils  -y

        python3.8 -m pip install pipenv
        export PATH="~/.local/bin:$PATH"

        python3.8 -m pipenv install
        pipenv run python3.8 -m pip install -U prefect
        # pipenv run python3.8 -m pip install prefect-dask
        pipenv shell


        # the ip in next command should be set to the internal ip of the VM (also works with external):
        prefect config set PREFECT_API_URL=10.154.0.4:4200/api

        prefect server start --host "0.0.0.0"

Go to your browser and open the url:
        
        http://34.142.109.18:4200 (this needs to be external IP of VM, will have change every time you stop and start a VM to the new one, unless we create and pay for a IP)
