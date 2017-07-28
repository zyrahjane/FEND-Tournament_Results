# FEND-Tournament_Results
Udacity Nanodegree Full Stack Project

## Objective
Built a PostgreSQL relational database scheme to store the results of a game tournament. Also provided a number of queries to efficiently report the results of the tournament and determine the winner.

## Installation
To run the Vagrant Virtual Machine will need to be insalled.

## Run
To run use the following command lines in project's directory:
1. `$ vagrant ssh`
2. `$ psql`
3. Create a database `# create database tournament`
4. Connect to database `# \c tournament`
5. Inialise schemas `# \i tournament.sql`
6. Quit psql `# \q`
7. Run Project `$ python tournament_test.py`
