/*
 Navicat Premium Data Transfer

 Source Server         : 172.17.0.1_3306
 Source Server Type    : MySQL
 Source Server Version : 80039 (8.0.39)
 Source Host           : 172.17.0.1:3306
 Source Schema         : estate_datamart

 Target Server Type    : MySQL
 Target Server Version : 80039 (8.0.39)
 File Encoding         : 65001

 Date: 10/12/2024 09:20:53
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for agrregate_address
-- ----------------------------
DROP TABLE IF EXISTS `agrregate_address`;
CREATE TABLE `agrregate_address` (
  `districts_sk` bigint DEFAULT NULL,
  `districts_name` varchar(255) DEFAULT NULL,
  `province_sk` bigint DEFAULT NULL,
  `province_name` varchar(255) DEFAULT NULL,
  `average_district` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of agrregate_address
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for agrregate_address_temp
-- ----------------------------
DROP TABLE IF EXISTS `agrregate_address_temp`;
CREATE TABLE `agrregate_address_temp` (
  `districts_sk` bigint DEFAULT NULL,
  `districts_name` varchar(255) DEFAULT NULL,
  `province_sk` bigint DEFAULT NULL,
  `province_name` varchar(255) DEFAULT NULL,
  `average_district` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of agrregate_address_temp
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for agrregate_plot
-- ----------------------------
DROP TABLE IF EXISTS `agrregate_plot`;
CREATE TABLE `agrregate_plot` (
  `area` varchar(255) DEFAULT NULL,
  `column_name` double DEFAULT NULL,
  `count` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of agrregate_plot
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for agrregate_plot_temp
-- ----------------------------
DROP TABLE IF EXISTS `agrregate_plot_temp`;
CREATE TABLE `agrregate_plot_temp` (
  `area` varchar(255) DEFAULT NULL,
  `column_name` double DEFAULT NULL,
  `count` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of agrregate_plot_temp
-- ----------------------------
BEGIN;
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
