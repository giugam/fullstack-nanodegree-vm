-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS matches;

CREATE TABLE players (
	name TEXT, 
	reg_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	id SERIAL);

CREATE TABLE matches (
	id1 integer,
	name1 text,
	id2 integer,
	name2 text,
	round integer,
	winner integer,
	loser integer,
	match_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	id_match serial);

-- Insert Players into players table
INSERT INTO players (name) VALUES
	('Giulio'),
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
	('Giulio'),
	('Chiara'),
	('Stefano'),
	('Samantha');

--
INSERT INTO matches (id1, name1, id2, name2, round, winner, loser) VALUES
	(1,'Giulio',2,'Payal',1,1,2),
	(3,'Marc',4,'Jo',1,1,2),
	(5,'Gioia',6,'Fede',1,1,2),
	(7,'Bhanu',8,'Rupa',1,1,2),
	(9,'Terri',10,'Cristina',1,1,2),
	(11,'Paolo',12,'Martina',1,1,2),
	(13,'Giulio',14,'Chiara',1,1,2),
	(15,'Stefano',16,'Samantha',1,1,2);

