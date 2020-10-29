DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS directors;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL,
  username VARCHAR(30) UNIQUE NOT NULL,
  email VARCHAR(50) UNIQUE NOT NULL, 
  password TEXT NOT NULL
);

CREATE TABLE directors (
  id VARCHAR(10) PRIMARY KEY NOT NULL,
  director_name VARCHAR(40) NOT NULL,
  birth_year SMALLINT,
  well_known_titles VARCHAR(100)
);

CREATE TABLE movies (
  id VARCHAR(10) PRIMARY KEY NOT NULL,
  movie_name VARCHAR(100) NOT NULL,
  year_rel SMALLINT,
  runtime SMALLINT,
  genres TEXT,
  director_id VARCHAR(10) NOT NULL,
  FOREIGN KEY (director_id) REFERENCES directors(id)
);

CREATE TABLE review (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  movie_id VARCHAR(10) NOT NULL,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  star TINYINT UNSIGNED,
  FOREIGN KEY (movie_id) REFERENCES movies(id),
  FOREIGN KEY (author_id) REFERENCES user(id)
);