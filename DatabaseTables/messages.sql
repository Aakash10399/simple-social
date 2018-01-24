CREATE TABLE `messages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `recipient` varchar(1000) NOT NULL,
  `sender` varchar(1000) NOT NULL,
  `message` varchar(5000) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;