-- Création de la base de données association_v1_db si elle n'existe pas déjà
CREATE DATABASE IF NOT EXISTS association_v1_db;

-- Utilisation de la base de données association_v1_db
USE association_v1_db;

-- Création des tables

-- Table 'user'
CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    name VARCHAR(100),
    address VARCHAR(200),
    postal_address VARCHAR(200),
    date_of_birth DATE,
    marital_status VARCHAR(50),
    is_admin BOOLEAN DEFAULT FALSE
);

-- Table 'news'
CREATE TABLE news (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    image_url VARCHAR(100),
    date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Table 'media'
CREATE TABLE media (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    file_url VARCHAR(200) NOT NULL,
    upload_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Table 'achievement'
CREATE TABLE achievement (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    site VARCHAR(150) NOT NULL,
    objectives TEXT NOT NULL,
    beneficiaries_kind VARCHAR(150) NOT NULL,
    beneficiaries_number INT NOT NULL,
    results_obtained TEXT NOT NULL
);

-- Table 'association'
CREATE TABLE association (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(128) NOT NULL
);

-- Table 'event'
CREATE TABLE event (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    date DATETIME NOT NULL
);

-- Table 'report'
CREATE TABLE report (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(128) NOT NULL,
    date DATETIME NOT NULL,
    content TEXT NOT NULL
);


-- Insertion de données aléatoires

-- Insertion dans 'user' avec 10 utilisateurs aléatoires
INSERT INTO user (username, password, email, name, address, postal_address, date_of_birth, marital_status, is_admin)
SELECT 
    CONCAT('user', id) AS username,
    MD5(RAND()) AS password,
    CONCAT('user', id, '@example.com') AS email,
    CONCAT('User', id) AS name,
    CONCAT('Address', id) AS address,
    CONCAT('Postal Address', id) AS postal_address,
    DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND() * 40) YEAR) AS date_of_birth,
    CASE FLOOR(RAND() * 3)
        WHEN 0 THEN 'Single'
        WHEN 1 THEN 'Married'
        ELSE 'Divorced'
    END AS marital_status,
    0 AS is_admin
FROM 
    (SELECT n + m * 10 + t * 100 AS id
     FROM (SELECT 0 AS n UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4) AS n
     JOIN (SELECT 0 AS m UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4) AS m
     JOIN (SELECT 0 AS t UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4) AS t
     ORDER BY RAND()
     LIMIT 10
    ) AS ids;


-- Insertion dans 'news' avec 10 articles aléatoires
INSERT INTO news (title, content, image_url, date)
SELECT 
    CONCAT('News Title ', id) AS title,
    CONCAT('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.') AS content,
    NULL AS image_url,
    NOW() - INTERVAL FLOOR(RAND() * 30) DAY AS date
FROM 
    (SELECT n + m * 10 + t * 100 AS id
     FROM (SELECT 0 AS n UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4) AS n
     JOIN (SELECT 0 AS m UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4) AS m
     JOIN (SELECT 0 AS t UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4) AS t
     ORDER BY RAND()
     LIMIT 10
    ) AS ids;


-- Insertion dans 'media' avec 10 entrées aléatoires
INSERT INTO media (title, description, file_url, upload_date)
SELECT 
    CONCAT('Media Title ', id) AS title,
    CONCAT('Description for media ', id) AS description,
    CONCAT('/path/to/file', id, '.pdf') AS file_url,
    NOW() - INTERVAL FLOOR(RAND() * 30) DAY AS upload_date
FROM 
    (SELECT n + m * 10 + t * 100 AS id
     FROM (SELECT 0 AS n UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4) AS n
     JOIN (SELECT 0 AS m UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4) AS m
     JOIN (SELECT 0 AS t UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4) AS t
     ORDER BY RAND()
     LIMIT 10
    ) AS ids;


-- Insertion dans 'achievement' avec 10 réalisations aléatoires
INSERT INTO achievement (name, start_date, end_date, site, objectives, beneficiaries_kind, beneficiaries_number, results_obtained)
SELECT 
    CONCAT('Achievement ', id) AS name,
    DATE_SUB(NOW(), INTERVAL FLOOR(RAND() * 5) YEAR) AS start_date,
    DATE_SUB(NOW(), INTERVAL FLOOR(RAND() * 2) YEAR) AS end_date,
    CONCAT('Site ', id) AS site,
    CONCAT('Objectives for achievement ', id) AS objectives,
    CASE FLOOR(RAND() * 3)
        WHEN 0 THEN 'Students'
        WHEN 1 THEN 'Employees'
        ELSE 'Community'
    END AS beneficiaries_kind,
    FLOOR(RAND() * 100) AS beneficiaries_number,
    CONCAT('Results obtained for achievement ', id) AS results_obtained
FROM 
    (SELECT n + m * 10 + t * 100 AS id
     FROM (SELECT 0 AS n UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4) AS n
     JOIN (SELECT 0 AS m UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4) AS m
     JOIN (SELECT 0 AS t UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4) AS t
     ORDER BY RAND()
     LIMIT 10
    ) AS ids;


-- Insertion dans 'association' avec 5 associations aléatoires
INSERT INTO association (name)
SELECT 
    CONCAT('Association ', id) AS name
FROM 
    (SELECT n + m * 10 AS id
     FROM (SELECT 0 AS n UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4) AS n
     JOIN (SELECT 0 AS m UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4) AS m
     ORDER BY RAND()
     LIMIT 5
    ) AS ids;


-- Insertion dans 'event' avec 5 événements aléatoires
INSERT INTO event (name, date)
SELECT 
    CONCAT('Event ', id) AS name,
    NOW() - INTERVAL FLOOR(RAND() * 30) DAY AS date
FROM 
    (SELECT n + m * 10 AS id
     FROM (SELECT 0 AS n UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4) AS n
     JOIN (SELECT 0 AS m UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4) AS m
     ORDER BY RAND()
     LIMIT 5
    ) AS ids;


-- Insertion dans 'report' avec 5 rapports aléatoires
INSERT INTO report (title, date, content)
SELECT 
    CONCAT('Report ', id) AS title,
    NOW() - INTERVAL FLOOR(RAND() * 30) DAY AS date,
    CONCAT('Content for report ', id) AS content
FROM 
    (SELECT n + m * 10 AS id
     FROM (SELECT 0 AS n UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4) AS n
     JOIN (SELECT 0 AS m UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4) AS m
     ORDER BY RAND()
     LIMIT 5
    ) AS ids;
