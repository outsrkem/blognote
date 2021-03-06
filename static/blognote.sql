
SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for article
-- ----------------------------
DROP TABLE IF EXISTS `article`;
CREATE TABLE `article` (
  `articleid` int(11) NOT NULL AUTO_INCREMENT,
  `userid` int(11) NOT NULL,
  `type` tinyint(255) NOT NULL,
  `headline` varchar(100) NOT NULL,
  `content` mediumtext,
  `thumbnail` varchar(30) DEFAULT NULL,
  `credit` int(11) DEFAULT '0',
  `readcount` int(11) DEFAULT '0',
  `replycount` int(11) DEFAULT '0',
  `recmmended` tinyint(255) DEFAULT '0',
  `hidden` tinyint(255) DEFAULT '0',
  `drafted` tinyint(255) DEFAULT '0',
  `checked` tinyint(255) DEFAULT '1',
  `createtime` datetime DEFAULT NULL,
  `updatetime` datetime DEFAULT NULL,
  PRIMARY KEY (`articleid`),
  KEY `userid` (`userid`),
  CONSTRAINT `article_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `users` (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='文章表';

-- ----------------------------
-- Records of article
-- ----------------------------

-- ----------------------------
-- Table structure for comment
-- ----------------------------
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment` (
  `commentid` int(11) NOT NULL,
  `userid` int(11) NOT NULL,
  `articleid` int(11) NOT NULL,
  `content` text,
  `ipaddr` varchar(30) DEFAULT NULL,
  `replyid` int(11) DEFAULT NULL,
  `agreecount` int(11) DEFAULT '0',
  `opposecount` int(11) DEFAULT '0',
  `hidden` tinyint(255) DEFAULT '0',
  `createtime` datetime DEFAULT NULL,
  `updatetime` datetime DEFAULT NULL,
  PRIMARY KEY (`commentid`),
  KEY `userid` (`userid`),
  KEY `articleid` (`articleid`),
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `users` (`userid`),
  CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`articleid`) REFERENCES `article` (`articleid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='评论表';

-- ----------------------------
-- Records of comment
-- ----------------------------

-- ----------------------------
-- Table structure for credit
-- ----------------------------
DROP TABLE IF EXISTS `credit`;
CREATE TABLE `credit` (
  `creditid` int(11) NOT NULL AUTO_INCREMENT,
  `userid` int(11) NOT NULL,
  `category` varchar(10) DEFAULT NULL,
  `target` int(11) DEFAULT NULL,
  `credit` int(11) DEFAULT NULL,
  `createtime` datetime DEFAULT NULL,
  `updatetime` datetime DEFAULT NULL,
  PRIMARY KEY (`creditid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='积分表';

-- ----------------------------
-- Records of credit
-- ----------------------------

-- ----------------------------
-- Table structure for favorite
-- ----------------------------
DROP TABLE IF EXISTS `favorite`;
CREATE TABLE `favorite` (
  `favorite` int(11) NOT NULL AUTO_INCREMENT,
  `articleid` int(11) NOT NULL,
  `userid` int(11) NOT NULL,
  `canceled` tinyint(255) DEFAULT '0',
  `createtime` datetime DEFAULT NULL,
  `updatetime` datetime DEFAULT NULL,
  PRIMARY KEY (`favorite`),
  KEY `articleid` (`articleid`),
  KEY `userid` (`userid`),
  CONSTRAINT `favorite_ibfk_1` FOREIGN KEY (`articleid`) REFERENCES `article` (`articleid`),
  CONSTRAINT `favorite_ibfk_2` FOREIGN KEY (`userid`) REFERENCES `users` (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='收藏表';

-- ----------------------------
-- Records of favorite
-- ----------------------------

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `userid` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(32) NOT NULL,
  `nickname` varchar(30) DEFAULT NULL,
  `avatar` varchar(255) DEFAULT NULL,
  `qq` varchar(15) DEFAULT NULL,
  `role` varchar(10) DEFAULT NULL,
  `credit` int(11) DEFAULT '50',
  `createtime` datetime DEFAULT CURRENT_TIMESTAMP,
  `updatetime` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- ----------------------------
-- Records of users
-- ----------------------------


INSERT INTO `blognote`.`users` (`username`, `password`, `nickname`, `avatar`, `qq`, `role`, `credit`) VALUES ('www.baidu.com', '123456!@#$%', NULL, NULL, NULL, 'user', '5');
INSERT INTO `blognote`.`users` (`username`, `password`, `nickname`, `avatar`, `qq`, `role`, `credit`) VALUES ('yong.com', '123456!@#$%', NULL, NULL, NULL, 'user', '5');
INSERT INTO `blognote`.`users` (`username`, `password`, `nickname`, `avatar`, `qq`, `role`, `credit`) VALUES ('www.baidu.com', '123456!@#$%', NULL, NULL, NULL, 'user', '5');
INSERT INTO `blognote`.`users` (`username`, `password`, `nickname`, `avatar`, `qq`, `role`, `credit`) VALUES ('yong5.com', '123456!@#$%', NULL, NULL, NULL, 'user', '5');
INSERT INTO `blognote`.`users` (`username`, `password`, `nickname`, `avatar`, `qq`, `role`, `credit`) VALUES ('yong5.com', '123456!@#$%', NULL, NULL, NULL, 'user', '5');
INSERT INTO `blognote`.`users` (`username`, `password`, `nickname`, `avatar`, `qq`, `role`, `credit`) VALUES ('yong5.com', '123456!@#$%', NULL, NULL, NULL, 'user', '5');
INSERT INTO `blognote`.`users` (`username`, `password`, `nickname`, `avatar`, `qq`, `role`, `credit`) VALUES ('we', 'we', 'we', 'we', 'we', 'admin', '123');

















