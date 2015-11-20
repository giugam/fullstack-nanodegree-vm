#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
# Import bleach for input sanitisation
import bleach
# Import random for the swissPairing function
import random

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn=connect() 
    c=conn.cursor() 
    c.execute("DELETE FROM matches;") 
    conn.commit() 
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn=connect() 
    c=conn.cursor() 
    c.execute("DELETE FROM players;") 
    conn.commit() 
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn=connect() 
    c=conn.cursor() 
    # Count the number of players
    c.execute("SELECT count(*) FROM players;") 
    # Retrieve the number of players, which is
    # the first value of the first and only row of the result query 
    total_players = c.fetchall()[0][0]
    conn.close()    
    # Return the number of players
    return total_players


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn=connect()
    c=conn.cursor()
    # Input Sanitization with Bleach
    new_player = bleach.clean(name, strip = True)
    # Insert 'new_player' into the table 'players'
    c.execute("""INSERT INTO players (name) VALUES (%(str)s);""",
      {'str': new_player})
    conn.commit()
    conn.close()


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
    conn=connect()
    c=conn.cursor()
    ### In the select there might be MISSING clause to FILTER & ORDER players
    c.execute("""SELECT * FROM player_standings;""")
    results = c.fetchall();
    player_standings = [(int(row[0]),
                         str(row[1]),
                         int(row[2]),
                         int(row[3])) for row in results];
    conn.close()
    return player_standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn=connect()
    c=conn.cursor()
    # Extracting the data of winner and loser from player_standings
    c.execute("""SELECT * FROM player_standings
                    WHERE player_standings.id = %(id_winner)s
                    OR player_standings.id = %(id_loser)s""",
                {'id_winner': int(winner), 'id_loser':int(loser)})
    current_standings = c.fetchall();

    # THIS IF ELSE MIGHT PROBABLY BE REMOVED LATER ON
    
    if current_standings[0][0] == winner:
        # Keep track of which 'round' is played by taking into account
        # the current number of matches being played by that player
        current_round = current_standings[0][3] + 1;
        # Insert the match result into the table 'matches'
        c.execute("""INSERT INTO matches
                                 (id1, name1, id2,
                                 name2, round, winner, loser)
                            VALUES
                                 (%(id1)s, %(name1)s, %(id2)s,
                                  %(name2)s, %(round)s, %(winner)s,
                                  %(loser)s);""",
                  {'id1': int(current_standings[0][0]),
                   'name1': str(current_standings[0][1]),
                   'id2': int(current_standings[1][0]),
                   'name2': str(current_standings[1][1]),
                   'round': int(current_round),
                   'winner': int(winner),
                   'loser': int(loser) 
                  })
    else:
        current_round = current_standings[1][3] + 1;
        c.execute("""INSERT INTO matches
                                 (id1, name1,
                                  id2, name2,
                                  round, winner, loser)
                             VALUES
                                 (%(id1)s, %(name1)s,
                                 %(id2)s, %(name2)s,
                                 %(round)s, %(winner)s,
                                 %(loser)s);""",
                  {'id1': int(current_standings[0][0]),
                   'name1': str(current_standings[0][1]),
                   'id2': int(current_standings[1][0]),
                   'name2': str(current_standings[1][1]),
                   'round': int(current_round),
                   'winner': int(winner),
                   'loser': int(loser) 
                  })
    print('Current round: ',current_round)
    print(current_standings)
    conn.commit()
    conn.close()
 
 
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
    conn=connect()
    c=conn.cursor()
    # Determining the number of players 
    players_nr = countPlayers() / 2;
    # Pairing the winners
    c.execute("""SELECT id,name FROM player_standings LIMIT (%(half_players)s);""",
              {'half_players': players_nr})
    first_group = c.fetchall();
    #print('FIRST: ',first_group)
    c.execute("""SELECT id,name FROM player_standings OFFSET (%(half_players)s);""",
              {'half_players': players_nr})
    second_group = c.fetchall();
    #print('SECOND: ',second_group)
    # Collecting the two group of player's id
    id_first_group = [(int(row[0])) for row in first_group];
    id_second_group = random.sample([int(row[0]) for row in second_group], players_nr);
    #print('ID1: ',id_first_group)
    #print('ID2: ',id_second_group)
    winner_list = []
    loser_list = []
    steps = players_nr / 2;
    pairs = []
    for i in id_first_group:
        winner_list.append(i)
        for row in first_group:
            if i == row[0]:
                winner_list.append(str(row[1]))
    # slicing the list into pair of players               
    for i in range(1,steps+1):
            pairs.append(tuple(winner_list[(i-1)*4:2*(i*2):1]))
    
    for i in id_second_group:
        loser_list.append(i)
        for row in second_group:
            if i == row[0]:
                loser_list.append(str(row[1]))
                
    for i in range(1,steps+1):
        pairs.append(tuple(loser_list[(i-1)*4:2*(i*2):1]))
    #print(pairs)
    return pairs


