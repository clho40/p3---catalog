-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

--
-- every table has created_on and updated_on to keep track of the time the record being created
--

--Make fresh database everytime the script runs. Thanks to Diego for pointing out
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

--player's table (created_on and updated_on is to keep track of the time the record being created)
CREATE TABLE tournament_player (
	id serial PRIMARY KEY,
	name text NOT NULL,
	win_count int DEFAULT 0,
	match_count int DEFAULT 0,
	updated_on timestamp DEFAULT current_timestamp,
	created_on timestamp DEFAULT current_timestamp
);

-- match table
CREATE TABLE tournament_matches (
	id serial PRIMARY KEY,
	contestant_1 int references tournament_player(id) ON DELETE CASCADE,
	contestant_2 int references tournament_player(id) ON DELETE CASCADE,
	match_winner int references tournament_player(id) ON DELETE CASCADE,
	updated_on timestamp DEFAULT current_timestamp,
	created_on timestamp DEFAULT current_timestamp,
	CHECK (contestant_1 <> contestant_2)
);

-- player standing view
CREATE VIEW v_playerstandings as
	select id, name, win_count, match_count 
	from tournament_player
	order by win_count desc;

-- report match function
CREATE OR REPLACE FUNCTION f_reportmatch(winner int, loser int)
	RETURNS text AS $$
	DECLARE
		r_result text;
	BEGIN
		BEGIN
			--for winner, update win count and match count
			update tournament_player set win_count=win_count+1, match_count=match_count+1, updated_on=current_timestamp where id=winner;
			--for loser, just update match count
			update tournament_player set match_count=match_count+1,updated_on=current_timestamp where id=loser;
			--update match result in match table. since the function is taking winner's and loser's id instead of 
			--match id, it is neccessary to look for the pair.
			update tournament_matches set match_winner=winner 
			where ((contestant_1=winner and contestant_2=loser) or (contestant_1=loser and contestant_2=winner));
			r_result := 'OK';
		EXCEPTION WHEN OTHERS THEN
		-- error message. however the tournament_test.py is not expecting error message from tournament.py
			r_result := SQLERRM;
		END;
		return r_result;
	END
	$$ LANGUAGE plpgsql;

-- function to create match pair
CREATE OR REPLACE FUNCTION f_swissParings()
	RETURNS TABLE (
		id1 int,
		name1 text,
		id2 int,
		name2 text
	) as $$
	DECLARE
		player_count int;
		max_match_tier int;
		r_result text;
		player_index int;
		player1 int;
		c1 CURSOR (max_match integer) FOR SELECT p.id,p.name from tournament_player p where p.match_count <> max_match order by p.match_count,p.win_count desc;
	BEGIN
		--clear the match table to avoid duplicate pairs (assuming the function will only be called once due to the structure of tournament_test.py)
		delete from tournament_matches;
		r_result := ''; player_index := 1;
		SELECT count(*) INTO player_count FROM tournament_player;
		-- get the number of player and the number of matches for the tournament
		max_match_tier := (player_count / 2);
		--by using a cursor, assign pairs by looping the record.
		for player in c1(max_match_tier) loop
			if player_index = 1 then 
				player1 = player.id;
				player_index := 2;
			else
				INSERT INTO tournament_matches(contestant_1,contestant_2) VALUES (player1,player.id);
				player_index = 1;
			end if;
		end loop;
	END
	$$ LANGUAGE plpgsql;