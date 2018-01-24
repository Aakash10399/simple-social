CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(500) NOT NULL,
  `username` varchar(500) NOT NULL,
  `password` varchar(500) NOT NULL,
  `email` varchar(50) NOT NULL,
  `mobile` varchar(50) NOT NULL,
  `website` varchar(500) NOT NULL DEFAULT 'https://yourwebsitenamehere.com/gotosettings',
  `description` varchar(500) NOT NULL,
  `subs` varchar(5000) NOT NULL,
  `interests` varchar(5000) NOT NULL,
  `notifications` varchar(5000) NOT NULL,
  `notfuser` varchar(1000) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8;