#!/bin/bash

# Note to READER: Please ensure to have a ROOT access to run certain commands

function clone_source() {
    
    cd /home/$USER
    sudo mkdir -p tests
    cd tests
    sudo git clone https://github.com/arunc1985/arun-chandramouli.git
    ls /home/$USER/tests/arun-chandramouli
    sudo chown -R $USER /home/$USER/tests/
}

function install_docker_engine() {

    sudo groupadd docker
    sudo usermod -aG docker $USER

    sudo apt-get remove docker docker-engine docker.io containerd runc -y
    sudo apt-get update -y
    sudo apt-get install \
        ca-certificates \
        curl \
        gnupg \
        lsb-release  -y

    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg -y
    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    sudo apt-get update -y
    sudo apt-get install docker-ce docker-ce-cli containerd.io -y
    sudo docker run hello-world
    sudo chown -R $USER /home/$USER/tests/

}

function docker_network_create() {
    docker rm -f $(docker ps -qa)
    docker rmi -f $(docker images -qa)
    docker volume rm -f $(docker volume ls)
    docker network rm elastic
    docker network create elastic
}

function kickoff_es_kibana() {

    docker rm -f $(docker ps -qa)
    docker rmi -f $(docker images -qa)
    docker pull docker.elastic.co/elasticsearch/elasticsearch:7.16.2
    docker pull docker.elastic.co/kibana/kibana:7.16.2
    docker volume rm -f $(docker volume ls)
    docker run --rm -d --name bmies --net elastic -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.16.2
    docker run --rm -d --name bmikib --net elastic -p 5601:5601 -e "ELASTICSEARCH_HOSTS=http://bmies:9200" docker.elastic.co/kibana/kibana:7.16.2
    docker ps | grep 'bmies'
    docker ps | grep 'bmikib'
}

function build_bmi_docker() {

    sudo chown -R $USER /home/$USER/tests/
    cd /home/$USER/tests/arun-chandramouli/challenge/planA/deployments
    docker build -t bmicalc:v1.1 -f dockerfile .
}

function build_bmi_app_container() {
    sudo chown -R $USER /home/$USER/tests/
    cd /home/$USER/tests/arun-chandramouli/challenge/planA/deployments
    docker build -t bmicalc:v1.1 -f dockerfile .
}

function run_bmi_app_container() {

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
}


function app_rest_tests() {    
    sleep 10
    curl -XGET http://localhost:7777/ 
}

function cleanup() {    
    
    cd /home/$USER
    rm -rf /home/$USER/arun-chandramouli
}

function clean_install() {
    echo "Clone the Source Code..."
    clone_source
    echo "Install Docker Engine ... from https://docs.docker.com/engine/install/ubuntu/"
    install_docker_engine
    echo "Create a Docker Network for maintaining all the Containers"
    docker_network_create
    echo "Kickoff Elasticsearch & Kibana Containers"
    kickoff_es_kibana
    echo "Build BMI dockerfile..."
    build_bmi_docker
    echo "Build BMI Docker Container..."
    build_bmi_app_container
    echo "Running the Flask application with all environment variables ..."
    run_bmi_app_container
    echo "Wait for all containers to bring-up eco-system"
    echo "Run App tests to ensure Flask app works!"
    app_rest_tests
    echo "Do cleanup"
    cleanup
}
# Do a Clean Install
clean_install


