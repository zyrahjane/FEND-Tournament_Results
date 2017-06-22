# FEND-Tournament_Results
Udacity Nanodegree, Full Stack Project

To run Vagrant Virtual Machine will need to be insalled.

The following are key files:
tournament.sql  - this file is used to set up your database schema (the table representation of your data structure).
tournament.py - this file is used to provide access to your database via a library of functions which can add, delete or query data in your database to another python program (a client program). Remember that when you define a function, it does not execute, it simply means the function is defined to run a specific set of instructions when called.
tournament_test.py - this is a client program which will use your functions written in the tournament.py module. 

In correct directory run the following:

$vagrant ssh


$psql

---to create a database


vagrant=> create database tournament;

---to inialise schemas


tournament=> \i tournament.sql

---to quit psql


\q

---to run test


python tournament_test.py

