-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 17, 2023 at 05:17 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `blog`
--

-- --------------------------------------------------------

--
-- Table structure for table `posts`
--

CREATE TABLE `posts` (
  `sno` int(11) NOT NULL,
  `title` text NOT NULL,
  `slug` varchar(25) NOT NULL,
  `content` text NOT NULL,
  `date` datetime NOT NULL DEFAULT current_timestamp(),
  `img_file` varchar(25) NOT NULL,
  `tagline` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `posts`
--

INSERT INTO `posts` (`sno`, `title`, `slug`, `content`, `date`, `img_file`, `tagline`) VALUES
(1, 'Robert-AI', 'robert-AI', 'Robert-AI, an open-source project that uses natural language processing to perform tasks. Robert-AI comes with voice recognition, natural language processing, task automation, and customizability features, making it a powerful and customizable personal assistant. Using Robert-AI is simple; download the project from GitHub and install required libraries. Building your own personal assistant can be a fun and rewarding experience, and Robert-AI provides a great platform to achieve that.', '2023-03-17 19:30:24', 'robert.jpg', 'Own personal assistant using Python and explore the features of Robert-AI, an open-source project that uses natural language processing to perform tasks.'),
(2, 'Banking Portal', 'bank-portal', 'An open-source project on GitHub called the Banking Portal, created by Romil Arora, which provides a template for building a fully functional online banking portal using Python. The project includes features such as user authentication, account management, and transaction history, making it a powerful platform for building a banking portal. It is highly customizable, allowing users to add their own features and functionality. To use the Banking Portal, one can download the project from the GitHub repository and install the required libraries. Overall, the project provides a solid foundation for building a fully functional online banking portal using Python.', '2023-03-17 19:55:30', 'bank.jpg', 'Online Banking with the Banking Portal - The Python-based and Customizable.');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`sno`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `posts`
--
ALTER TABLE `posts`
  MODIFY `sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
