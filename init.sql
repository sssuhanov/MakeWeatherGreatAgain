CREATE TABLE observ
(
	date date NOT NULL,
    temperature int,
    dewpoint int,
    pressure NUMERIC(6,2),
    wind_speed int,
    visibility int,
    max_temperature int,
    min_temperature int,
    max_dewpoint int,
    min_dewpoint int,
    max_humidity int,
    min_humidity int,
    max_wind_speed int,
    min_wind_speed int,
    max_pressure NUMERIC(6,2),
    min_pressure NUMERIC(6,2),
    max_visibility int,
    min_visibility int,
    rain boolean,
    snow boolean,
    fog boolean,
    hail boolean,
    thunder boolean,
    tornado boolean,
    snowfall NUMERIC(6,2)
);

CREATE TABLE temperature
(
	date date NOT NULL PRIMARY KEY,
    temperature NUMERIC(6,2)
);