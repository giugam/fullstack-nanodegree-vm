#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *


def checkRematches():
    """ Check if a rematch has been registered

    Check if the list of matches does not contain duplicates,
    in other words, check if the players have not played
    against each other before.

    Return:
        A list with the matches that appear more than
        once in the list
    """
    conn = connect()
    c = conn.cursor()
    c.execute("""SELECT * FROM rematches_check
                 WHERE counter > 1;""")
    matches_list = c.fetchall()
    if matches_list:
        raise ValueError("A rematch has been found.")
    print "   OK. No rematches has been found."


def testReportMatchesOdd():
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    registerPlayer("Giulio G")
    standings = playerStandings()
    [id1, id2, id3, id4, id5] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    reportSkipRound(id5)
    standings = playerStandings()
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError(
                "Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError(
                "Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError(
                "Each match loser should have zero wins recorded.")
    print "1. (5 Players) After one match, players have updated "\
          "standings."


def testPairingsOdd():
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    registerPlayer("Giulio G")
    standings = playerStandings()
    [id1, id2, id3, id4, id5] = [row[0] for row in standings]
    # Round 1
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    reportSkipRound(id5)
    pairings = swissPairings()
    if len(pairings) != 2:
        raise ValueError(
            "For five players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2),
     (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs_1 = set([frozenset([id1, id5]),
                           frozenset([id2, id4])])
    correct_pairs_2 = set([frozenset([id3, id5]),
                           frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]),
                        frozenset([pid3, pid4])])
    # Check if one of the possible pairs is matching the actual_pairs
    check = 0
    if correct_pairs_1 != actual_pairs:
        check = check + 1
    if correct_pairs_2 != actual_pairs:
        check = check + 1
    if check != 1:
        raise ValueError(
            "After one match with an odd number of players, "
            "the players should not rematch each other.")
    # Check for a rematch
    print "-- After Round 1: "
    checkRematches()
    print "2. (5 Players) After one match, players with one win "\
          "are paired."


def testPairingsOddRound_7_round_1_2():
    print "TOURNAMENT WITH 7 PLAYERS -- ROUND 1 & 2"
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    registerPlayer("Giulio G")
    registerPlayer("Payal P")
    registerPlayer("Extra Player")
    standings = playerStandings()
    [id1, id2, id3, id4, id5, id6, id7] = [row[0] for row in standings]
    # Round 1
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    reportMatch(id5, id6)
    reportSkipRound(id7)
    pairings = swissPairings()
    # Check for a rematch
    print "-- After Round 1"
    checkRematches()
    if len(pairings) != 3:
        raise ValueError(
            "For Seven players, swissPairings should return three pairs.")
    [(pid1, pname1, pid2, pname2),
     (pid3, pname3, pid4, pname4),
     (pid5, pname5, pid6, pname6)] = pairings
    # Round 2
    reportMatch(pid1, pid2)
    reportMatch(pid3, pid4)
    reportMatch(pid5, pid6)
    standings = playerStandings()
    for (i, n, w, m) in standings:
        if m != 2:
            raise ValueError(
                "Each player should have two matches recorded.")
    # Check for a rematch
    print "-- After Round 2"
    checkRematches()
    print "3. (7 Players) After two rounds, players with nearly "\
          "equal win are paired, without rematches."


def testPairingsOddRound_7_round3():
    print "TOURNAMENT WITH 7 PLAYERS -- ROUND 3"
    pairings = swissPairings()
    if len(pairings) != 3:
        raise ValueError(
            "For seven players, swissPairings should return three pairs.")
    [(pid1, pname1, pid2, pname2),
     (pid3, pname3, pid4, pname4),
     (pid5, pname5, pid6, pname6)] = pairings
    reportMatch(pid1, pid2)
    reportMatch(pid3, pid4)
    reportMatch(pid5, pid6)
    standings = playerStandings()
    for (i, n, w, m) in standings:
        if m != 3:
            raise ValueError(
                "Each player should have three matches recorded.")
    # Check for a rematch
    print "-- After Round 3"
    checkRematches()
    print "4. (7 Players) After three rounds, players with nearly "\
          "equal win are paired, without rematches."


