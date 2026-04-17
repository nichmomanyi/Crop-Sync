CREATE TABLE countries (
    country_id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);
CREATE TABLE locations (
    location_id SERIAL PRIMARY KEY,
    country_id INT REFERENCES countries(country_id),
    town VARCHAR(100) NOT NULL,
    lat DECIMAL(10, 6),
    lon DECIMAL(10, 6),
    UNIQUE(country_id, town)
);
CREATE TABLE tpes (
    tpe_id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    stressors TEXT[]
);
CREATE TABLE weather (
    weather_id SERIAL PRIMARY KEY,
    location_id INT REFERENCES locations(location_id),
    year INT NOT NULL,
    month VARCHAR(20) NOT NULL,
    temperature DECIMAL(5, 2),
    humidity DECIMAL(5, 2),
    condition VARCHAR(100),
    rainfall DECIMAL(5, 2),
    UNIQUE(location_id, year, month)
);
CREATE TABLE crops (
    crop_id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);
CREATE TABLE varieties (
    variety_id SERIAL PRIMARY KEY,
    crop_id INT REFERENCES crops(crop_id),
    name VARCHAR(100) NOT NULL,
    UNIQUE(crop_id, name)
);
CREATE TABLE traits (
    trait_id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    trait_type VARCHAR(20) NOT NULL
);
CREATE TABLE variety_traits (
    variety_id INT REFERENCES varieties(variety_id),
    trait_id INT REFERENCES traits(trait_id),
    PRIMARY KEY(variety_id, trait_id)
);
--ML ready table, Joined all the tables together
CREATE TABLE cropsync_ml_data AS
WITH variety_location_performance AS (
    -- Join varieties, traits, and locations
    SELECT
        v.variety_id,
        v.name AS variety_name,
        c.name AS crop_name,
        t.name AS trait_name,
        t.trait_type,
        l.location_id,
        l.town,
        l.lat,
        l.lon,
        co.name AS country,
        w.temperature,
        w.humidity,
        w.rainfall,
        w.condition,
        w.month,
        w.year,
        tp.name AS tpe_name,
        tp.description AS tpe_description,
        tp.stressors,
        -- Placeholder for performance metrics (if available)
        NULL AS yield,
        NULL AS adoption_rate
    FROM
        varieties v
    JOIN
        crops c ON v.crop_id = c.crop_id
    JOIN
        variety_traits vt ON v.variety_id = vt.variety_id
    JOIN
        traits t ON vt.trait_id = t.trait_id
    JOIN
        locations l ON l.location_id IN (
            SELECT DISTINCT location_id FROM weather
        )
    JOIN
        countries co ON l.country_id = co.country_id
    JOIN
        weather w ON l.location_id = w.location_id
    LEFT JOIN
        tpes tp ON (
            -- Join with tpes based on environmental conditions
            -- This logic should be adjusted based on TPE classification rules.
            -- Example: Match TPE based on rainfall and temperature.
            CASE
                WHEN w.rainfall < 400 THEN tp.name = 'ARID'
                WHEN w.rainfall BETWEEN 400 AND 800 THEN tp.name = 'SEMI_ARID'
                WHEN w.rainfall BETWEEN 800 AND 1200 THEN tp.name = 'SUB_HUMID'
                WHEN w.rainfall > 1200 THEN tp.name = 'HUMID'
                ELSE tp.name = 'UNKNOWN'
            END
        )
)
SELECT * FROM variety_location_performance;
SELECT * FROM cropsync_ml_data;
