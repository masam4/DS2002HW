# DS 2002 HW Assignment 1

# PART 1

#1. List all countries in South America.
SELECT NAME FROM `country` WHERE CONTINENT = 'South America';

#2. Find the population of 'Germany'.
SELECT NAME, Population FROM `country` WHERE NAME = 'Germany';

#3. Retrieve all cities in the country 'Japan'.
SELECT city.name 
FROM city 
JOIN country ON city.CountryCode = country.Code 
WHERE country.name = 'Japan';

#4. Find the 3 most populated countries in the 'Africa' region.
SELECT name, Population 
FROM country 
WHERE Continent = 'Africa' 
ORDER BY Population DESC 
LIMIT 3;

#5. Retrieve the country and its life expectancy where the population is between 1 and 5 million.SELECT name from country where Population > 1000000 and Population < 5000000 order by population DESC;
SELECT name from country where Population > 1000000 and Population < 5000000 order by population DESC;

#6. List countries with an official language of 'French'.
SELECT name from country 
JOIN countrylanguage ON country.code = countrylanguage.CountryCode
WHERE countrylanguage.Language = "French" AND countrylanguage.IsOfficial = "T"

#7. Retrieve all album titles by the artist 'AC/DC'.
SELECT Title 
FROM Album
WHERE ArtistId = '1';

#8. Find the name and email of customers located in 'Brazil'.
SELECT FirstName, LastName, Email
FROM Customer
WHERE Country = 'Brazil';

#9. List all playlists in the database. (CHECK IF THIS IS CORRECT)
SELECT * FROM `Playlist` 

#10. Find the total number of tracks in the 'Rock' genre.
SELECT SUM(TrackId) as "Total 'Rock' Tracks" FROM `Track` WHERE GenreId = 1	

#11. List all employees who report to 'Nancy Edwards'.
SELECT FirstName, LastName, EmployeeId
FROM Employee
WHERE ReportsTo = 2

#12. Calculate the total sales per customer by summing the total amount in invoices.
SELECT SUM(Total) / 412 as "Total Sales Per Customer" 
FROM Invoice 

# PART 2

# Ensure that each table has a primary key and relationships where appropriate. 

CREATE TABLE Customer (
    CustomerId INT AUTO_INCREMENT PRIMARY KEY,
    PhoneNumber VARCHAR(15),
    LastName varchar(100),
    FirstName varchar(100),
    Email varchar(200)
);

CREATE TABLE Bouqet (
    FlowerId INT AUTO_INCREMENT PRIMARY KEY,
    FlowerType VARCHAR(100),
    Price DECIMAL(10, 2)
);

CREATE TABLE `Order` (
    OrderId INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT,
    FlowerId INT,
    Quantity INT,
    OrderDate DATE,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
    FOREIGN KEY (FlowerId) REFERENCES Bouqet(FlowerId)
);

# Insert at least 5 rows of data into each of the tables you created. 

INSERT INTO Customer (FirstName, LastName, Email, PhoneNumber) 
VALUES 
('Alice', 'Mary', 'alice.mary@example.com', '571-345-6789'),
('Jane', 'Murray', 'janemmmurray@example.com', '757-123-4563'),
('Daniel', 'Lee', 'danlee@example.com', '703-345-6789'),
('Robert', 'Xiaoh', 'robxia@example.com', '603-234-5673'),
('Celeste', 'Kurzt', 'celestekurzt@example.com', '267-567-8901');

INSERT INTO Bouqet (FlowerType, FlowerId, Price) 
VALUES 
('Rose', 1, 3),
('Tulip', 2, 2.5),
('Daisy', 3, 2),
('Sunflower', 4, 4),
('Orchid', 5, 6);

INSERT INTO `Order` (CustomerId, FlowerId, Quantity, OrderDate) 
VALUES 
(1, 5, 6, '2024-09-07'),
(2, 4, 8, '2024-09-06'),
(3, 1, 31, '2024-09-05'),
(4, 3, 11, '2024-09-04'),
(5, 2, 25, '2024-09-03');

# Write at least 3 queries to extract data from your new database. 

# Select flower that costs more than 5
SELECT FlowerType, Price FROM Bouqet WHERE Price > 5;

# Select flower which fits rose descriptor
SELECT FlowerType FROM Bouqet WHERE FlowerType = 'Rose';

# Show total quantity of flowers sold
SELECT FlowerId, SUM(Quantity) AS TotalQuantitySold
FROM `Order`
GROUP BY FlowerId
ORDER BY TotalQuantitySold DESC;

# Show list of customers who purchased bouqet after September 4th
SELECT FirstName, LastName, Email
FROM Customer
WHERE CustomerId IN (SELECT CustomerId FROM `Order` WHERE OrderDate > '2024-09-04');
