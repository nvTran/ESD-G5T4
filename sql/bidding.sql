CREATE DATABASE IF NOT EXISTS `bidding` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `bidding`;

CREATE TABLE if not exists bidItem 
(productID varchar(100) not null,
userID1 varchar(10) not null,
userID2 varchar(10) not null,
bidDateTime timestamp not null,
bidStatus varchar(20) not null,
bidAmt float not null,
meetup varchar(100) not null,
CONSTRAINT bidItem_pk primary key(productID, userID1, userID2) ) ENGINE=INNODB DEFAULT charset=latin1;