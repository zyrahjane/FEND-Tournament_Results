#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect(database_name):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        c = db.cursor()
        return db, c
    except psycopg2.Error as e:
        print "Unable to connect to database"
        # THEN perhaps exit the program
        sys.exit(1) # The easier method
        # OR perhaps throw an error
        raise e
        # If you choose to raise an exception,
        # It will need to be caught by the whoever called this function


def deleteMatches():
    """Remove all the match records from the database."""
    DB, c = connect("tournament")
    c.execute("TRUNCATE matches")
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB, c = connect("tournament")
    c.execute("TRUNCATE matches, players")
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB, c = connect("tournament")
    c.execute("SELECT count(*) from players")
    count = int(c.fetchone()[0])
    DB.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB, c = connect("tournament")
    c.execute("INSERT INTO players (name) VALUES (%s)", (bleach.clean(name),))
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB, c = connect("tournament")
    c.execute(
        '''select a.id, a.name, wins, losses+wins as num_matches from
        (select name, id, count(loser) as losses from players left join
        matches on players.id = matches.loser group by name, id) a inner join
        (select name, id, count(winner) as wins from players
        left join matches on players.id = matches.winner group by name, id) b
        on a.id=b.id order by wins desc;
        '''
    )
    standings = c.fetchall()
    DB.close()
    ids, names, wins, num_matches = zip(*standings)
    ids = map(int, ids)
    names = map(str, names)
    wins = map(int, wins)
    num_matches = map(int, num_matches)
    return zip(ids, names, wins, num_matches)


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB, c = connect("tournament")
    c.execute("INSERT INTO matches (winner, loser) VALUES (%s, %s)",
              (bleach.clean(winner), bleach.clean(loser),))
    DB.commit()
    DB.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    DB, c = connect("tournament")
    c.execute(
        '''select id, name, count(winner) as wins from players
        left join matches on players.id = matches.winner group by name, id
        order by wins desc;
        '''
    )
    standings = c.fetchall()
    DB.close()
    ids, names, wins = zip(*standings)
    ids = map(int, ids)
    names = map(str, names)
    return zip(ids[::2], names[::2], ids[1::2], names[1::2])
