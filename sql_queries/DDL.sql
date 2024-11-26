-- CS340 Group 1
-- Kent Tolzmann, Ryan Messenger
-- Project Step 2 Draft 1

-- Data Definition Queries:
-- Main Tables
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    user_id int AUTO_INCREMENT NOT NULL, 
    username varchar(255) NOT NULL,
    email varchar(255) NOT NULL,
    CONSTRAINT username UNIQUE (username),
    CONSTRAINT email UNIQUE (email),
    PRIMARY KEY (user_id)
    );
    
DROP TABLE IF EXISTS locations;
CREATE TABLE locations (
    location_id int AUTO_INCREMENT NOT NULL,
    location_name varchar(255) NOT NULL,
    coordinates varchar(255),
    CONSTRAINT location_name UNIQUE (location_name),
    PRIMARY KEY (location_id)
);

DROP TABLE IF EXISTS stations;
CREATE TABLE stations (
    station_id int AUTO_INCREMENT NOT NULL,
    station_code varchar(20) NOT NULL,
    station_name varchar(255) NOT NULL,
    station_url varchar(1000) NOT NULL,
    CONSTRAINT station_name UNIQUE (station_name),
    CONSTRAINT station_code UNIQUE (station_code),
    PRIMARY KEY (station_id)
);

DROP TABLE IF EXISTS conditions;
CREATE TABLE conditions (
    condition_id int AUTO_INCREMENT not NULL,
    condition_type varchar(50) NOT NULL,
    measurement_unit varchar(20) NOT NULL,
    PRIMARY KEY (condition_id)
);

