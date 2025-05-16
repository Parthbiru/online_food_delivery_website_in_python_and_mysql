-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: May 16, 2025 at 01:05 PM
-- Server version: 8.3.0
-- PHP Version: 8.2.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `food_delivery`
--

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

DROP TABLE IF EXISTS `cart`;
CREATE TABLE IF NOT EXISTS `cart` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `item_id` int DEFAULT NULL,
  `quantity` int DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=71 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`id`, `user_id`, `item_id`, `quantity`) VALUES
(1, 2, 1, 1),
(2, 1, 1, 1),
(3, 1, 1, 1),
(4, 1, 2, 1),
(5, 1, 2, 1),
(6, 1, 2, 1),
(7, 1, 1, 1),
(8, 1, 1, 1),
(9, 1, 2, 1),
(10, 1, 2, 1),
(11, 1, 1, 1),
(12, 1, 1, 1),
(13, 1, 2, 1),
(14, 1, 2, 1),
(15, 1, 1, 1),
(16, 4, 3, 1),
(17, 4, 1, 1),
(18, 4, 1, 1),
(19, 4, 1, 1),
(53, 14, 3, 3);

-- --------------------------------------------------------

--
-- Table structure for table `items`
--

DROP TABLE IF EXISTS `items`;
CREATE TABLE IF NOT EXISTS `items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `price` int DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `description` text,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `items`
--

INSERT INTO `items` (`id`, `name`, `price`, `image`, `description`) VALUES
(11, 'pizza', 399, 'pepperoni.jpg', 'margarita'),
(4, 'khavsa', 50, 'Khavsa.jpg', 'ethythyryetutyiuui'),
(12, 'pop', 2344, 'delhi_travel-4813658_1920.jpg', 'dfgdfg'),
(13, '7 Chess pizza', 799, 'pepperoni.jpg', 'famose'),
(8, 'Spicy burger', 399, 'offer3.jpg', 'noveg'),
(6, 'vada pow', 30, 'maxresdefault.jpg', 'deep fried potato fritter'),
(7, 'Samosa', 50, '61050397.webp', ' Punjabi Samosa with super-flaky crust and delicious potato stuffing');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
CREATE TABLE IF NOT EXISTS `orders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `email` varchar(100) NOT NULL,
  `address` text NOT NULL,
  `city` varchar(50) NOT NULL,
  `state` varchar(50) NOT NULL,
  `pincode` varchar(10) NOT NULL,
  `delivery_instructions` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `payment_method` varchar(20) NOT NULL,
  `order_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` varchar(20) NOT NULL DEFAULT 'Pending',
  `subtotal` decimal(10,2) NOT NULL,
  `taxes` decimal(10,2) NOT NULL,
  `delivery_fee` decimal(10,2) NOT NULL,
  `total_amount` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `user_id`, `name`, `phone`, `email`, `address`, `city`, `state`, `pincode`, `delivery_instructions`, `payment_method`, `order_date`, `status`, `subtotal`, `taxes`, `delivery_fee`, `total_amount`) VALUES
(1, 15, 'lalu', '8866729338', 'guddi@gmail.com', 'weqsfrdew', 'navsari', 'gujrat', '396445', 'eqwrewfr', 'cod', '2025-05-15 12:47:51', 'Pending', 390.00, 20.00, 40.00, 450.00),
(2, 15, 'BEERU PARTH BALKRUSHNA', '8866729338', 'parth.biru8194@gmail.com', 'rstyrty', 'Navsari, Gujarat, India', 'gujrat', '396445', 'tyrtyrty', 'cod', '2025-05-15 12:48:25', 'Pending', 1200.00, 60.00, 40.00, 1300.00),
(3, 15, 'YESH TOPIWALA', '8866729338', 'hemanshi@gmail.com', 'efedfef', 'ewfredwfr', 'gujrat', '396445', 'efrweferwfe', 'cod', '2025-05-15 12:53:07', 'Pending', 550.00, 28.00, 40.00, 618.00),
(4, 13, 'BEERU PARTH BALKRUSHNA', '8866729338', 'hemanshi@gmail.com', 'ughjyji', 'navsari', 'ttyu', '396445', 'tyutyuty', 'cod', '2025-05-15 12:54:53', 'Pending', 300.00, 15.00, 40.00, 355.00),
(5, 13, 'BEERU PARTH BALKRUSHNA', '8866729338', 'parth.biru8194@gmail.com', 'wrwefrt', 'rewtertger', 'retert', '396445', 'reertgyretg', 'cod', '2025-05-15 13:19:10', 'Pending', 450.00, 22.00, 40.00, 512.00),
(6, 13, 'new', '8866729338', 'new@gmail.com', 'chapra', 'navsari', 'gujrat', '396445', 'near char rasta', 'cod', '2025-05-15 15:34:17', 'Pending', 1020.00, 51.00, 40.00, 1111.00),
(7, 13, 'BEERU PARTH BALKRUSHNA', '8866729338', 'guddi@gmail.com', 'chapra', 'surat', 'gujrat', '396445', 'bhoot mama', 'cod', '2025-05-15 16:03:13', 'Pending', 1200.00, 60.00, 40.00, 1300.00),
(8, 13, 'BEERU PARTH BALKRUSHNA', '8866729338', 'parth.biru8194@gmail.com', 'nvs', 'surat', 'gujrat', '396445', 'chapra ', 'cod', '2025-05-15 16:24:36', 'Pending', 120.00, 6.00, 40.00, 166.00),
(9, 13, 'BEERU PARTH BALKRUSHNA', '8866729338', 'sv@gmail.com', 'fgh', 'yfu', 'tyu', '396445', '', 'cod', '2025-05-15 16:34:13', 'Pending', 120.00, 6.00, 40.00, 166.00),
(10, 13, 'BEERU PARTH BALKRUSHNA', '8866729338', 'parth.biru8194@gmail.com', 'dsfgds', 'sdfgdfsg', 'fdgdfg', '396445', '', 'cod', '2025-05-15 16:41:00', 'Pending', 200.00, 10.00, 40.00, 250.00),
(11, 13, 'BEERU PARTH BALKRUSHNA', '8866729338', 'guddi@gmail.com', 'ghjughik', 'gfigui', 'ghfghk', '396445', 'kfghjk', 'cod', '2025-05-15 16:45:49', 'Pending', 50.00, 2.00, 40.00, 92.00),
(12, 13, 'nandu', '8866729338', 'guddi@gmail.com', 'ewerwfew', 'navsari', 'gujrat', '396445', 'sdfdfgdfg', 'cod', '2025-05-16 00:00:07', 'Pending', 798.00, 40.00, 40.00, 878.00),
(13, 13, 'BEERU PARTH BALKRUSHNA', '8866729338', 'hemanshi@gmail.com', 'chndan va', 'navsari', 'gujrat', '396445', 'gdfgdfg', 'cod', '2025-05-16 12:45:05', 'Pending', 399.00, 20.00, 40.00, 459.00),
(14, 13, 'sonu', '9999999999', 'guddi@gmail.com', 'dsfadsf', 'dsfdsf', 'sdfdsf', '396445', 'dsfdsfgdsfg', 'online', '2025-05-16 17:40:29', 'Pending', 2394.00, 120.00, 40.00, 2554.00);

