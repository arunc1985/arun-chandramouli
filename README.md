
> 
	SETUP PROGRAM TO BRING-UP THE ECOSYSTEM
	
	* * * The entire set-up is automated, but you only need to clone and run setup.sh file * * *

	Please run the following steps in an order; (You must have ROOT Access)

		sudo rm -rf /home/$USER/arun-chandramouli
		sudo rm -rf /home/$USER/tests
		git clone https://github.com/arunc1985/arun-chandramouli.git
		sudo chown -R $USER /home/$USER/arun-chandramouli
 		ls -la
		cd arun-chandramouli
		git checkout setup
		sudo apt update -y && sudo apt install dos2unix -y && sudo dos2unix ./setup.sh && sudo chmod 777 ./setup.sh
		./setup.sh  
