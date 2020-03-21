CREATE DATABASE IF NOT EXISTS `listing` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `listing`;

CREATE TABLE if not exists postItem 
(productID varchar(100) not null,
userID varchar(10) not null,
productName varchar(100) not null,
productType varchar(20) not null,
productDesc varchar(500) default null,
meetup varchar(100) not null,
CONSTRAINT postItem_pk primary key(productID, userID) ) ENGINE=INNODB DEFAULT charset=latin1;