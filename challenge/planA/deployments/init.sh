#!/bin/bash

# Note to READER: Please ensure to have a ROOT access to run certain commands

function init_setup() {
    
	sudo git clone https://github.com/arunc1985/arun-chandramouli.git
	sudo chown -R $USER /home/$USER/arun-chandramouli
	ls -la
	cd arun-chandramouli
	git checkout setup
	sudo apt update -y && sudo apt install dos2unix -y && sudo dos2unix ./setup.sh && sudo chmod 777 ./setup.sh
	./setup.sh  
}


init_setup