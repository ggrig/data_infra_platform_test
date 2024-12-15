# "Building a data infrastructure optimization platform" job interview test

## Setting up the virtual environment

### Linux/Mac

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Windows

```
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### Verify the virtual environment is set

Run

```
pip list
```

At a minimum the following Python Packages are to be listed:

```
Package            Version
------------------ -----------
certifi            2024.12.14
charset-normalizer 3.4.0
geopandas          1.0.1
idna               3.10
networkx           3.4.2
numpy              2.2.0
osmnx              2.0.0
packaging          24.2
pandas             2.2.3
pip                24.3.1
pyogrio            0.10.0
pyproj             3.7.0
python-dateutil    2.9.0.post0
pytz               2024.2
requests           2.32.3
shapely            2.0.6
six                1.17.0
tzdata             2024.2
urllib3            2.2.3
```

### Running the docker image locally

Build/Rebuild the docker image

```
docker-compose build
```

Run the container

```
docker-compose up -d
```

Stop the container

```
docker-compose down
```

The container logs can be followed in the `logs/download-permits.log` file.

## The AWS CDK Python project

This builds and deploys the necessary AWS ECS infrastructure including:

- ECS task container images
- ECS Clusters 
- CloudWatch log groups & log lifecycle
- CloudWatch notifications & alarms 

The `cdk.json` file tells the CDK Toolkit how to execute your app.

To synthesize the CloudFormation template for this code:

```
$ cdk synth
```

### Useful commands

 * `cdk ls`          lists all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compares the deployed stack with the current state
 * `cdk docs`        open CDK documentation

## Environment Variables (Settings)

The environment variables for both local docker containers and ECS tasks are defined with the `.env` files in [congig_files](./congig_files)
Currently defined env variables:
`IDENTITY` - the particular crawler JSON identifier
`STORAGE_TYPE` - the crawler storage type (S3, PostgreSQL, etc.)
`BASE_URL` - the scraped website base URL 
`CRALWER_NAME` - the name of the Python module that implements the particular crawler 
`http_proxy` - HTTP proxy address docker container setting  
`https_proxy` - HTTPS proxy address docker container setting