-- Table Intersections
DROP TABLE IF EXISTS users_locations;
CREATE TABLE users_locations (
    user_id int NOT NULL,
    location_id int NOT NULL,
    PRIMARY KEY (user_id, location_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE,
    FOREIGN KEY (location_id) REFERENCES locations(location_id)
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS users_conditions;
CREATE TABLE users_conditions (
    user_id int NOT NULL,
    condition_id int NOT NULL,
    PRIMARY KEY (user_id, condition_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE,
    FOREIGN KEY (condition_id) REFERENCES conditions(condition_id)
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS locations_stations;
CREATE TABLE locations_stations (
    location_id int NOT NULL,
    station_id int NOT NULL, 
    PRIMARY KEY (location_id, station_id),
    FOREIGN KEY (location_id) REFERENCES locations(location_id)
        ON DELETE CASCADE,
    FOREIGN KEY (station_id) REFERENCES stations(station_id)
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS stations_conditions;
CREATE TABLE stations_conditions (
    reading_id int AUTO_INCREMENT NOT NULL,
    station_id int NOT NULL,
    condition_id int NOT NULL,
    condition_reading decimal(5,2) NOT NULL,
    wind_direction varchar(10),
    date_refreshed DATE,
    PRIMARY KEY (reading_id),
    FOREIGN KEY (station_id) REFERENCES stations(station_id)
        ON DELETE CASCADE,
    FOREIGN KEY (condition_id) REFERENCES conditions(condition_id)
        ON DELETE CASCADE
);


-- Sample data INSERT statements
-- Main Tables
INSERT INTO users (username, email) VALUES 
('tolzmank', 'tolzmank@oregonstate.edu'),
('messengr', 'messengr@oregonstate.edu'),
('surfbro1', 'browhosurfs@gmail.com');

INSERT INTO locations (location_name, coordinates) VALUES 
('Keahi Point - HI', '21.32027778 N, 157.97833333 W'),
('White Plains - HI', '21.30277778 N, 158.04555556 W'),
('Puaena Point - HI', '21.60222222 N, 158.10500000 W'),
('Ocean Beach - CA', '32.75305556 N, 117.25333333 W');

INSERT INTO stations (station_code, station_name, station_url) VALUES 
('51211', 'Pearl Harbor Entrance, HI', 'https://www.ndbc.noaa.gov/station_page.php?station=51211'),
('51201', 'Waimea Bay, HI', 'https://www.ndbc.noaa.gov/station_page.php?station=51201'),
('46237', 'San Francisco Bar, CA', 'https://www.ndbc.noaa.gov/station_page.php?station=46237'),
('PHNL', 'Daniel K Inouye International Airport', 'https://forecast.weather.gov/MapClick.php?lat=21.3178&lon=-157.9202'),
('PHHI', 'Wheeler Air Force Base / Oahu', 'https://forecast.weather.gov/MapClick.php?lon=-158.1148491427302&lat=21.589120977127592'),
('SFOC1', 'SAN FRANCISCO DOWNTOWN', 'https://forecast.weather.gov/MapClick.php?lat=37.7594&lon=-122.5107'),
('1612366', 'FORT KAMEHAMEHA, BISHOP POINT, PEARL HBR, HI', 'https://tidesandcurrents.noaa.gov/noaatidepredictions.html?id=1612366');


INSERT INTO conditions (condition_type, measurement_unit) VALUES 
('Swell Height', 'ft'),
('Swell Period', 'sec'),
('Wind Speed', 'kts'),
('Tide Level', 'ft');

-- Intersection Tables
INSERT INTO locations_stations (location_id, station_id) VALUES 
((SELECT location_id FROM locations WHERE location_name = 'Keahi Point - HI'), (SELECT station_id FROM stations WHERE station_code = '51211')),
((SELECT location_id FROM locations WHERE location_name = 'White Plains - HI'), (SELECT station_id FROM stations WHERE station_code = '51211')),
((SELECT location_id FROM locations WHERE location_name = 'Puaena Point - HI'), (SELECT station_id FROM stations WHERE station_code = '51201')),
((SELECT location_id FROM locations WHERE location_name = 'Ocean Beach - CA'), (SELECT station_id FROM stations WHERE station_code = '46237')),

((SELECT location_id FROM locations WHERE location_name = 'Keahi Point - HI'), (SELECT station_id FROM stations WHERE station_code = 'PHNL')),
((SELECT location_id FROM locations WHERE location_name = 'White Plains - HI'), (SELECT station_id FROM stations WHERE station_code = 'PHNL')),
((SELECT location_id FROM locations WHERE location_name = 'Puaena Point - HI'), (SELECT station_id FROM stations WHERE station_code = 'PHHI')),
((SELECT location_id FROM locations WHERE location_name = 'Ocean Beach - CA'), (SELECT station_id FROM stations WHERE station_code = 'SFOC1')),
((SELECT location_id FROM locations WHERE location_name = 'Keahi Point - HI'), (SELECT station_id FROM stations WHERE station_code = '1612366')),
((SELECT location_id FROM locations WHERE location_name = 'White Plains - HI'), (SELECT station_id FROM stations WHERE station_code = '1612366'));

INSERT INTO users_locations (user_id, location_id) VALUES 
((SELECT user_id FROM users WHERE username = 'tolzmank'), (SELECT location_id FROM locations WHERE location_name = 'Keahi Point - HI')),
((SELECT user_id FROM users WHERE username = 'tolzmank'), (SELECT location_id FROM locations WHERE location_name = 'White Plains - HI')),
((SELECT user_id FROM users WHERE username = 'messengr'), (SELECT location_id FROM locations WHERE location_name = 'Ocean Beach - CA'));

INSERT INTO users_conditions (user_id, condition_id) VALUES 
((SELECT user_id FROM users WHere username = 'tolzmank'), (SELECT condition_id FROM conditions WHERE condition_type = 'Swell Height')),
((SELECT user_id FROM users WHere username = 'tolzmank'), (SELECT condition_id FROM conditions WHERE condition_type = 'Swell Period')),
((SELECT user_id FROM users WHere username = 'tolzmank'), (SELECT condition_id FROM conditions WHERE condition_type = 'Tide Level')),
((SELECT user_id FROM users WHere username = 'messengr'), (SELECT condition_id FROM conditions WHERE condition_type = 'Wind Speed'));


INSERT INTO stations_conditions (station_id, condition_id, condition_reading, wind_direction, date_refreshed) VALUES 
((SELECT station_id FROM stations WHERE station_code = '51211'), (SELECT condition_id FROM conditions WHERE condition_type = 'Swell Height'), 2.8, NULL, '2024-10-30 06:00:00'),
((SELECT station_id FROM stations WHERE station_code = '51211'), (SELECT condition_id FROM conditions WHERE condition_type = 'Swell Period'), 15.2, NULL, '2024-10-30 06:00:00'),
((SELECT station_id FROM stations WHERE station_code = 'PHHI'), (SELECT condition_id FROM conditions WHERE condition_type = 'Wind Speed'), 12.0, 'E', '2024-10-30 09:00:00'),
((SELECT station_id FROM stations WHERE station_code = 'SFOC1'), (SELECT condition_id FROM conditions WHERE condition_type = 'Wind Speed'), 5.0, 'W', '2024-10-30 09:00:00'),
((SELECT station_id FROM stations WHERE station_code = '1612366'), (SELECT condition_id FROM conditions WHERE condition_type = 'Tide Level'), 2.2, NULL, '2024-10-30 06:00:00');
