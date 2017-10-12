-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Oct 12, 2017 at 02:57 AM
-- Server version: 5.7.19-0ubuntu0.16.04.1
-- PHP Version: 7.0.22-0ubuntu0.16.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `media`
--

-- --------------------------------------------------------

--
-- Table structure for table `genre`
--

CREATE TABLE `genre` (
  `genre_id` int(11) NOT NULL,
  `genre_name` varchar(500) NOT NULL,
  `genre_url_keyword` varchar(500) NOT NULL,
  `source_site` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `signedband`
--

CREATE TABLE `signedband` (
  `p_id` int(11) NOT NULL,
  `ranking` int(11) NOT NULL,
  `last_ranking` int(11) NOT NULL,
  `image_link` text NOT NULL,
  `name` varchar(500) NOT NULL,
  `song_artist_name` varchar(500) NOT NULL,
  `artist_page_link` text NOT NULL,
  `genre_id` int(11) NOT NULL,
  `rank_date` varchar(100) NOT NULL,
  `source_site` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `song`
--

CREATE TABLE `song` (
  `p_id` int(11) NOT NULL,
  `ranking` int(11) NOT NULL,
  `last_ranking` int(11) NOT NULL,
  `image_link` text NOT NULL,
  `name` varchar(255) NOT NULL,
  `song_artist_name` varchar(500) NOT NULL,
  `artist_page_link` text NOT NULL,
  `genre_id` int(11) NOT NULL,
  `rank_date` varchar(100) NOT NULL,
  `source_site` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `unsignedband`
--

CREATE TABLE `unsignedband` (
  `p_id` int(11) NOT NULL,
  `ranking` int(11) NOT NULL,
  `last_ranking` int(11) NOT NULL,
  `image_link` text NOT NULL,
  `name` varchar(500) NOT NULL,
  `song_artist_name` varchar(500) NOT NULL,
  `artist_page_link` text NOT NULL,
  `genre_id` int(11) NOT NULL,
  `rank_date` varchar(100) NOT NULL,
  `source_site` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `genre`
--
ALTER TABLE `genre`
  ADD PRIMARY KEY (`genre_id`);

--
-- Indexes for table `signedband`
--
ALTER TABLE `signedband`
  ADD PRIMARY KEY (`p_id`);

--
-- Indexes for table `song`
--
ALTER TABLE `song`
  ADD PRIMARY KEY (`p_id`);

--
-- Indexes for table `unsignedband`
--
ALTER TABLE `unsignedband`
  ADD PRIMARY KEY (`p_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `genre`
--
ALTER TABLE `genre`
  MODIFY `genre_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=146;
--
-- AUTO_INCREMENT for table `signedband`
--
ALTER TABLE `signedband`
  MODIFY `p_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `song`
--
ALTER TABLE `song`
  MODIFY `p_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=47318;
--
-- AUTO_INCREMENT for table `unsignedband`
--
ALTER TABLE `unsignedband`
  MODIFY `p_id` int(11) NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
