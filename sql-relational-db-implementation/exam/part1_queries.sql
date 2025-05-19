-- 1. core table
CREATE TABLE Anime (
	anime_id SERIAL PRIMARY KEY,
	english_name VARCHAR(255) NOT NULL,
	score NUMERIC(4,2) NOT NULL,
	type VARCHAR(50)  NOT NULL,
	episodes INT,
	aired TEXT,
	premiered VARCHAR(50),
	source VARCHAR(50),
	duration VARCHAR(50),
	rating VARCHAR(100),
	ranked NUMERIC,
	popularity INT
);

-- 2. lookup table
CREATE TABLE Genre (
	genre_id SERIAL PRIMARY KEY,
	name VARCHAR(100) NOT NULL
);

CREATE TABLE Studio (
	studio_id SERIAL PRIMARY KEY,
	name VARCHAR(100) NOT NULL
);

CREATE TABLE Producer ( 
	producer_id SERIAL PRIMARY KEY,
	name VARCHAR(100) NOT NULL
);

-- 3. join tables with cascades
CREATE TABLE Anime_Genre (
	anime_genre_id SERIAL PRIMARY KEY,
	anime_id INT NOT NULL REFERENCES Anime(anime_id) ON DELETE CASCADE,
	genre_id INT NOT NULL REFERENCES Genre(genre_id) ON DELETE CASCADE
);

CREATE TABLE Anime_Studio ( 
	anime_studio_id SERIAL PRIMARY KEY,
	anime_id INT NOT NULL REFERENCES Anime(anime_id) ON DELETE CASCADE,
	studio_id INT NOT NULL REFERENCES Studio(studio_id) ON DELETE CASCADE
);

CREATE TABLE Anime_Producer ( 
    anime_producer_id SERIAL PRIMARY KEY,
	anime_id INT NOT NULL REFERENCES Anime(anime_id) ON DELETE CASCADE,
	producer_id INT NOT NULL REFERENCES Producer(producer_id) ON DELETE CASCADE
);

-- 4. insert data into Anime 
INSERT INTO Anime (english_name, score, type, episodes, aired, premiered, source, duration, rating, ranked, popularity)
VALUES
	('Cowboy Bebop', 8.78, 'TV', 26, 'Apr 3, 1998 to Apr 24, 1999', 'Spring 1998', 'Original', '24 min. per ep', 'R - 17+ (violence & profanity)', 28.0, 39),
	('Cowboy Bebop:The Movie', 8.39, 'Movie', 1, 'Sep 1, 2001', NULL, 'Original', '1 hr. 55 min.', 'R - 17+ (violence & profanity)', 159.0, 518),
	('Naruto', 7.91, 'TV', 220, 'Oct 3, 2002 to Feb 8, 2007', 'Fall 2002', 'Manga', '23 min. per ep.', 'PG-13 – Teens 13 or older', 660.0, 8),
	('One Piece', 8.52, 'TV', NULL, 'Oct 20, 1999 to ?', 'Fall 1999', 'Manga', '24 min.', 'PG-13 – Teens 13 or older', 95.0, 31),
	('Mobile Suit Gundam SEED', 7.79, 'TV', 50, 'Oct 5, 2002 to Sep 27, 2003', 'Fall 2002', 'Original', '24 min. per ep.', 'R - 17+ (violence & profanity)', 850.0, 1057),
	('Mobile Suit Gundam SEED Destiny', 7.22, 'TV', 50, 'Oct 9, 2004 to Oct 1, 2005', 'Fall 2004', 'Original', '24 min. per ep.', 'R - 17+ (violence & profanity)', 2687.0, 1530);

-- 5. insert lookup values
INSERT INTO Genre (name) 
VALUES ('Action'), ('Adventure'), ('Drama'), ('Sci-Fi'), ('Space'), ('Shounen'), ('Military');

INSERT INTO Studio (name)
VALUES ('Sunrise'), ('Bones'), ('Studio Pierrot'), ('Toei Animation');

INSERT INTO Producer (name)
VALUES ('Bandai Visual'), ('Sunrise'), ('TV Tokyo'), ('Shueisha'), ('Sotsu'), ('Sony Music Entertainment');

-- 6. inset all many to many links
INSERT INTO Anime_Genre (anime_id, genre_id) VALUES 
	(1,1), (1,2), (1,3), (1,4), (1,5),
	(2,1), (2,3), (2,4), (2,5),
	(3,1), (3,2), (3,6),
	(4,1), (4,2), (4,6),
	(5,1), (5,3), (5,4), (5,5), (5,7),
	(6,1), (6,3), (6,4), (6,5), (6,7);

INSERT INTO Anime_Studio (anime_id, studio_id) VALUES
    (1,1), (2,1), (3,3), (4,4), (5,1), (6,1);

INSERT INTO Anime_Producer (anime_id, producer_id) VALUES
    (1,1), (1,2), (2,1), (2,2), (3,3), (3,4), (4,4), (5,5), (5,6), (6,5), (6,6);

-- verification
SELECT COUNT(*) FROM Anime;
SELECT COUNT(*) FROM Genre;
SELECT COUNT(*) FROM Studio;
SELECT COUNT(*) FROM Producer;
SELECT COUNT(*) FROM Anime_Genre;
SELECT COUNT(*) FROM Anime_Studio;
SELECT COUNT(*) FROM Anime_Producer;
