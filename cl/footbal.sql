-- 1) Competitions (competitions.csv)
CREATE TABLE IF NOT EXISTS competitions (
    competition_id     TEXT,
    name               TEXT,
    type               TEXT,
    sub_type           TEXT,
    confederation      TEXT,
    cl_year            INTEGER PRIMARY KEY,
    url                TEXT
);

-- 2) Clubs (CL.csv)
CREATE TABLE IF NOT EXISTS clubs (
    club_id                 TEXT PRIMARY KEY,
    club_code               TEXT,
    name                    TEXT,
    domestic_competition_id TEXT,
    squad_size              INTEGER,
    average_age             NUMERIC,
    foreigners_number       INTEGER,
    foreigners_percentage   NUMERIC,
    stadium_name            TEXT,
    stadium_seats           INTEGER,
    coach_name              TEXT,
    url                     TEXT,
    cl_year                 INTEGER REFERENCES competitions(cl_year)
);


-- 3) Players (players.csv)
CREATE TABLE IF NOT EXISTS players (
    player_id                     BIGINT PRIMARY KEY,
    first_name                    TEXT,
    last_name                     TEXT,
    date_of_birth                 DATE,
    position                      TEXT,
    sub_position                  TEXT,
    height_in_cm                  INTEGER,
    market_value_in_eur           NUMERIC,
    highest_market_value_in_eur   NUMERIC,
    current_club_id               TEXT REFERENCES clubs(club_id),
    current_club_name             TEXT,
    nationality                   TEXT,
    country_of_birth              TEXT,
    city_of_birth                 TEXT,
    agent_name                    TEXT
);

SELECT * FROM competitions WHERE cl_year = 202425;

SELECT * FROM clubs WHERE cl_year = 202425;


