CREATE TABLE `simp_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `h1` varchar(5000) NOT NULL,
  `h2` varchar(5000) NOT NULL,
  `h3` varchar(5000) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf;