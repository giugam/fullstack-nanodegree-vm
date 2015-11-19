-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Before creating the table structure we check if these exist
-- if these exists, we delete them
DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS matches CASCADE;
DROP TABLE IF EXISTS standings CASCADE;
-- Create the 'players' table structure
-- This table stores the registered name of a player
-- and it assign each player a unique ID.
CREATE TABLE players (
	name TEXT, 
	reg_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	id SERIAL PRIMARY KEY);
-- Create the 'matches' table structure 
-- This table stores the matches and results between two players
CREATE TABLE matches (
	id1 INTEGER,
	name1 TEXT,
	id2 INTEGER,
	name2 TEXT,
	round INTEGER,
	winner INTEGER,
	loser INTEGER,
	match_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	id_match SERIAL);
-- Create the 'standings' table structure
-- This table generates a view
CREATE TABLE standings (
	id INTEGER REFERENCES players,
	name TEXT,
	wins INTEGER,
	matches INTEGER);

-- Insert Players into players table

INSERT INTO players (name) VALUES
	('Giulio G.'),
	('Payal'),
	('Marc'),
	('Jo'),
	('Gioia'),
	('Fede'),
	('Bhanu'),
	('Rupa'),
	('Terri'),
	('Cristina'),
	('Paolo'),
	('Martina'),
	('Giulio A.'),
	('Chiara'),
	('Stefano'),
	('Samantha');
--
INSERT INTO matches (id1, name1, id2, name2, round, winner, loser) VALUES
	(1,'Giulio',2,'Payal',1,2,1),
	(3,'Marc',4,'Jo',1,3,4),
	(5,'Gioia',6,'Fede',1,6,5),
	(7,'Bhanu',8,'Rupa',1,7,8),
	(9,'Terri',10,'Cristina',1,9,10),
	(11,'Paolo',12,'Martina',1,12,11),
	(13,'Giulio',14,'Chiara',1,13,14),
	(15,'Stefano',16,'Samantha',1,16,15);


/*
CREATE VIEW winner_standing AS
	SELECT players.id, players.name, matches.round,
		matches.winner 
	FROM players RIGHT JOIN matches
	ON players.id = matches.winner 
	ORDER BY matches.winner, players.id;

CREATE VIEW loser_standing AS
	SELECT players.id, players.name, 
		matches.loser, matches.round
	FROM players RIGHT JOIN matches
	ON players.id = matches.loser 
	ORDER BY matches.loser, players.id;
*/

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
    	players.id;

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
    GROUP BY players.id;

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
        wins desc;
