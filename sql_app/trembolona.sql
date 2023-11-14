CREATE DATABASE IF NOT EXISTS trembolona;

USE trembolona;

DROP TABLE IF EXISTS `trembolona`.`plan`;

CREATE TABLE `trembolona`.`plan` (
  `plan_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(20) NOT NULL,
  `value` FLOAT NOT NULL,
  `description` VARCHAR(200) NULL,
  PRIMARY KEY (`plan_id`));

DROP TABLE IF EXISTS `trembolona`.`member`;

CREATE TABLE `trembolona`.`member` (
  `member_id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(20) NULL,
  `last_name` VARCHAR(20) NULL,
  `email` VARCHAR(50) NOT NULL,
  `plan_id` INT NOT NULL,
  PRIMARY KEY (`member_id`),
  FOREIGN KEY (`plan_id`) REFERENCES plan(plan_id));