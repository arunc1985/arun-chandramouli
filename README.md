
-------------
REQUIREMENTS
-------------

Given the following JSON data
>

    [{"Gender": "Male", "HeightCm": 171, "WeightKg": 96 },
    { "Gender": "Male", "HeightCm": 161, "WeightKg": 85 },
    { "Gender": "Male", "HeightCm": 180, "WeightKg": 77 },
    { "Gender": "Female", "HeightCm": 166, "WeightKg": 62},
    {"Gender": "Female", "HeightCm": 150, "WeightKg": 70},
    {"Gender": "Female", "HeightCm": 167, "WeightKg": 82}]
    
    as the input with weight and height parameters of a person, we have to perform
    the following:
        
        1) Calculate the BMI (Body Mass Index) using Formula 1, BMI Category and Health risk from Table 1 of the person 
        and add them as 3 new columns.
        2) Count the total number of overweight people using ranges in the column BMI
        Category of Table 1, check this is consistent programmatically and add any other observations in the documentation.
        3) Create build, tests to make sure the code is working as expected and this can be added to an 
        automation build / testing / deployment pipeline.

----------
USE-CASES
----------

>
    - Ability of the System to take user-inputs via a *json* file
    - Ability of the System to parse the *json* file and load records in-memory
    - Ability of the System to parse each record, refer to BMI Table and add details such as;
        - BMI Category
        - Health Risk
    - Ability of the System to store modified records into an Elastic-search index
    - Ability of the System to parse the calculated index and store all overweight people into new index
    - Ability of the System to be deployed as Containers/PODS
    - Ability of the System to process millions of records in an optimized manner

------------------------------
FORMULAS FOR BMI CALCULATIONS
------------------------------
>
    BMI(kg/m2) = mass(kg) / height(m)2

-------------------------
BMI CALCULATIONS EXAMPLE
-------------------------
>

    The BMI (Body Mass Index) in (kg/m2) is equal to the weight in kilograms (kg)
    divided by your height in meters squared (m)2. 
    For example, if you are 175cm (1.75m) in height and 75kg in weight, 
        - you can calculate your BMI as follows: 
            - 75kg/ (1.75m²) = 24.49kg/m²

-----------------------------------
BMI TABLE - CATEGORY - HEALTH RISK
-----------------------------------
>
    BMI-Category    BMI-Range(kg/m2)    Health-risk
    ------------    ----------------    ------------

    Underweight    | 18.4 and below   |   Malnutrition risk
    Normal weight  | 18.5 - 24.9      |   Low risk
    Overweight     | 25 - 29.9        |   Enhanced risk
    Moderately-obese | 30 - 34.9      |   Medium risk
    Severely-obese  | 35 - 39.9       |   High risk
    Very-severely-obese | 40 & above  |   Very high risk

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

-----------------
TECHNOLOGY STACK
-----------------
>
    Programming - Python3
    Database - Elasticsearch (Can store several millions of records, search is optimized)
    Reports - Kibana
    Deployments - Dockers & K8s
    Unit-Testing - Pytests
    Code Repository - Github
    Docker Registry - docker.io

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

----------
ALGORITHM
----------
>
    ~ Run the solution as a Docker Image.
    ~ Read the contents of the *json* file input into memory.
    ~ Flush the following indexes before execution - (bmi-modified,bmi-results) .
    ~ Store the contents of the *json* file into in-memory for faster operations.
    ~ For each record in the json
        ~   Calculate the BMI (Body Mass Index) using Formula 1.
        ~   Refer BMI Category and Health risk from Table 1 of the person and add them as 3 new columns to the same record.
    ~ Push the modified records to a separate index (bmi-modified).
    ~   Count the total number of overweight people using ranges in the column BMI
        Category of Table 1 and push to a separate index (bmi-results).

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

-------------------------
CLONING THE SOURCE-CODE
-------------------------
>
    echo "Clone the Source Code..."
    cd /home/$USER
    sudo rm -rf /home/$USER/tests/
    sudo mkdir tests
    cd tests
    sudo git clone https://github.com/arunc1985/arun-chandramouli.git
    ls /home/$USER/tests/arun-chandramouli

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

-------------------------------------------------
EXECUTION STEPS - ENVIRONMENT BRINGUP AUTOMATED
-------------------------------------------------

>
    Please run the shell file to kickoff automated environment bring-up
    ls /home/$USER/tests/arun-chandramouli
    cd /home/intucell/tests/arun-chandramouli/challenge/planA/deployments
    sudo chmod 777 ./setup.sh
    ./setup.sh


* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