def testPairingsOddRound_9_round_1_2():
    print "TOURNAMENT WITH 9 PLAYERS -- ROUND 1 & 2"
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    registerPlayer("Giulio G")
    registerPlayer("Payal P")
    registerPlayer("Mario Bros")
    registerPlayer("Luigi Bros")
    registerPlayer("Extra Player")
    standings = playerStandings()
    [id1, id2, id3, id4,
     id5, id6, id7, id8, id9] = [row[0] for row in standings]
    # Round 1
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    reportMatch(id5, id6)
    reportMatch(id7, id8)
    reportSkipRound(id9)
    standings = playerStandings()
    # Check for a rematch
    print "-- After Round 1"
    checkRematches()
    # Round 2
    pairings = swissPairings()
    if len(pairings) != 4:
        raise ValueError(
            "For Nine players, swissPairings should return four pairs.")
    [(pid1, pname1, pid2, pname2),
     (pid3, pname3, pid4, pname4),
     (pid5, pname5, pid6, pname6),
     (pid7, pname7, pid8, pname8)] = pairings
    reportMatch(pid1, pid2)
    reportMatch(pid3, pid4)
    reportMatch(pid5, pid6)
    reportMatch(pid7, pid8)
    standings = playerStandings()
    for (i, n, w, m) in standings:
        if m != 2:
            raise ValueError(
                "Each player should have two match recorded.")
    # Check for a rematch
    print "-- After Round 2"
    checkRematches()
    print "5. (9 players) After two rounds players with nearly "\
          "equal win are paired, without rematches."


def testPairingsOddRound_9_round_3():
    print "TOURNAMENT WITH 9 PLAYERS -- ROUND 3"
    # Round 3
    pairings = swissPairings()
    if len(pairings) != 4:
        raise ValueError(
            "For nine players, swissPairings should return four pairs.")
    [(pid1, pname1, pid2, pname2),
     (pid3, pname3, pid4, pname4),
     (pid5, pname5, pid6, pname6),
     (pid7, pname7, pid8, pname8)] = pairings
    reportMatch(pid1, pid2)
    reportMatch(pid3, pid4)
    reportMatch(pid5, pid6)
    reportMatch(pid7, pid8)
    standings = playerStandings()
    for (i, n, w, m) in standings:
        if m != 3:
            raise ValueError(
                "Each player should have two match recorded.")
    # Check for a rematch
    print "-- After Round 3"
    checkRematches()
    print "6. (9 players) After three rounds players with nearly "\
          "equal win are paired, without rematches."


def testPairingsEvenRound_16_round_1_2():
    print "TOURNAMENT WITH 16 PLAYERS -- ROUND 1 & 2"
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    registerPlayer("Giulio G")
    registerPlayer("Payal P")
    registerPlayer("Mario Bros")
    registerPlayer("Andy Murray")
    registerPlayer("Stefan Edberg")
    registerPlayer("Carlos Moya")
    registerPlayer("Novak Djokovich")
    registerPlayer("Roger Federer")
    registerPlayer("Pete Sampras")
    registerPlayer("Ivan Lendl")
    registerPlayer("Andre Agassi")
    registerPlayer("Thomas Muster")
    standings = playerStandings()
    [id1, id2, id3, id4, id5,
     id6, id7, id8, id9, id10,
     id11, id12, id13, id14, id15,
     id16] = [row[0] for row in standings]
    # Round 1
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    reportMatch(id5, id6)
    reportMatch(id7, id8)
    reportMatch(id9, id10)
    reportMatch(id11, id12)
    reportMatch(id13, id14)
    reportMatch(id15, id16)
    # Check for a rematch
    print "-- After Round 1"
    checkRematches()
    # Round 2
    pairings = swissPairings()
    if len(pairings) != 8:
        raise ValueError(
            "For sixteen players, swissPairings should return "
            "eight pairs.")
    [(pid1, pname1, pid2, pname2),
     (pid3, pname3, pid4, pname4),
     (pid5, pname5, pid6, pname6),
     (pid7, pname7, pid8, pname8),
     (pid9, pname9, pid10, pname10),
     (pid11, pname11, pid12, pname12),
     (pid13, pname13, pid14, pname14),
     (pid15, pname15, pid16, pname16)] = pairings
    reportMatch(pid1, pid2)
    reportMatch(pid3, pid4)
    reportMatch(pid5, pid6)
    reportMatch(pid7, pid8)
    reportMatch(pid9, pid10)
    reportMatch(pid11, pid12)
    reportMatch(pid13, pid14)
    reportMatch(pid15, pid16)
    # Check for a rematch
    print "-- After Round 2"
    checkRematches()
    print "7. (16 players) After two rounds, players with nearly "\
          "equal win are paired, without rematches."