-- --------------------------------------------------------

--
-- Table structure for table `order_items`
--

DROP TABLE IF EXISTS `order_items`;
CREATE TABLE IF NOT EXISTS `order_items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_id` int NOT NULL,
  `item_id` int NOT NULL,
  `quantity` int NOT NULL,
  `price` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `order_id` (`order_id`),
  KEY `item_id` (`item_id`)
) ENGINE=MyISAM AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `order_items`
--

INSERT INTO `order_items` (`id`, `order_id`, `item_id`, `quantity`, `price`) VALUES
(1, 1, 3, 2, 120.00),
(2, 1, 7, 3, 50.00),
(3, 2, 3, 10, 120.00),
(4, 3, 4, 11, 50.00),
(5, 4, 6, 10, 30.00),
(6, 5, 6, 15, 30.00),
(7, 6, 2, 1, 20.00),
(8, 6, 7, 20, 50.00),
(9, 7, 3, 10, 120.00),
(10, 8, 3, 1, 120.00),
(11, 9, 3, 1, 120.00),
(12, 10, 4, 4, 50.00),
(13, 11, 4, 1, 50.00),
(14, 12, 8, 2, 399.00),
(15, 13, 8, 1, 399.00),
(16, 14, 12, 1, 2344.00),
(17, 14, 4, 1, 50.00);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=MyISAM AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`) VALUES
(1, 'BEERU PARTH BALKRUSHNA', 'parth.biru8194@gmail.com', '123'),
(3, 'hemanshi tandel', 'hemanshi@gmail.com', '123'),
(4, 'sonu', 'sonu@gmail', '123'),
(6, 'lalu', 'lalu@gmaiyi.com', '123'),
(7, 'sonnu', 'sonnu@gmail.com', '123'),
(8, 'pop', 'pop@gmail.com', '123'),
(9, 'sim', 'sim@gmail.com', '123'),
(10, 'ss', 'ss@gmail.com', 'scrypt:32768:8:1$v9vTS7eQ77cqRHk7$b49e151b7d6c684ee647f790c57cacaeb939db073e2dba169935905390b264adfe'),
(11, 'kd', 'kd@gmail.com', 'scrypt:32768:8:1$o5d1fLfLDgaTQ3uA$6de39ca3c79311e2cfdbb26fa709170ff3b3a300c449d704f16a4bfddb5e40991b'),
(12, 'nn', 'nn@gmail.com', 'scrypt:32768:8:1$ZdWCLwGGM33eAz3J$b0aa3e1b6eb9062f027449058d93bb7788c6266161251a4cf195bd4edb996efc1e'),
(13, 'sv', 'sv@gmail.com', 'scrypt:32768:8:1$U4oleY0YKQsMxjTy$00be4aed61ab508df0963e899cc0862ca580a2a29bc5f6d6bb938382aec9deaa9fa622d345e1120891d087133a25d92393ebb8e25da1aeaa5fe1cd5d41dbec15'),
(14, 'sv', 'sagar@gmail.com', 'scrypt:32768:8:1$unBndY4rRFGVFRtN$ac5a9cf5c1db0e2817c481159eeafc7a85b897ba4920c9bf0f764f5066699341f14a9d3147e6dfb8701d2cb773c934ac5cfe7c3eaa01f2b951f9598bccf1fd8b'),
(16, 'biru', 'biru@gmail.com', 'scrypt:32768:8:1$5MmxbJh3hGgmnmvX$9cd8122e971d7dc52924a48f752f6415e4ff51d55671568b58219edc56150f460769ba5350c09fe900292eb4bdbbef3c83b7743a70200224f8f59703f4572c95');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
