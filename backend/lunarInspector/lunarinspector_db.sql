/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 100432
 Source Host           : localhost:3306
 Source Schema         : lunarinspector_db

 Target Server Type    : MySQL
 Target Server Version : 100432
 File Encoding         : 65001

 Date: 27/08/2024 20:54:20
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for lunar_images
-- ----------------------------
DROP TABLE IF EXISTS `lunar_images`;
CREATE TABLE `lunar_images`  (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'id of the image',
  `route` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'route to the img folder',
  `user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'user that upload de image',
  `lat` int NOT NULL COMMENT 'latitude',
  `lon` int NOT NULL COMMENT 'longitude',
  `uv` decimal(2, 2) NOT NULL COMMENT 'uv factor average last year',
  `polution` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'air quality average last year',
  `state` bit(1) NOT NULL COMMENT 'state of the image on the system',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 57 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
