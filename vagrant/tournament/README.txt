Author: Giulio Gambardella
Date: 12.12.2015
Project: P2 Tournament Results

TITLE
-----
P2: TOURNAMENT RESULTS

LIST OF FILES
-------------
Inside the compressed folder “p2—tr-gambardella” there are the
following files:
- tournament.sql
- tournament.py
- tournament_test.py
- tournament_extra_test.py

PREREQUISITE
------------
Vagrant VM having Python and Psql installed and working.
The following Python modules should also be installed: psycopg2, bleach,
random, math.

INSTRUCTIONS
------------
Unzip the compressed file "p2-tr-gambardella.zip".
In order to create the tables and views required for the 'tournament'
database it is necessary to run 'psql' from Vagrant and then run 
the command: \i tournament.sql 
In order to run the application to verify the standard requirements it
is neccesary to run the module: tournament_test.py
In order to run the application to verify the extra credits that have been 
implemented it is neccesary to run the module: tournament_extra_test.py.

ADDITIONAL NOTES
----------------
The tournament.sql file contains two tables: 
- players: it stores the registered player's 'name' and 'id'. The 'id' is
		   the primary key and it is assigned to a player every time a
		   player is registered.
- matches: it stores the outcome of a match between two players. For every
		   match it stores the id and name of both players ('id1','name1',
		   'id2','name2'), as well as the current 'round', the id of the 
		   'winner' and the 'loser', a value 'bye' stores the skip of a 
		   round, and a unique 'id_match' assigned automatically.   
The tournament.sql file also contains the following four views: 
- matches_won: it lists the players by counting their respective wins; 
- matches_bye: it lists the players by counting their respective BYE flags 
  			   received when these players have skipped a round;
- matches_played: it lists the players by counting their respective
				  matches played;
- player_standings: it lists the players providing the players 
					id, name, the number of wins and the number of matches 
					played, and the players are ordered by their wins in a
					decreasing order;
- rematches_check: it lists the registered matches between two players
				   and counts their number. 
The module tournament.py implements all the functions required to pass the
standard test contained in tournament_test.py, as well as the two extra
credits implemented.
Extra credits implemented: 
1. The tournament doesn't assume an even number of players, therefore any
   number of players (even or odd) can be registered.
2. The tournament prevents rematches between the players.
An additional separate testing module called: tournament_extra_test.py
contains the tests for the extra credits that have been implemented.
Two additional functions are present in tournament.py, these are called:
selectWhoSkipRound() and reportSkipRound(). Both of them are called within
the swissPairing() function when the number of registered players is odd.
The swissPairings() function is designed to work with any number of 
registered players and it is called always after the first round. This
function divides the registered players in two groups based on their
win's standings. Depending if the number of players in the two groups is
even or odd, the function distributes the players in order to obtain two
even groups. The pairings of new matches between players is done 
sequentially and according to the player's standing. The function
generates a list of matches and then it loops through each of them in
order to check if a rematch exists. If a rematch is found, two adjacent
players swap their position in order to prevent a rematch. This test ends
when the proposed list of matches does not contains players that have been
matched before.