USE DATABASE bootcamp_rally;

-- 1. Create schema
CREATE SCHEMA IF NOT EXISTS racing;

-- 2. Teams table
DROP TABLE IF EXISTS bootcamp_rally.racing.teams;
CREATE TABLE bootcamp_rally.racing.teams (
team_id INTEGER AUTOINCREMENT PRIMARY KEY,
team_name STRING NOT NULL,
budget NUMBER(20,2) NOT NULL DEFAULT 0.00
);

-- 3. Cars table
DROP TABLE IF EXISTS bootcamp_rally.racing.cars;
CREATE TABLE bootcamp_rally.racing.cars (
car_id INTEGER AUTOINCREMENT PRIMARY KEY,
team_id INTEGER REFERENCES bootcamp_rally.racing.teams(team_id),
car_name STRING NOT NULL,
base_speed_kmh NUMBER(6,2) NOT NULL, -- average speed on track
handling NUMBER(5,2) NOT NULL, -- 0..1

reliability NUMBER(5,2) NOT NULL, -- 0..1 chance to not break
weight_kg INTEGER NOT NULL
);

-- 4. Team members table
DROP TABLE IF EXISTS bootcamp_rally.racing.team_members;
CREATE TABLE bootcamp_rally.racing.team_members (
member_id INTEGER AUTOINCREMENT PRIMARY KEY,
team_id INTEGER REFERENCES bootcamp_rally.racing.teams(team_id),
car_id INTEGER REFERENCES bootcamp_rally.racing.cars(car_id),
member_name STRING NOT NULL
);

-- 5. Races table
DROP TABLE IF EXISTS bootcamp_rally.racing.races;
CREATE TABLE IF NOT EXISTS bootcamp_rally.racing.races (
race_id INTEGER AUTOINCREMENT PRIMARY KEY,
race_name STRING,
distance_km NUMBER(8,2) NOT NULL,
fee_per_team NUMBER(12,2) NOT NULL,
race_date TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP
);

-- 6. Race results table (single track assumption)
DROP TABLE IF EXISTS bootcamp_rally.racing.race_results;
CREATE TABLE bootcamp_rally.racing.race_results (
result_id INTEGER AUTOINCREMENT PRIMARY KEY,

race_id INTEGER REFERENCES bootcamp_rally.racing.races(race_id),
car_id INTEGER REFERENCES bootcamp_rally.racing.cars(car_id),
team_id INTEGER REFERENCES bootcamp_rally.racing.teams(team_id),
member_id INTEGER REFERENCES bootcamp_rally.racing.team_members(member_id),
finished BOOLEAN,
time_seconds NUMBER(12,4),
position INTEGER,
prize_money NUMBER(12,2)
);

-- 7. Create example teams
INSERT INTO bootcamp_rally.racing.teams (team_name, budget) VALUES
('Invicta Racing', 10000),
( 'ART Grand Prix', 12000),
( 'Rodin Motorsport', 8000),
('AIX Racing', 9000);

-- 8. Create example cars
INSERT INTO bootcamp_rally.racing.cars (team_id, car_name, base_speed_kmh, handling,
reliability, weight_kg) VALUES
-- Team 1 cars
(1, 'Falcon F1', 160, 0.85, 0.95, 1200),
(1, 'Falcon II', 155, 0.83, 0.96, 1250),
-- Team 2 cars
(2, 'Comet Sprint', 158, 0.87, 0.92, 1180),
(2, 'Comet GT', 162, 0.89, 0.91, 1190),
-- Team 3 car

(3, 'Hornet Turbo', 150, 0.82, 0.90, 1300),
-- Team 4 cars
(4, 'AIX Speedster', 157, 0.84, 0.94, 1210),
(4, 'AIX Phantom', 152, 0.81, 0.93, 1240);

-- 9. Create example team members
-- Team 1
INSERT INTO bootcamp_rally.racing.team_members (team_id, car_id, member_name) VALUES
(1, 1, 'Alexey'),
(1, 2, 'Daniels');
-- Team 2
INSERT INTO bootcamp_rally.racing.team_members (team_id, car_id, member_name) VALUES
(2, 3, 'Boris'),
(2, 4, 'Maksims');
-- Team 3
INSERT INTO bootcamp_rally.racing.team_members (team_id, car_id, member_name) VALUES
(3, 5, 'Arturs');
-- Team 4
INSERT INTO bootcamp_rally.racing.team_members (team_id, car_id, member_name) VALUES
(4, 6, 'Eduards'),
(4, 7, 'Semjons');