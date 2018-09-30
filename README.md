# Demo User Database Service

Demonstration database service to add and list users using REST API and front end.

This Python repo includes:
 - SQLLite database and web-service
 - REST API to add and list users to the database
 - Front-end
 - REST API test cases implemented using PyTest
 - Front-end tests implemented using Behave and Selenium
 - Dockerfiles for the web service and tests
 - Docker-compose definitions to run the service or tests

## Setup

### Build docker images

Clone the repo and run from root folder:

`git clone https://github.com/rhuddie/demo-user-service.git`

`cd demo-user-service`

`docker build -t demo-server .`

`docker build -t demo-server-tests -f Dockerfile.tests .`

## Run the server

### Run the demo server

As docker image:

`docker run --name demo-server -p 5000:5000 demo-server`

or with docker-compose:

`docker-compose --file docker-compose.yml up`

and to stop and remove:

`docker-compose --file docker-compose.yml down`

Utility scripts are also provided to run the above commands:

`./build_and_run_server.sh` and `./stop_server.sh`

#### Add a new user:

Visit url with browser:

<http://127.0.0.1:5000/add-user>

#### List users

<http://127.0.0.1:5000/list-users>

#### List users using the REST API

`curl http://127.0.0.1:5000/api/list`

#### Add user using REST API

`curl http://127.0.0.1:5000/api/add --data 'username=test_username2&email=test%40email.com&dob=01%2F01%2F1970&address=test+address%2C+the+street'`

## Run the tests

### Run the demo server and tests

As docker image:

`docker run -e HEADLESS=1 -e SERVER_PORT=5001 --name demo-server-tests -p 5001:5001 demo-server-tests`

or with docker-compose:

`docker-compose --file docker-compose-tests.yml up`

and remove:

`docker-compose --file docker-compose-tests.yml down`

A utility script is also provided to run the above commands:

`./build_and_run_tests.sh`

## Development environment

Create virtualenv:

`virtualenv --python=python3.6 demo-server`

`source demo-server/bin/activate`

`sudo pip install -r requirements.txt -r requirements.tests.txt`

### Run the server

`SERVER_PORT=5000 python server/server.py`

### Run the tests

`SERVER_PORT=5000 ./tests/run_tests.sh`