-----------------------------------------------
EXECUTION STEPS - ENVIRONMENT BRINGUP MANUALLY
-----------------------------------------------

>
    Please run the following commands in an ORDER to bring-up Environment

    ----------------
    MANUAL EXECUTION
    ----------------

    echo "Install Docker Engine ... from https://docs.docker.com/engine/install/ubuntu/"

    sudo groupadd docker
    sudo usermod -aG docker $USER

    sudo apt-get remove docker docker-engine docker.io containerd runc -y
    sudo apt-get update -y
    sudo apt-get install \
        ca-certificates \
        curl \
        gnupg \
        lsb-release
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    sudo apt-get update -y
    sudo apt-get install docker-ce docker-ce-cli containerd.io -y
    sudo docker run hello-world


    echo "Create a Docker Network for maintaining all the Containers"
    docker network rm elastic
    docker network create elastic
    docker pull docker.elastic.co/elasticsearch/elasticsearch:7.16.2
    docker pull docker.elastic.co/kibana/kibana:7.16.2

    echo "Kickoff Elasticsearch & Kibana Containers"
    docker rm -f $(docker ps -qa)
    docker rmi -f $(docker images -qa)
    docker volume rm -f $(docker volume ls)

    docker run --rm -d --name bmies --net elastic -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.16.2
    docker run --rm -d --name bmikib --net elastic -p 5601:5601 -e "ELASTICSEARCH_HOSTS=http://bmies:9200" docker.elastic.co/kibana/kibana:7.16.2
    docker ps | grep 'bmies'
    docker ps | grep 'bmikib'

    echo "Build the Dockerfile for processing the application ..."

    cd /home/$USER/tests/arun-chandramouli/challenge/planA/deployments
    docker build -t bmicalc:v1.1 -f dockerfile .

    echo "Running the Flask application with all environment variables ..."
    docker rm -f bmicalcapp
    docker run -d --rm --name bmicalcapp \
        --net elastic \
        -v /home/$USER/tests/arun-chandramouli/challenge/planA/:/tmp/bmi/ \
        -e bmiCatJsonFile="/tmp/bmi/files/bmicategory/bmi_cat.json" \
        -e bmiUsersJsonFilePath="/tmp/bmi/files/bmisamples" \
        -e esHost="bmies" \
        -e esPort="9200" \
        -e esIndex="bmi" \
        -e FLASKHOSTNAME="0.0.0.0" \
        -e FLASKPORT="7777" \
        -p 7777:7777 \
        bmicalc:v1.1 \
        python /tmp/bmi/source/main/driver.py

    docker ps | grep 'bmicalcapp'


    sudo chown -R $USER /home/$USER/tests/

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

-----------------------------------------
EXECUTION STEPS - RUN APP TO GET RESULTS
-----------------------------------------

> 
    echo "Run the CURL Commands for Publishing and Filtering BMI Records ...""
    
        > curl -XGET http://localhost:7777/  # Tests-Hello World
    
    echo "Run the below POST call to send records to Elasticsearch ... "
        > curl -XPOST http://localhost:7777/api/v1.1/bmi/publish/ # Publish records to elasticsearch server(millions of records)

    echo "Run the below GET call to fetch records from Elasticsearch ... "
        
        Example 1 : Find all OverWeight people
        > curl -XGET http://localhost:7777/api/v1.1/bmi/filter/ -d 'esQuery={"query": {"match": {"bmi.cat":"OverWeight"}}}'

        Example 2 : Find all NormalWeight people
        > curl -XGET http://localhost:7777/api/v1.1/bmi/filter/ -d 'esQuery={"query": {"match": {"bmi.cat":"NormalWeight"}}}'
        
        Example 3 : Find all ModerateObese people
        > curl -XGET http://localhost:7777/api/v1.1/bmi/filter/ -d 'esQuery={"query": {"match": {"bmi.cat":"ModerateObese"}}}' 

        Example 4 : Find all UnderWeight people
        > curl -XGET http://localhost:7777/api/v1.1/bmi/filter/ -d 'esQuery={"query": {"match": {"bmi.cat":"UnderWeight"}}}' 

        Example 5 : Find all SevereObese people
        > curl -XGET http://localhost:7777/api/v1.1/bmi/filter/ -d 'esQuery={"query": {"match": {"bmi.cat":"SevereObese"}}}' 

        Example 6 : Find all VerySevereObese people
        > curl -XGET http://localhost:7777/api/v1.1/bmi/filter/ -d 'esQuery={"query": {"match": {"bmi.cat":"VerySevereObese"}}}' 

        Note : If you want to filter based on more fields, login to Kibana and refer to index named 'bmi'

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *                      