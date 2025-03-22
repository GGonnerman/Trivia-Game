-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema trivia
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `trivia` ;

-- -----------------------------------------------------
-- Schema trivia
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `trivia` DEFAULT CHARACTER SET utf8mb4 ;
SHOW WARNINGS;
USE `trivia` ;

-- -----------------------------------------------------
-- Table `User`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `User` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `User` (
  `idUser` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(50) NOT NULL,
  `password` BINARY(60) NOT NULL,
  `created_at` DATETIME NOT NULL,
  PRIMARY KEY (`idUser`),
  UNIQUE INDEX `idUser_UNIQUE` (`idUser` ASC) VISIBLE,
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `CustomGame`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `CustomGame` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `CustomGame` (
  `idCustomGame` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `User_idUser` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`idCustomGame`),
  UNIQUE INDEX `idCustomGame_UNIQUE` (`idCustomGame` ASC) VISIBLE,
  INDEX `fk_CustomGame_User_idx` (`User_idUser` ASC) VISIBLE,
  CONSTRAINT `fk_CustomGame_User`
    FOREIGN KEY (`User_idUser`)
    REFERENCES `User` (`idUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `Season`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Season` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `Season` (
  `idSeason` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `season_number` SMALLINT UNSIGNED NULL,
  PRIMARY KEY (`idSeason`),
  UNIQUE INDEX `idSeason_UNIQUE` (`idSeason` ASC) VISIBLE)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `Episode`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Episode` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `Episode` (
  `idEpisode` INT UNSIGNED NOT NULL,
  `air_date` DATE NOT NULL,
  `Season_idSeason` INT UNSIGNED NOT NULL,
  `episode_number` SMALLINT UNSIGNED NULL,
  PRIMARY KEY (`idEpisode`),
  INDEX `fk_Episode_Season1_idx` (`Season_idSeason` ASC) VISIBLE,
  CONSTRAINT `fk_Episode_Season1`
    FOREIGN KEY (`Season_idSeason`)
    REFERENCES `Season` (`idSeason`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `Category`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Category` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `Category` (
  `idCategory` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `Episode_idEpisode` INT UNSIGNED NOT NULL,
  `round` TINYINT UNSIGNED NOT NULL,
  PRIMARY KEY (`idCategory`),
  UNIQUE INDEX `idCategory_UNIQUE` (`idCategory` ASC) VISIBLE,
  INDEX `fk_Category_Episode1_idx` (`Episode_idEpisode` ASC) VISIBLE,
  CONSTRAINT `fk_Category_Episode1`
    FOREIGN KEY (`Episode_idEpisode`)
    REFERENCES `Episode` (`idEpisode`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `Question`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Question` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `Question` (
  `idQuestion` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `clue_value` SMALLINT UNSIGNED NOT NULL,
  `comment` VARCHAR(250) NULL,
  `question` VARCHAR(250) NOT NULL,
  `answer` VARCHAR(250) NOT NULL,
  `Category_idCategory` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`idQuestion`),
  UNIQUE INDEX `idQuestion_UNIQUE` (`idQuestion` ASC) VISIBLE,
  INDEX `fk_Question_Category1_idx` (`Category_idCategory` ASC) VISIBLE,
  CONSTRAINT `fk_Question_Category1`
    FOREIGN KEY (`Category_idCategory`)
    REFERENCES `Category` (`idCategory`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `CustomGame_has_Category`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `CustomGame_has_Category` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `CustomGame_has_Category` (
  `CustomGame_idCustomGame` INT UNSIGNED NOT NULL,
  `Category_idCategory` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`CustomGame_idCustomGame`, `Category_idCategory`),
  INDEX `fk_CustomGame_has_Category_Category1_idx` (`Category_idCategory` ASC) VISIBLE,
  INDEX `fk_CustomGame_has_Category_CustomGame1_idx` (`CustomGame_idCustomGame` ASC) VISIBLE,
  CONSTRAINT `fk_CustomGame_has_Category_CustomGame1`
    FOREIGN KEY (`CustomGame_idCustomGame`)
    REFERENCES `CustomGame` (`idCustomGame`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_CustomGame_has_Category_Category1`
    FOREIGN KEY (`Category_idCategory`)
    REFERENCES `Category` (`idCategory`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
