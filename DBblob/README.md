## Database taken from https://datasets.imdbws.com/.

Credit to IMDB for the database.

All dataset are taken in 28th of October 2020.

1000 movies with 100000 user ratings are taken from the database randomly.

Load into MySQL by

```
LOAD DATA LOCAL INFILE 'C:/Users/nakam/Documents/GitHub/ColonD/DBblob/movies_fix.tsv'
INTO TABLE movies
FIELDS TERMINATED BY '\t'
LINES TERMINATED BY '\n';

LOAD DATA LOCAL INFILE 'C:/Users/nakam/Documents/GitHub/ColonD/DBblob/directors_fix.tsv'
INTO TABLE directors
FIELDS TERMINATED BY '\t'
LINES TERMINATED BY '\n';
```