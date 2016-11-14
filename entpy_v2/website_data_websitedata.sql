-- phpMyAdmin SQL Dump
-- version 3.3.9
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Nov 14, 2016 at 04:24 
-- Server version: 5.5.8
-- PHP Version: 5.3.5

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `ev2_sandbox`
--

-- --------------------------------------------------------

--
-- Table structure for table `website_data_websitedata`
--

CREATE TABLE IF NOT EXISTS `website_data_websitedata` (
  `id_website_data` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(500) NOT NULL,
  `val` longtext,
  `site_id` int(11) NOT NULL,
  PRIMARY KEY (`id_website_data`),
  KEY `website_data_websitedata_site_id_c9085277_fk_django_site_id` (`site_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=48 ;

--
-- Dumping data for table `website_data_websitedata`
--

INSERT INTO `website_data_websitedata` (`id_website_data`, `key`, `val`, `site_id`) VALUES
(4, 'classic_index_title', 'Lorem <strong>ipsum</strong> dolor sit amet', 1),
(5, 'classic_index_subtitle', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit', 1),
(6, 'classic_index_first_content', '<div class="col-md-4">\r\n					<div class="feature-left">\r\n						<div>\r\n							<h3>Titolo1</h3>\r\n							<p>Facilis ipsum reprehenderit nemo molestias. Aut cum mollitia reprehenderit.</p>\r\n						</div>\r\n					</div>\r\n\r\n				</div>\r\n				<div class="col-md-4">\r\n					<div class="feature-left">\r\n						<div>\r\n							<h3>Titolo2</h3>\r\n							<p>Facilis ipsum reprehenderit nemo molestias. Aut cum mollitia reprehenderit.</p>\r\n						</div>\r\n					</div>\r\n				</div>\r\n				<div class="col-md-4">\r\n					<div class="feature-left">\r\n						<div>\r\n							<h3>Titolo3</h3>\r\n							<p>Facilis ipsum reprehenderit nemo molestias. Aut cum mollitia reprehenderit.</p>\r\n						</div>\r\n					</div>\r\n				</div>', 1),
(7, 'classic_index_section_one_title', 'Titolo sezione1', 1),
(8, 'classic_index_section_one_content', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque ut lectus vestibulum, fringilla tellus in, lacinia ligula. Vivamus id odio maximus, semper justo suscipit, convallis diam.', 1),
(9, 'classic_index_second_content', '<div class="col-md-4">\r\n					<div class="feature-text">\r\n						<h3><span class="number">01.</span> Titolo1</h3>\r\n						<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque ut lectus vestibulum, fringilla tellus in, lacinia ligula. Vivamus id odio maximus, semper justo suscipit, convallis diam.</p>\r\n					</div>\r\n				</div>\r\n				<div class="col-md-4">\r\n					<div class="feature-text">\r\n						<h3><span class="number">02.</span> Titolo2</h3>\r\n						<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque ut lectus vestibulum, fringilla tellus in, lacinia ligula. Vivamus id odio maximus, semper justo suscipit, convallis diam.</p>\r\n					</div>\r\n				</div>\r\n				<div class="col-md-4">\r\n					<div class="feature-text">\r\n						<h3><span class="number">03.</span> Titolo3</h3>\r\n						<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque ut lectus vestibulum, fringilla tellus in, lacinia ligula. Vivamus id odio maximus, semper justo suscipit, convallis diam.</p>\r\n					</div>\r\n				</div>', 1),
(10, 'classic_index_section_two_title', 'Titolo sezione2', 1),
(11, 'classic_index_section_two_content', 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit est facilis maiores, perspiciatis accusamus asperiores sint consequuntur debitis.', 1),
(18, 'classic_about_title', 'Chi <strong>Siamo</strong>', 1),
(19, 'classic_about_subtitle', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit', 1),
(20, 'classic_about_section_one_title', 'Titolo sezione1', 1),
(21, 'classic_about_section_one_content', 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit est facilis maiores, perspiciatis accusamus asperiores sint consequuntur debitis.', 1),
(22, 'classic_about_section_two_title', 'Titolo paragrafo1', 1),
(23, 'classic_about_section_two_content_one', 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Aut rerum perspiciatis, debitis pariatur atque vitae sed blanditiis nobis sint, reprehenderit quas, natus corrupti! Ipsum cum possimus corporis aut architecto! Delectus enim adipisci quidem possimus voluptates! Aut ut aliquid molestias laudantium.', 1),
(24, 'classic_about_section_two_content_two', 'Lorem ipsum dolor sit amet, consectetur adipisicing elit.', 1),
(25, 'classic_services_title', 'I Nostri servizi', 1),
(26, 'classic_services_subtitle', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit', 1),
(27, 'classic_services_section_one_title', 'Cosa Facciamo', 1),
(28, 'classic_services_section_one_content', 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit est facilis maiores, perspiciatis accusamus asperiores sint consequuntur debitis.', 1),
(29, 'classic_services_blocks', '<div class="col-md-4 col-sm-4">\r\n					<div class="services animate-box">\r\n						<h3>Titolo blocco1</h3>\r\n						<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit est facilis maiores, perspiciatis accusamus asperiores sint consequuntur debitis.</p>\r\n					</div>\r\n				</div>\r\n				<div class="col-md-4 col-sm-4">\r\n					<div class="services animate-box">\r\n						<h3>Titolo blocco2</h3>\r\n						<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit est facilis maiores, perspiciatis accusamus asperiores sint consequuntur debitis.</p>\r\n					</div>\r\n				</div>\r\n				<div class="col-md-4 col-sm-4">\r\n					<div class="services animate-box">\r\n						<h3>Titolo blocco3</h3>\r\n						<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit est facilis maiores, perspiciatis accusamus asperiores sint consequuntur debitis.</p>\r\n					</div>\r\n				</div>\r\n				<div class="col-md-4 col-sm-4">\r\n					<div class="services animate-box">\r\n						<h3>Titolo blocco4</h3>\r\n						<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit est facilis maiores, perspiciatis accusamus asperiores sint consequuntur debitis.</p>\r\n					</div>\r\n				</div>\r\n				<div class="col-md-4 col-sm-4">\r\n					<div class="services animate-box">\r\n						<h3>Titolo blocco5</h3>\r\n						<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit est facilis maiores, perspiciatis accusamus asperiores sint consequuntur debitis.</p>\r\n					</div>\r\n				</div>\r\n				<div class="col-md-4 col-sm-4">\r\n					<div class="services animate-box">\r\n						<h3>Titolo blocco6</h3>\r\n						<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit est facilis maiores, perspiciatis accusamus asperiores sint consequuntur debitis.</p>\r\n					</div>\r\n				</div>', 1),
(30, 'classic_services_first_service_title', 'Titolo paragrafo1', 1),
(31, 'classic_services_first_service_content', 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Totam quae modi earum eligendi eaque quis laudantium aperiam sunt atque recusandae, fugiat veritatis repellendus incidunt nostrum voluptatibus. Eveniet ex magnam repellat sunt molestiae, quibusdam culpa dignissimos recusandae voluptatum necessitatibus provident commodi?', 1),
(32, 'classic_services_first_service_list', '<ul>\r\n						<li>Nome servizio1</li>\r\n						<li>Nome servizio2</li>\r\n						<li>Nome servizio3</li>\r\n						<li>Nome servizio4</li>\r\n					</ul>', 1),
(33, 'classic_services_second_service_title', 'Titolo paragrafo2', 1),
(34, 'classic_services_second_service_content', 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Totam quae modi earum eligendi eaque quis laudantium aperiam sunt atque recusandae, fugiat veritatis repellendus incidunt nostrum voluptatibus. Eveniet ex magnam repellat sunt molestiae, quibusdam culpa dignissimos recusandae voluptatum necessitatibus provident commodi?', 1),
(35, 'classic_services_second_service_list', '<ul>\r\n						<li>Nome servizio5</li>\r\n						<li>Nome servizio6</li>\r\n						<li>Nome servizio7</li>\r\n						<li>Nome servizio8</li>\r\n					</ul>', 1),
(36, 'classic_contacts_title', 'Contatti', 1),
(37, 'classic_contacts_subtitle', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit', 1),
(38, 'classic_contacts_section_one_title', 'Contatti', 1),
(39, 'classic_contacts_section_one_content', 'In una terra lontana, dietro le montagne Parole, lontani dalle terre di Vocalia e Consonantia, vivono i testi casuali. Vivono isolati nella cittadina di Lettere, sulle coste del Semantico, un immenso oceano linguistico. Un piccolo ruscello chiamato Devoto Oli attraversa quei luoghi, rifornendoli di tutte le regolalie di cui hanno bisogno.', 1),
(40, 'classic_contacts_address1', 'Indirizzo del negozio', 1),
(41, 'classic_contacts_phone1', '+39 123456789', 1),
(42, 'classic_contacts_email1', 'tuaemail@mail.com', 1),
(43, 'classic_contacts_timetables1', 'Lunedì-Venerdì 9.00-19.00', 1),
(44, 'classic_contacts_section_one_maps_position', '45.0711813,7.6850388', 1),
(45, 'classic_base_twitter_page_url', '#', 1),
(46, 'classic_base_facebook_page_url', '#', 1),
(47, 'classic_base_site_name', 'Classico', 1);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `website_data_websitedata`
--
ALTER TABLE `website_data_websitedata`
  ADD CONSTRAINT `website_data_websitedata_site_id_c9085277_fk_django_site_id` FOREIGN KEY (`site_id`) REFERENCES `django_site` (`id`);
