------------------------------------
Project 2	- Tournament Results
Author 		- Ho Chia Leung
Completion Date	- 25 August 2015
------------------------------------

Required:
1. Vagrant (url - https://www.vagrantup.com/ )
2. Virtualbox (url - https://www.virtualbox.org/wiki/Downloads )

Files contained in this project:
1. .vagrant
2. catalog
3. pg_config.sh
4. Read Me.md
5. Vagranfile

Instruction:
1. Make sure you have the required software (Vagrant and VirtualBox) installed. The download links can be found in the Required section.

2. Open Command Prompt as Administrator

3. Change directory to the project directory (root of vagrant folder)
	Type in command prompt:
		- cd <project directory>\vagrant

4. Type command : vagrant up
-If this is the first time you run this command, it takes awhile for the required files to be downloaded. Make sure you have stable internet connection.

5. Type command : vagrant ssh
- This command is to login to the virtual machine.

6. Type command : cd /vagrant/catalog
- To change directory to catalog folder.
- Catalog folder consists these files :
	- static (contains the required CSS stylesheet and upload folder)
	- templates (contains all the HTML templates)
	- applcation.py (Main script)
	- client_secrets.json (client_secret file to connect to google api)
	- database_service.py (contains all the method for database transaction)
	- database_setup.py (to setup database)
	- fb_client_secrets.json (client_secret file to connect to facebook api)

7. Type command : python database_setup.py
- To create database

8. Type command : python application.py
- To start running the server, hosting the website

9. Go to your browser, browse : http://localhost:8000/ 






