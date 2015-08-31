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
3. forum
4. tournament
5. pg_config.sh
6. Read Me.txt
7. Vagranfile

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

6. Type command : cd /vagrant/tournament
- To change directory to tournament folder.
- Tournament folder consists of 3 files :
	- tournament.py (Functions to get, update and delete records in database)
	- tournament.sql (Database schema, to create tables, views and functions)
	- tournament_test.py (Script to check tournament.py)

7. Type command : psql
- To login to Postgre Database

8. Type command: \i tournament.sql
- To import the script - tournament.sql into the database to create the database schema (tables, views and functions).
- Skip this setp if the database schema is already created.
- Execute some query to test if the schema is created correctly. Eg: Query select * from tournament_players; should return result with 0 rows (currently no player is registered)

9. Press "CTRL+D"
- To exit psql

10. Type command: python tournament_test.py
- To run the Python script tournament_test.py.
- The result should be as follow :
Match records deleted!
1. Old matches can be deleted.
Match records deleted!
Player records deleted!
2. Player records can be deleted.
Match records deleted!
Player records deleted!
3. After deleting, countPlayers() returns zero.
Match records deleted!
Player records deleted!
Player Chandra Nalaar has joined the tournament!
4. After registering a player, countPlayers() returns 1.
Match records deleted!
Player records deleted!
Player Markov Chaney has joined the tournament!
Player Joe Malik has joined the tournament!
Player Mao Tsu-hsi has joined the tournament!
Player Atlanta Hope has joined the tournament!
Player records deleted!
5. Players can be registered and deleted.
Match records deleted!
Player records deleted!
Player Melpomene Murray has joined the tournament!
Player Randy Schwartz has joined the tournament!
6. Newly registered players appear in the standings with no matches.
Match records deleted!
Player records deleted!
Player Bruno Walton has joined the tournament!
Player Boots O'Neal has joined the tournament!
Player Cathy Burton has joined the tournament!
Player Diane Grant has joined the tournament!
7. After a match, players have updated standings.
Match records deleted!
Player records deleted!
Player Twilight Sparkle has joined the tournament!
Player Fluttershy has joined the tournament!
Player Applejack has joined the tournament!
Player Pinkie Pie has joined the tournament!
8. After one match, players with one win are paired.
Success!  All tests pass!






