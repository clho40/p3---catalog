#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def ExecuteQuery(query,variables=(),fetch_record=False,commit=False):
    """All in One query helper. Thanks to Diego :) """
    conn = connect()
    c = conn.cursor()
    c.execute(query,variables)
    if fetch_record: result = c.fetchall()
    else: result = None
    if commit: conn.commit()
    conn.close()
    return result

def deleteMatches():
    """Remove all the match records from the database."""
    query = "delete from tournament_matches;"
    ExecuteQuery(query,commit=True)
    print("Match records deleted!")


def deletePlayers():
    """Remove all the player records from the database."""
    query = "delete from tournament_player;";
    ExecuteQuery(query,commit=True)
    print("Player records deleted!")


def countPlayers():
    """Returns the number of players currently registered."""
    query = "select count(*) as player_count from tournament_player;"
    result = ExecuteQuery(query,fetch_record=True)
    return result[0][0]

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    query = "insert into tournament_player(name) values (%s);"
    ExecuteQuery(query,[name],commit=True)
    print ("Player {0} has joined the tournament!".format(name))


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    result = ExecuteQuery("select * from v_playerstandings;",fetch_record=True)
    return result

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    ExecuteQuery("select f_reportmatch(%s,%s);",(winner,loser),commit=True)
 
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
    ExecuteQuery("select f_swissParings();",commit=True)
    query = "SELECT m.contestant_1,p1.name,m.contestant_2,p2.name from tournament_matches m, tournament_player p1, tournament_player p2 where p1.id=m.contestant_1 and p2.id=m.contestant_2;"
    result = ExecuteQuery(query,fetch_record=True)
    return result