def testPairingsEvenRound_16_round_3():
    print "TOURNAMENT WITH 16 PLAYERS -- ROUND 3 & 4"
    pairings = swissPairings()
    if len(pairings) != 8:
        raise ValueError(
            "For SIXTEEN players, swissPairings should return "
            "eight pairs.")
    [(pid1, pname1, pid2, pname2),
     (pid3, pname3, pid4, pname4),
     (pid5, pname5, pid6, pname6),
     (pid7, pname7, pid8, pname8),
     (pid9, pname9, pid10, pname10),
     (pid11, pname11, pid12, pname12),
     (pid13, pname13, pid14, pname14),
     (pid15, pname15, pid16, pname16)] = pairings
    # Round 3
    reportMatch(pid1, pid2)
    reportMatch(pid3, pid4)
    reportMatch(pid5, pid6)
    reportMatch(pid7, pid8)
    reportMatch(pid9, pid10)
    reportMatch(pid11, pid12)
    reportMatch(pid13, pid14)
    reportMatch(pid15, pid16)
    # Check for a rematch
    print "-- After Round 3"
    checkRematches()
    pairings = swissPairings()
    if len(pairings) != 8:
        raise ValueError(
            "For SIXTEEN players, swissPairings should return eight pairs.")
    [(pid1, pname1, pid2, pname2),
     (pid3, pname3, pid4, pname4),
     (pid5, pname5, pid6, pname6),
     (pid7, pname7, pid8, pname8),
     (pid9, pname9, pid10, pname10),
     (pid11, pname11, pid12, pname12),
     (pid13, pname13, pid14, pname14),
     (pid15, pname15, pid16, pname16)] = pairings
    # Round 4
    reportMatch(pid1, pid2)
    reportMatch(pid3, pid4)
    reportMatch(pid5, pid6)
    reportMatch(pid7, pid8)
    reportMatch(pid9, pid10)
    reportMatch(pid11, pid12)
    reportMatch(pid13, pid14)
    reportMatch(pid15, pid16)
    # Check for a rematch
    print "-- After Round 4"
    checkRematches()
    print "8. (16 players) After four rounds, players with nearly "\
          "equal win are paired, without rematches."

if __name__ == '__main__':
    # Additional test with an odd (5) number of players
    testReportMatchesOdd()
    testPairingsOdd()
    # Additional test for three rounds with an odd (7) number of players
    testPairingsOddRound_7_round_1_2()
    testPairingsOddRound_7_round3()
    # Additional test for three rounds with an odd (9) number of players
    testPairingsOddRound_9_round_1_2()
    testPairingsOddRound_9_round_3()
    # Additional test for four rounds with an even (16) number of players
    testPairingsEvenRound_16_round_1_2()
    testPairingsEvenRound_16_round_3()
    print "Success!  All tests pass!"
