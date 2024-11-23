create database pet_shop_db;
use pet_shop_db;
CREATE TABLE petdetails (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    breed VARCHAR(100),
    age INT,
    owner_email VARCHAR(100)
);
INSERT INTO petdetails (id, name, breed, age, owner_email)
VALUES
(1, 'Bella', 'Labrador', 3, 'owner1@example.com'),
(2, 'Max', 'Bulldog', 5, 'owner2@example.com'),
(3, 'Charlie', 'Beagle', 2, 'owner3@example.com'),
(4, 'Molly', 'Poodle', 4, 'owner4@example.com'),
(5, 'Rocky', 'German Shepherd', 6, 'owner5@example.com');
select * from  petdetails;