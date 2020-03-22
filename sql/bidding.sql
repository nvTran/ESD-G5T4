CREATE DATABASE IF NOT EXISTS `bidding` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `bidding`;

CREATE TABLE if not exists bidItem 
(bidID int not null auto_increment,
productID varchar(100) not null,
sellerID varchar(10) not null,
buyerID varchar(10) not null,
bidDateTime timestamp not null,
bidStatus varchar(20) not null,
bidAmt float not null,
meetup varchar(100) not null,
CONSTRAINT bidItem_pk primary key(productID, bidID) ) ENGINE=INNODB DEFAULT charset=latin1;