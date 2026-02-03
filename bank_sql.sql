show databases;
create database bank_new;
use bank_new;
CREATE DATABASE bank_new;
USE bank_new;

-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    phone VARCHAR(15),
    account_no BIGINT UNIQUE,
    pin INT
);

-- Accounts table
CREATE TABLE accounts (
    account_no BIGINT PRIMARY KEY,
    account_type VARCHAR(20),
    balance DECIMAL(10,2)
);

-- Transactions table
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_no BIGINT,
    type VARCHAR(10),
    amount DECIMAL(10,2),
    date DATETIME
);
select * from users;
select * from transactions;
select * from accounts;