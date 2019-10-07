# Osprey test
        

### Prerequisites
    install https://docs.docker.com/docker-for-mac/install/
    install docker-compose https://docs.docker.com/compose/install/

### Installation steps
    checkout the source code
    > git clone repo
    > cd /path/to/your/install/ospreytest
    > docker-compose build
    > docker-compose up
    > init cameras data 
    docker exec -it ospreytest_statisticapi_1 python -c 'from tests.utils.db import init_db; init_db()'
    > open browser http://localhost:8081/statistic

## Working on the project

### project location
    The code accessed by all the docker servers/instances is in the folder
    /path/to/your/install/ospreytest

### bring up the docker work environment
    start docker and set docker-machine environment variables
    > cd /path/to/your/install/ospreytest/
    > docker-compose up

## Adding project requirements

### add new packages to container
    when adding new requirements to the requirements.txt a new image must be
    built in order to persist the changes across container restarts

    go inside the container
    > docker exec -i -t ospreytest_statisticapi_1 bash

    to update requirements.txt
    > pip install --upgrade --force-reinstall -r requirements.txt

    to insall a new package
    > pip install some-packege-name

    to freeze changes
    > pip freeze > requirements.txt
    
## Run tests
   We test some cases for this project
   - timeout error skipping
   - ability to work with about 5m images dataset
   - statistic data calculation
   
   We create image service to imitate image storage. 
   We use MongoDB as storage.
   We store camera config like (timeout value, timeout error imitation, etc) 
   in the same collection only for simplifying the tests.
   
   
### bring up the docker work environment
    start docker and set docker-machine environment variables
    > cd /path/to/your/install/ospreytest/
    > docker-compose up

### run tests
   docker exec -it ospreytest_statisticapi_1 pytest -vv
   





