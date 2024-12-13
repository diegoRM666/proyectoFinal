-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema erp
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema erp
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `erp` DEFAULT CHARACTER SET utf8mb3 ;
USE `erp` ;

-- -----------------------------------------------------
-- Table `erp`.`cliente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `erp`.`cliente` (
  `idCliente` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL DEFAULT NULL,
  `telefono` VARCHAR(45) NULL DEFAULT NULL,
  `email` VARCHAR(45) NULL DEFAULT NULL,
  `direccion` VARCHAR(200) NULL DEFAULT NULL,
  `notas` LONGTEXT NULL DEFAULT NULL,
  PRIMARY KEY (`idCliente`))
ENGINE = InnoDB
AUTO_INCREMENT = 6
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `erp`.`miembro`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `erp`.`miembro` (
  `idMiembro` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL DEFAULT NULL,
  `telefono` VARCHAR(45) NULL DEFAULT NULL,
  `email` VARCHAR(45) NULL DEFAULT NULL,
  `direccion` VARCHAR(45) NULL DEFAULT NULL,
  `disponibilidad` VARCHAR(45) NULL DEFAULT NULL,
  `estatus` VARCHAR(45) NULL DEFAULT NULL,
  `notas` LONGTEXT NULL DEFAULT NULL,
  PRIMARY KEY (`idMiembro`))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `erp`.`actividad`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `erp`.`actividad` (
  `idActividad` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL DEFAULT NULL,
  `fecha_inicio` DATE NULL DEFAULT NULL,
  `fecha_fin` DATE NULL DEFAULT NULL,
  `descripcion` LONGTEXT NULL DEFAULT NULL,
  `acciones_realizadas` VARCHAR(45) NULL DEFAULT NULL,
  `tipo` VARCHAR(45) NULL DEFAULT NULL,
  `estado` VARCHAR(45) NULL DEFAULT NULL,
  `idCliente` INT NOT NULL,
  `idMiembro` INT NOT NULL,
  PRIMARY KEY (`idActividad`),
  INDEX `fk_actividad_cliente_idx` (`idCliente` ASC) VISIBLE,
  INDEX `fk_actividad_miembro1_idx` (`idMiembro` ASC) VISIBLE,
  CONSTRAINT `fk_actividad_cliente`
    FOREIGN KEY (`idCliente`)
    REFERENCES `erp`.`cliente` (`idCliente`),
  CONSTRAINT `fk_actividad_miembro1`
    FOREIGN KEY (`idMiembro`)
    REFERENCES `erp`.`miembro` (`idMiembro`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `erp`.`recurso`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `erp`.`recurso` (
  `idRecurso` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL DEFAULT NULL,
  `tipo` VARCHAR(45) NULL DEFAULT NULL,
  `descripcion` VARCHAR(45) NULL DEFAULT NULL,
  `categoria` VARCHAR(45) NULL DEFAULT NULL,
  `no_serie` VARCHAR(45) NULL DEFAULT NULL,
  `estado_recurso` VARCHAR(45) NULL DEFAULT NULL,
  `vida_util` VARCHAR(45) NULL DEFAULT NULL,
  `notas` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`idRecurso`))
ENGINE = InnoDB
AUTO_INCREMENT = 6
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `erp`.`actividad_has_recurso`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `erp`.`actividad_has_recurso` (
  `idActividad` INT NULL DEFAULT NULL,
  `idRecurso` INT NULL DEFAULT NULL,
  `idARecurso` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`idARecurso`),
  INDEX `fk_actividad_has_recurso_recurso1_idx` (`idRecurso` ASC) VISIBLE,
  INDEX `fk_actividad_has_recurso_actividad1_idx` (`idActividad` ASC) VISIBLE,
  CONSTRAINT `fk_actividad_has_recurso_actividad1`
    FOREIGN KEY (`idActividad`)
    REFERENCES `erp`.`actividad` (`idActividad`),
  CONSTRAINT `fk_actividad_has_recurso_recurso1`
    FOREIGN KEY (`idRecurso`)
    REFERENCES `erp`.`recurso` (`idRecurso`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `erp`.`factura`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `erp`.`factura` (
  `idFactura` INT NOT NULL AUTO_INCREMENT,
  `fecha_emision` DATE NULL DEFAULT NULL,
  `costo` DOUBLE NULL DEFAULT NULL,
  `tipo` VARCHAR(45) NULL DEFAULT NULL,
  `impuesto` DOUBLE NULL DEFAULT NULL,
  `estatus` VARCHAR(45) NULL DEFAULT NULL,
  `creado_por` VARCHAR(45) NULL DEFAULT NULL,
  `fecha_modificacion` DATE NULL DEFAULT NULL,
  `modificado_por` VARCHAR(45) NULL DEFAULT NULL,
  `idActividad` INT NOT NULL,
  `idMiembro` INT NOT NULL,
  PRIMARY KEY (`idFactura`),
  INDEX `fk_factura_actividad1_idx` (`idActividad` ASC) VISIBLE,
  INDEX `fk_factura_miembro1_idx` (`idMiembro` ASC) VISIBLE,
  CONSTRAINT `fk_factura_actividad1`
    FOREIGN KEY (`idActividad`)
    REFERENCES `erp`.`actividad` (`idActividad`),
  CONSTRAINT `fk_factura_miembro1`
    FOREIGN KEY (`idMiembro`)
    REFERENCES `erp`.`miembro` (`idMiembro`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `erp`.`peticion_nuevo_recurso`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `erp`.`peticion_nuevo_recurso` (
  `idCliente` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL DEFAULT NULL,
  `tipo` VARCHAR(45) NULL DEFAULT NULL,
  `descripcion` VARCHAR(400) NULL DEFAULT NULL,
  `fecha_peticion` DATE NULL DEFAULT NULL,
  `cantidad` INT NULL DEFAULT NULL,
  `estado_peticion` VARCHAR(200) NULL DEFAULT NULL,
  `notas` LONGTEXT NULL DEFAULT NULL,
  `idMiembro` INT NOT NULL,
  PRIMARY KEY (`idCliente`),
  INDEX `fk_peticion_nuevo_recurso_1_idx` (`idMiembro` ASC) VISIBLE,
  CONSTRAINT `fk_peticion_nuevo_recurso_1`
    FOREIGN KEY (`idMiembro`)
    REFERENCES `erp`.`miembro` (`idMiembro`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
