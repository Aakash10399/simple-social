CREATE TABLE `planner` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `interests` varchar(5000) NOT NULL,
  `locality` varchar(5000) NOT NULL,
  `city` varchar(5000) NOT NULL,
  `destination` varchar(5000) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;