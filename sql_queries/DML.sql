-- CRUD operations for Surf Conditions Reporter


-- READ OPERATIONS:
-- get all users
SELECT * FROM users;

-- get all locations
SELECT * FROM locations;

-- get all stations
SELECT * FROM stations;

-- get all conditions
SELECT * FROM conditions;

-- get all the users locations that are selected
SELECT * FROM users_locations;

-- get all the users conditions that are selected
SELECT * FROM users_conditions;

-- get all stations that serve each location
SELECT * FROM locations_stations;

-- get all conditions read at each station
SELECT * FROM stations_conditions;

-- get all conditions that a user has selected
SELECT condition_id FROM users_conditions WHERE user_id = :user_id;

-- get all locations that a user has selected
SELECT location_id FROM users_locations WHERE user_id = :user_id;

-- CREATE OPERATIONS
--  create new user
INSERT INTO users (username, email) 
VALUES (:username, :email);

-- add a new location
INSERT INTO locations (location_name, coordinates) 
VALUES (:location_name, :coordinates);

-- add a new station
INSERT INTO stations (station_code, station_name, station_url, date_refreshed) 
VALUES (:station_code, :station_name, :station_url, :date_refreshed);

-- add a new condition
INSERT INTO conditions (condition_type, measurement_unit)
VALUES (:condition_type, :measurement_unit);

-- create a user-location relationship (user selects a location they want to get a report for)
INSERT INTO users_locations (user_id, location_id, is_selected) VALUES 
(:user_id, :location_id, :is_selected);

-- create a user-condition relationship (user selects a condition they want to include in the report)
INSERT INTO users_conditions (user_id, condition_id, is_selected) VALUES 
(:user_id, :condition_id, :is_selected);

-- create a new location-station relationship (set which location(s) are monitored by which station(s)) 
INSERT INTO locations_stations (location_id, station_id, is_monitored) VALUES 
(:location_id, :station_id, :is_monitored);

-- create a station-condition relationship (record a weather condition reading from a weather station)
INSERT INTO stations_conditions (station_id, condition_id, condition_reading, wind_direction) VALUES 
(:station_id, :condition_id, :condition_reading, :wind_direction);


-- UPDATE OPERATIONS
-- update a user's email
UPDATE users SET email = :email 
WHERE username = :username;

-- update a location’s coordinates
UPDATE locations SET coordinates = :coordinates 
WHERE location_name = :location_name;

-- update a station's date_refreshed
UPDATE stations SET date_refreshed = :date_refreshed 
WHERE station_code = :station_code;

-- update a condition reading for a station
UPDATE stations_conditions SET condition_reading = :condition_reading
WHERE reading_id = :reading_id;

-- update the is_selected field in users_conditions to change selection status
UPDATE users_conditions SET is_selected = :is_selected 
WHERE user_id = :user_id AND condition_id = :condtion_id;

-- update a condition's measurement units
UPDATE conditions SET measurement_unit = :measurement_unit 
WHERE condition_type = :condition_type;


-- DELETE OPERATIONS:
-- delete a user
DELETE FROM users WHERE user_id = :user_id;

-- delete a location
DELETE FROM locations WHERE location_id = :location_id;

-- delete a station and cascade delete all relationships
DELETE FROM stations WHERE station_id = :station_id;

-- delete a condition and cascade delete all relationships
DELETE FROM conditions WHERE condition_id = :condition_id;

-- delete a user-location relationship (user chooses not to include a location in their report anymore)
DELETE FROM users_locations WHERE user_id = :user_id AND location_id = :location_id;

-- delete user-condition relationship (user chooses not to include a conditino in their report anymore)
DELETE FROM users_conditions WHERE user_id = :user_id AND condition_id = :condition_id;


