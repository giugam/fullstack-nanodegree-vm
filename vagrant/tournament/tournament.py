#!/usr/bin/env python
#
# tournament.py -- Implementation of a Swiss-system tournament
#
# Title
# -----
# Project 2: Tournament result
# Full Stack Web Developer Nanodegree - Udacity
#
# Project Description
# -------------------
# The project implement a swiss-system tournament between a number
# of registered players. The tournament supports any number of players
# (even or odd) and it's designed to prevent rematches between players.
# This project does not include a front end.
#
# Module Specification
# ---------------------
# This module defines the functions needed to implement a single
# swiss-system tournament and make use of a PostgreSql database.
#
# Author
# ------
# Giulio Gambardella
#
# Date
# ----
# 12.12.2015


# Import psycopg2 to connect to a PostgreSQL database
import psycopg2
# Import bleach for input sanitisation
import bleach
# Import random for the swissPairings() function
import random
# Import math
import math


def connect(database_name="tournament"):
    """Connect to the database """
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("There was an error connecting to the database")


def deleteMatches():
    """Remove all the match records from the database."""
    db, cursor = connect()
    query = "DELETE FROM matches;"
    cursor.execute(query)
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, cursor = connect()
    query = "DELETE FROM players;"
    cursor.execute(query)
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, cursor = connect()
    # Count the number of players
    query = "SELECT count(*) FROM players;"
    cursor.execute(query)
    # Retrieve the number of players
    total_players = cursor.fetchone()[0]
    db.close()
    # Return the number of players
    return total_players


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.
    (This should be handled by your SQL database schema, not in
    your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db, cursor = connect()
    # Input sanitization
    new_player = bleach.clean(name, strip=True)
    # Register the new player
    query = "INSERT INTO players (name) VALUES (%s);"
    parameter = (new_player,)
    cursor.execute(query, parameter)
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records,
       sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id,name,wins,matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db, cursor = connect()
    # Extracting the players from the player_standings VIEW in
    # the database
    query = "SELECT * FROM player_standings;"
    cursor.execute(query)
    results = cursor.fetchall()
    player_standings = [(int(row[0]),
                         str(row[1]),
                         int(row[2]),
                         int(row[3])) for row in results]
    db.close()
    return player_standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, cursor = connect()
    # Passing the parameters to extract the winner and loser
    # from the player_standings VIEW in the database
    query = """SELECT * FROM player_standings
               WHERE (player_standings.id = %s
               OR player_standings.id = %s);"""
    parameter = (int(winner), int(loser))
    cursor.execute(query, parameter)
    current_standings = cursor.fetchall()
    # Keep track of which 'round' is played by taking into account
    # the current number of matches being played by that player
    current_round = current_standings[0][3] + 1
    # Insert the match result into the table 'matches'
    id1 = bleach.clean(int(current_standings[0][0]), strip=True)
    name1 = bleach.clean(str(current_standings[0][1]), strip=True)
    id2 = bleach.clean(int(current_standings[1][0]), strip=True)
    name2 = bleach.clean(str(current_standings[1][1]), strip=True)
    round_nr = bleach.clean(int(current_round), strip=True)
    winner = bleach.clean(int(winner), strip=True)
    loser = bleach.clean(int(loser), strip=True)
    # Query
    query = """INSERT INTO matches
                           (id1, name1, id2,
                           name2, round, winner, loser)
                      VALUES
                           (%s, %s, %s,%s, %s, %s,%s);"""
    parameter = (id1, name1, id2, name2, round_nr, winner, loser)
    cursor.execute(query, parameter)
    db.commit()
    db.close()


def reportSkipRound(player):
    """ Record the automatic win of a randomly selected player

    The selected player will receive a BYE flag, meaning it will
    skip that round, and it will also automatically receive a win.

     Args:
         player: the id of the randomly selected player
    """
    db, cursor = connect()
    # Extracting the data of player that will skip the round
    # from the table 'player_standings'
    query = """SELECT * FROM player_standings
                 WHERE player_standings.id = %s;"""
    parameter = (player,)
    cursor.execute(query, parameter)
    plr_standings = cursor.fetchall()
    # Keep track of which 'round' is played by taking into account
    # the current number of matches being played by that player
    current_round = plr_standings[0][3] + 1
    # Record the automatic win to skip this round
    #
    # The data of the player that will skip the round will be used
    # also for the remaining fields, to ensure database integrity
    query = """INSERT INTO matches
                     (id1, name1, id2, name2,
                     round, winner, loser, bye)
                 VALUES
                     (%s, %s, %s, %s, %s, %s, %s, %s);"""
    # Input sanitization of various parameters
    id1 = bleach.clean(int(plr_standings[0][0]), strip=True)
    name1 = bleach.clean(str(plr_standings[0][1]), strip=True)
    id2 = bleach.clean(int(plr_standings[0][0]), strip=True)
    name2 = bleach.clean(str(plr_standings[0][1]), strip=True)
    round_nr = bleach.clean(int(current_round), strip=True)
    winner = bleach.clean(int(player), strip=True)
    loser = bleach.clean(int(player), strip=True)
    skip_round = 1
    # Assigning the parameters
    parameter = (id1, name1, id2, name2, round_nr, winner, loser, skip_round)
    cursor.execute(query, parameter)
    db.commit()
    db.close()


def selectWhoSkipRound():
    """ Select a random player to skip one round

    For the first round of matches, the player wil be selected
    randomly amongst the registered players
    In the following rounds the player will be selected amongst
    the players who have never received a BYE flag

    Returns: The player id that will skip that round
    """
    db, cursor = connect()
    # Select the players which skipped a round
    # from the 'matches_bye' VIEW
    query = "SELECT * FROM matches_bye;"
    cursor.execute(query)
    skip_player_list = cursor.fetchall()
    # Select all the players from the player_standings VIEW
    query = "SELECT * FROM player_standings;"
    cursor.execute(query)
    all_players = cursor.fetchall()
    # If the number of players is odd and it's the first round
    if countPlayers() % 2 != 0 and len(skip_player_list) == 0:
        # Randomly selects one of the player's id which will
        # skip one round from all available players
        id_extra_player = random.choice([(int(row[0]))
                                         for row in all_players])
    # If the number of players is odd and there have been players
    # who have received a BYE flag
    elif countPlayers() % 2 != 0 and len(skip_player_list) != 0:
        # Select all the players from the player_standings VIEW
        # who have already won a match
        query = "SELECT * FROM player_standings WHERE wins >= 1;"
        cursor.execute(query)
        all_players = cursor.fetchall()
        # Populate a filtered_players list that will be filtered
        # in order to remove players who have skipped a round
        filtered_players = [(int(row[0])) for row in all_players]
        # Remove players from the filtered_players list by checking
        # if any players in it have skipped a round
        for skip_player in skip_player_list:
            for player_id in all_players:
                if player_id[0] == skip_player[0]:
                    # Remove players who have skipped
                    filtered_players.remove(player_id[0])
        # Select the players that will skip this round amongst those
        # players in the previously filtered list
        id_extra_player = random.choice([(int(player))
                                         for player in filtered_players])
    db.close()
    return id_extra_player


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    If there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired
    with another player with an equal or nearly-equal win record,
    that is, a player adjacent to him or her in the standings.

    Additional implementations:
    If there is an odd number of registered players, another
    function selectWhoSkipRound() will determine the player id that
    will skip the round, and the remaining players will paired as
    previously described.

    The swissPairings() function also prevents players from playing
    twice against each other

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db, cursor = connect()
    # Determine if the number of players is even or odd
    if countPlayers() % 2 == 0:
        # The number of registered players is even,
        # therefore the players will be split in two groups
        # in which each group will contain half of the players.
        #
        # If the two sub groups contain an odd number of players,
        # reassign one player in order to have an even number of
        # players in both groups
        if (countPlayers() / 2) % 2 != 0:
            top_group_nr = countPlayers() / 2 + 1
            bottom_group_nr = countPlayers() / 2 - 1
        else:
            top_group_nr = bottom_group_nr = countPlayers() / 2
        # Select the top half of the players present in the
        # player_standings VIEW by passing the parameter 'half_players_nr'
        query = "SELECT id, name FROM player_standings LIMIT %s;"
        parameter = (top_group_nr,)
        cursor.execute(query, parameter)
        first_group = cursor.fetchall()
        # Select the remaining bottom half of the players present in the
        # player_standings VIEW by passing the parameter 'half_players_nr'
        query = "SELECT id, name FROM player_standings OFFSET %s;"
        parameter = (bottom_group_nr,)
        cursor.execute(query, parameter)
        second_group = cursor.fetchall()
    else:
        # The number of registered players is odd,
        # therefore one player will receive a BYE flag
        # which will take this player to the next round with an auto
        # assigned win. All the remaining players will be split
        # into two groups as before.
        half_players_nr = (countPlayers() - 1) / 2
        # If the remaining players are odd, reassing one player
        # in order to have an even number of players in both groups
        if half_players_nr % 2 != 0:
            # Since one player will skip a round and it will receive
            # an automatic win, the top group will be reduced to
            # equalise the players distribution
            top_group_nr = countPlayers() / 2 - 1
            bottom_group_nr = countPlayers() / 2 + 1
        else:
            top_group_nr = bottom_group_nr = countPlayers() / 2
        # Determine the id of the player that will skip this round
        id_extra_player = selectWhoSkipRound()
        # Select the players according to their standing but excluding
        # the player that will skip this round
        query = "SELECT id, name FROM player_standings WHERE id != %s;"
        parameter = (id_extra_player,)
        cursor.execute(query, parameter)
        filtered_list = cursor.fetchall()
        # Assign this player a BYE flag for this round, as well as
        # an automatic win.
        reportSkipRound(id_extra_player)
        # Assign the players in the two separate lists
        first_group = filtered_list[0:top_group_nr:1]
        second_group = filtered_list[
                       top_group_nr:top_group_nr+bottom_group_nr:1]

    # Once the players are divided into two groups, extract the
    # player's id contained in the two list 'first_group'and
    # 'second_group'
    id_first_group = [int(row[0]) for row in first_group]
    id_second_group = [int(row[0]) for row in second_group]
    # Create two list of matches by pairing two player's id sequentially,
    # for each of the players that are present in both lists
    first_pairs_matched = []
    for i in range(1, top_group_nr / 2 + 1):
        first_pairs_matched.append(
                            tuple(id_first_group[(i-1)*2:(i*2):1]))
    second_pairs_matched = []
    for i in range(1, bottom_group_nr / 2 + 1):
        second_pairs_matched.append(
                             tuple(id_second_group[(i-1)*2:(i*2):1]))
    # Select the matches that have already being played, excluding
    # the cases where a player skipped around
    query = "SELECT id1, id2 FROM matches WHERE bye = 0;"
    cursor.execute(query)
    matches_played = cursor.fetchall()
    # Define empty lists that will be used to prevent rematching
    # between players, and that will also be used to reconstruct the
    # final list of tuples:
    #
    # Define the final list of tuples [(id1,name1),(id2,name2),..]
    pairs_matched = []
    # Define the list that will contain the matches amongst players
    # present in the 'first_group'
    pairs_matched_first = []
    # Define the list that will contain the matches amongst players
    # present in the 'second_group'
    pairs_matched_second = []
    # Define a duplicate list that will contain the id of the players
    # present in the 'first_group'
    match_item_first = []
    # Define a duplicate list that will contain the id of the players
    # present in the 'first_group'
    match_item_second = []

    # Reassign the players id in the first group to a temporary list
    match_item_f = [(int(row[0])) for row in first_group]

    # Prevent rematching of same players by swapping adjacent
    # players in order to match players with nearly equal
    # ranking (wins)
    #
    # For example:
    # if (i,j) and (k,l) are two matches and (k,l) is a rematch
    # then swap players j and k so that the new pairing is:
    # (i,k) and (j,l)

    # Define the condition to interrupt the loop
    rematch_found = True
    # Check continuously the list of matches against the list of
    # matches already played
    while rematch_found is not False:
        rematch_found = False
        for match in first_pairs_matched:
            p = match[0]
            q = match[1]
            inverse = (q, p)
            if match in matches_played:
                rematch_found = True
                # Retrieve index of the match already played
                i = first_pairs_matched.index(match)
                if i == 0:
                    # Retrieve indexes of players to swap
                    # from the list
                    j = match_item_f.index(first_pairs_matched[0][1])
                    k = match_item_f.index(first_pairs_matched[1][0])
                else:
                    # Retrieve indexes of players to swap
                    # from the list
                    j = match_item_f.index(first_pairs_matched[i-1][1])
                    k = match_item_f.index(first_pairs_matched[i][0])
                # Retrieve players id
                val_j = match_item_f[j]
                val_k = match_item_f[k]
                # Swap values k -> j and j -> k
                match_item_f[j] = val_k
                match_item_f[k] = val_j
            if inverse in matches_played:
                rematch_found = True
                # Retrieve index of the match already played
                i = first_pairs_matched.index(match)
                if i == 0:
                    # Retrieve indexes of players to swap
                    # from the list
                    j = match_item_f.index(first_pairs_matched[0][1])
                    k = match_item_f.index(first_pairs_matched[1][0])
                else:
                    # Retrieve indexes of players to swap
                    # from the list
                    j = match_item_f.index(first_pairs_matched[i-1][1])
                    k = match_item_f.index(first_pairs_matched[i][0])
                # Retrieve players id
                val_j = match_item_f[j]
                val_k = match_item_f[k]
                # Swap values k -> j and j -> k
                match_item_f[j] = val_k
                match_item_f[k] = val_j

        if rematch_found is True:
            # Reconstruct the matches
            first_pairs_matched = []
            for i in range(1, top_group_nr / 2 + 1):
                first_pairs_matched.append(
                                    tuple(match_item_f[(i-1)*2:(i*2):1]))
            # Return checking if a match is present in the new list
            continue
        # If a rematch is NOT found exit the loop
        else:
            break

    # Construct the matches list for the first group of players
    # having the form: [(id1,name1,id2,name2,...)]
    for j in match_item_f:
        match_item_first.append(j)
        for row in first_group:
            if j == row[0]:
                match_item_first.append(str(row[1]))
    # Slice the list into tuples having the form:
    # [(id1,name1,id2,name2),(id3,name3,id4,name4),...]
    for i in range(1, top_group_nr / 2 + 1):
        pairs_matched_first.append(
                            tuple(match_item_first[(i-1)*4:2*(i*2):1]))
    # Repeat the same steps described above for the
    # remaining players present in the second group

    # Reassign the players id in the second group to a temporary list
    match_item_s = [(int(row[0])) for row in second_group]

    # Prevent rematching of same players by swapping adjacent
    # players in order to match players with nearly equal
    # ranking (wins)

    # Define the condition to interrupt the loop
    rematch_found = True
    # Check continuously the list of matches against the list of
    # matches already played
    while rematch_found is not False:
        rematch_found = False
        for match in second_pairs_matched:
            # Defining the inverse of 'match' by swapping the
            # player's id.
            p = match[0]
            q = match[1]
            inverse = (q, p)
            # Check for a possible rematch
            if match in matches_played:
                rematch_found = True
                # retrieve index of the match already played
                i = second_pairs_matched.index(match)
                if i == 0:
                    # retrieve indexes of players to swap
                    # from the list
                    j = match_item_s.index(second_pairs_matched[0][1])
                    k = match_item_s.index(second_pairs_matched[1][0])
                else:
                    # retrieve indexes of players to swap
                    # from the list
                    j = match_item_s.index(second_pairs_matched[i-1][1])
                    k = match_item_s.index(second_pairs_matched[i][0])
                # retrieve players id
                val_j = match_item_s[j]
                val_k = match_item_s[k]
                # swap values
                match_item_s[j] = val_k
                match_item_s[k] = val_j
            # Check for a possible rematch having the same players
            # but swapping the position of their id.
            # (for example: if 'match' is (p,q) -> 'inverse' is (q,p))
            if inverse in matches_played:
                rematch_found = True
                # retrieve index of the match already played
                i = second_pairs_matched.index(match)
                if i == 0:
                    # retrieve indexes of players to swap
                    # from the list
                    j = match_item_s.index(second_pairs_matched[0][1])
                    k = match_item_s.index(second_pairs_matched[1][0])
                else:
                    # retrieve indexes of players to swap
                    # from the list
                    j = match_item_s.index(second_pairs_matched[i-1][1])
                    k = match_item_s.index(second_pairs_matched[i][0])
                # retrieve players id
                val_j = match_item_s[j]
                val_k = match_item_s[k]
                # swap values
                match_item_s[j] = val_k
                match_item_s[k] = val_j

        if rematch_found is True:
            # Reconstruct the matches list
            second_pairs_matched = []
            for i in range(1, bottom_group_nr / 2 + 1):
                second_pairs_matched.append(
                                     tuple(match_item_s[(i-1)*2:(i*2):1]))
            # Continue checking for a rematch in the original list or
            # in the rearranged list
            continue
        # If a rematch is NOT found exit the loop
        else:
            break

    # Construct the matches list having the form:
    # [(id1,name1,id2,name2,...)]
    for j in match_item_s:
        match_item_second.append(j)
        for row in second_group:
            if j == row[0]:
                match_item_second.append(str(row[1]))
    # Slice the list into tuples having the form:
    # [(id1,name1,id2,name2),(id3,name3,id4,name4),...]
    for i in range(1, bottom_group_nr / 2 + 1):
        pairs_matched_second.append(
                             tuple(match_item_second[(i-1)*4:2*(i*2):1]))
    # Join the lists into the final list of tuples
    pairs_matched_first.extend(pairs_matched_second)
    pairs_matched.extend(pairs_matched_first)
    db.close()
    return pairs_matched
