-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS players;

CREATE TABLE players ( name TEXT,
                     id SERIAL,
                     PRIMARY KEY(id));


CREATE TABLE matches (winner INT
                     REFERENCES players,
                     loser INT
                     REFERENCES players);
