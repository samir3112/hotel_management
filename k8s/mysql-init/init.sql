-- mysql-init/init.sql

CREATE DATABASE IF NOT EXISTS hotel_db;
USE hotel_db;

-- Drop tables if exist (optional, for fresh start)
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS rooms;
DROP TABLE IF EXISTS users;

-- Create tables
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(100),
  password VARCHAR(100)
);

CREATE TABLE rooms (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  description TEXT,
  price INT,
  image VARCHAR(255),
  facility TEXT
);

CREATE TABLE bookings (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  room_id INT,
  name VARCHAR(255),
  city VARCHAR(100),
  contact VARCHAR(20),
  check_in DATE,
  check_out DATE,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (room_id) REFERENCES rooms(id)
);

-- Insert initial data

INSERT INTO rooms (name, description, price, image, facility) VALUES
('Single Room', 'Perfect for solo travelers with essentials.', 1000, 'room1.jpg', 'Wi-Fi, Air Conditioning'),
('Single Room', 'Cozy and affordable, ideal for one person.', 1500, 'room2.jpg', 'Wi-Fi, TV, Air Conditioning'),
('Double Room', 'Spacious for two guests with comfort.', 2000, 'room3.jpg', 'Wi-Fi, TV, Air Conditioning, Breakfast'),
('Double Room', 'Modern design, best for couples.', 2400, 'room4.jpg', 'Wi-Fi, TV, Air Conditioning, Breakfast, Mini Fridge'),
('Duplex Room', 'Luxury duplex with lounge area.', 3000, 'room5.jpg', 'Wi-Fi, TV, Air Conditioning, Breakfast, Lounge Area, Mini Fridge'),
('Duplex Room', 'Top-tier duplex with private balcony.', 4000, 'room6.jpg', 'Wi-Fi, TV, Air Conditioning, Breakfast, Lounge Area, Mini Fridge, Private Balcony');

 
