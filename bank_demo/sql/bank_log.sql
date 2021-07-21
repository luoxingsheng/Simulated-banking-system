/*
 Navicat Premium Data Transfer

 Source Server         : 本地连接
 Source Server Type    : MySQL
 Source Server Version : 80023
 Source Host           : localhost:3306
 Source Schema         : lxs

 Target Server Type    : MySQL
 Target Server Version : 80023
 File Encoding         : 65001

 Date: 21/07/2021 13:19:20
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for bank_log
-- ----------------------------
DROP TABLE IF EXISTS `bank_log`;
CREATE TABLE `bank_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `datetime` varchar(255) COLLATE utf8_bin NOT NULL DEFAULT '',
  `summary` varchar(255) COLLATE utf8_bin NOT NULL,
  `money` double(255,0) NOT NULL,
  `currency` varchar(255) COLLATE utf8_bin NOT NULL,
  `balance` double(255,0) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

SET FOREIGN_KEY_CHECKS = 1;
