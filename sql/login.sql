CREATE DATABASE IF NOT EXISTS `login` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `login`;
-- create table for storing user data 
CREATE TABLE IF NOT EXISTS login (
id int(9) NOT NULL auto_increment,
name varchar(100) NOT NULL,
email varchar(100) NOT NULL,
password varchar(100) ,
PRIMARY KEY (id)
);
