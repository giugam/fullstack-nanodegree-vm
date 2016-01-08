-- Table definitions for the tournament project.

-- Project 2: Tournament results
-- Author: Giulio Gambardella
-- Date: 12.15.2015

-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Before creating the database, check if it exsists,
-- if the database exists delete it.

-- Drop all connections
-- More info at: http://stackoverflow.com/questions/5408156
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'tournament'
  AND pid <> pg_backend_pid();

-- Drop database
DROP DATABASE tournament;

-- Create the database ' tournament'

CREATE DATABASE tournament;

-- Connect to the database and run this file
\c tournament;
-- Before creating the table structure, check if these exist,
-- if these tables already exist delete them, as well as deleting
-- the views which depends on the tables.
DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS matches CASCADE;
-- Define the 'players' table structure
-- This table stores the registered name of a player
-- and it assigns each player a unique ID (primary key).
CREATE TABLE players (
    -- Require the player's name when it is registered
	name TEXT NOT NULL, 
	-- reg_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	id SERIAL PRIMARY KEY);
-- Define the 'matches' table structure 
-- This table stores the matches and results between two players
CREATE TABLE matches (
    -- Reference (FKEYS) winner/loser to the player's id
	id1 INTEGER REFERENCES players (id),
	name1 TEXT,
	id2 INTEGER REFERENCES players (id),
    name2 TEXT,
	round INTEGER,
    -- Reference (FKEYS) winner/loser to the player's id
	winner INTEGER REFERENCES players (id),
	loser INTEGER REFERENCES players (id),
	bye INTEGER DEFAULT 0,
	id_match SERIAL PRIMARY KEY);
-- Define the 'matches_won' view 
-- This view lists the players by counting their wins.
-- The players are ordered by their wins in decreasing order.
CREATE VIEW matches_won AS
    SELECT
    	players.id, 
    	players.name,
        Count(matches.winner) AS mwon
    FROM 
    	players, matches 
    WHERE 
    	players.id = matches.winner
    GROUP BY 
    	players.id
    ORDER BY
    	mwon DESC;
-- Define the 'matches_bye' view 
-- This view lists the players by counting their respective
-- BYE flags received when these players have skipped a round.
-- The players are ordered by the number of BYE received in a
-- decreasing order.
CREATE VIEW matches_bye AS
	SELECT 
		players.id,
		players.name,
		Count(matches.bye) AS mbye
	FROM 
		players, matches
	WHERE
		players.id = matches.winner 
	AND 
		matches.bye = 1
	GROUP BY
		players.id
	ORDER BY
		mbye DESC;
-- Define the 'matches_bye' view 
-- This view lists the players by counting their respective
-- matches played.
-- The players are ordered by their matches played in a 
-- decreasing order;
CREATE VIEW matches_played AS
    SELECT 
    	players.id,
    	players.name,  
    	CASE 
    		WHEN Count(matches.id1) = Null THEN 0
    		ELSE Count(matches.id1) 
    	END AS mplayed
    FROM 
    	players 
    LEFT JOIN 
    	matches 
    ON 
    	players.id = matches.winner
    OR 
    	players.id = matches.loser
    GROUP BY players.id
    ORDER BY 
    	mplayed DESC;
-- Define the 'player_standings' view 
-- This view lists the players providing the players id, name, 
-- the number of wins and the number of matches played, and the
-- players are ordered by their win in a decreasing order.
CREATE VIEW player_standings AS
    SELECT
        matches_played.id,
        matches_played.name,
        COALESCE(matches_won.mwon,0) AS wins,
        COALESCE(matches_played.mplayed,0) AS matches
    FROM
        matches_played
    LEFT JOIN
        matches_won
    ON
        matches_played.id = matches_won.id OR mwon = 0
    ORDER BY
        wins DESC;
-- Define the 'rematches_check' view
-- This view lists the registered matches between players
-- showing how many matches 
CREATE VIEW rematches_check AS
	SELECT 
		id1, id2, count(id_match) as counter 
	FROM
		matches 
	GROUP BY id1, id2;

