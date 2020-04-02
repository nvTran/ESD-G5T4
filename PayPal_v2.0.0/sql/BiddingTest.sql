SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `transaction`
--
CREATE DATABASE IF NOT EXISTS `` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `transaction`;

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `transaction`;
CREATE TABLE IF NOT EXISTS `transaction` (
  `productID` char(13) NOT NULL,
  `bidID` char(13) NOT NULL,
  `Currency` varchar(64) NOT NULL,
  `bidAmt` decimal(10,2) NOT NULL,
  `Quantity` int(11) DEFAULT NULL,
  PRIMARY KEY (`bidID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `product`
--

INSERT INTO `transaction` (`productID`, `bidID`, `Currency`, `bidAmt`, `Quantity`) VALUES
('0001', '0001', '10', 2),
('0002', '0002', '12', 1),
('0003', '0003', '14', 3),
('0004', '0004', '123', 1),
('0005', '0005', '121', 1),
('0006', '0006', '44', 1),
('0007', '0007', '51', 2),
('0008', '0008', '12', 5),
('0009', '0009', '31', 1);

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
