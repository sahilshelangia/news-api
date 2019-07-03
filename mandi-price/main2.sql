-- phpMyAdmin SQL Dump
-- version 4.6.6deb4
-- https://www.phpmyadmin.net/
--
-- Host: db757077410.db.1and1.com
-- Generation Time: Dec 31, 2018 at 02:04 PM
-- Server version: 5.5.60-0+deb7u1-log
-- PHP Version: 7.0.33-0+deb9u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db757077410`
--

-- --------------------------------------------------------

--
-- Table structure for table `main2`
--

CREATE TABLE `main2` (
  `arrival` date NOT NULL DEFAULT '0000-00-00',
  `district` varchar(30) COLLATE latin1_general_ci NOT NULL DEFAULT '',
  `market` varchar(40) COLLATE latin1_general_ci NOT NULL DEFAULT '',
  `commodity` varchar(40) COLLATE latin1_general_ci NOT NULL DEFAULT '',
  `variety` varchar(30) COLLATE latin1_general_ci DEFAULT NULL,
  `grade` varchar(20) COLLATE latin1_general_ci DEFAULT NULL,
  `state` varchar(25) COLLATE latin1_general_ci DEFAULT NULL,
  `minP` int(11) DEFAULT NULL,
  `maxP` int(11) DEFAULT NULL,
  `modP` int(11) DEFAULT NULL,
  `tonnage` float DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

--
-- Dumping data for table `main2`
--

INSERT INTO `main2` (`arrival`, `district`, `market`, `commodity`, `variety`, `grade`, `state`, `minP`, `maxP`, `modP`, `tonnage`) VALUES
('2018-12-31', 'Mumbai', 'Mumbai', 'Black Gram Dal (Urd Dal)', 'Other', 'FAQ', NULL, 5300, 7300, 5800, NULL),
('2018-12-31', 'Mangalore(Dakshin Kannad)', 'Mangalore', 'Black pepper', 'Malabar', 'FAQ', NULL, 22000, 34000, 30000, NULL),
('2018-12-31', 'Karwar(Uttar Kannad)', 'Siddapur', 'Black pepper', 'Malabar', 'FAQ', NULL, 33369, 33429, 33429, NULL),
('2018-12-31', 'Karwar(Uttar Kannad)', 'Yellapur', 'Black pepper', 'Other', 'FAQ', NULL, 31490, 32394, 32098, NULL),
('2018-12-31', 'Kheda', 'Nadiyad(Piplag)', 'Bottle gourd', 'Bottle Gourd', 'FAQ', NULL, 1000, 1200, 1100, NULL),
('2018-12-31', 'Aurangabad', 'Aurangabad', 'Bottle gourd', 'Other', 'FAQ', NULL, 500, 1000, 750, NULL),
('2018-12-31', 'Mumbai', 'Mumbai', 'Bottle gourd', 'Other', 'FAQ', NULL, 1600, 2000, 1800, NULL),
('2018-12-31', 'Pune', 'Pune(Hadapsar)', 'Bottle gourd', 'Other', 'FAQ', NULL, 700, 2000, 1500, NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `main2`
--
ALTER TABLE `main2`
  ADD PRIMARY KEY (`commodity`,`district`,`market`,`arrival`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
