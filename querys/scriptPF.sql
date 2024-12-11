-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema erp
-- -----------------------------------------------------
DROP SCHEMA erp;
-- -----------------------------------------------------
-- Schema erp
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `erp` DEFAULT CHARACTER SET utf8 ;
USE `erp` ;

-- -----------------------------------------------------
-- Table `erp`.`cliente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `erp`.`cliente` (
  `idCliente` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `telefono` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  `direccion` VARCHAR(200) NULL,
  `notas` LONGTEXT NULL,
  PRIMARY KEY (`idCliente`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `erp`.`actividad`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `erp`.`actividad` (
  `idActividad` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `fecha_inicio` DATE NULL,
  `fecha_fin` DATE NULL,
  `descripcion` LONGTEXT NULL,
  `acciones_realizadas` VARCHAR(45) NULL,
  `tipo` VARCHAR(45) NULL,
  `estado` VARCHAR(45) NULL,
  `idCliente` INT NOT NULL,
  PRIMARY KEY (`idActividad`),
  INDEX `fk_actividad_cliente_idx` (`idCliente` ASC) VISIBLE,
  CONSTRAINT `fk_actividad_cliente`
    FOREIGN KEY (`idCliente`)
    REFERENCES `erp`.`cliente` (`idCliente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `erp`.`miembro`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `erp`.`miembro` (
  `idMiembro` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `telefono` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  `direccion` VARCHAR(45) NULL,
  `disponibilidad` VARCHAR(45) NULL,
  `estatus` VARCHAR(45) NULL,
  `notas` LONGTEXT NULL,
  PRIMARY KEY (`idMiembro`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `erp`.`factura`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `erp`.`factura` (
  `idFactura` INT NOT NULL AUTO_INCREMENT,
  `fecha_emision` DATE NULL,
  `costo` DOUBLE NULL,
  `tipo` VARCHAR(45) NULL,
  `impuesto` DOUBLE NULL,
  `estatus` VARCHAR(45) NULL,
  `creado_por` VARCHAR(45) NULL,
  `fecha_modificacion` DATE NULL,
  `modificado_por` VARCHAR(45) NULL,
  `idActividad` INT NOT NULL,
  `idMiembro` INT NOT NULL,
  PRIMARY KEY (`idFactura`),
  INDEX `fk_factura_actividad1_idx` (`idActividad` ASC) VISIBLE,
  INDEX `fk_factura_miembro1_idx` (`idMiembro` ASC) VISIBLE,
  CONSTRAINT `fk_factura_actividad1`
    FOREIGN KEY (`idActividad`)
    REFERENCES `erp`.`actividad` (`idActividad`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_factura_miembro1`
    FOREIGN KEY (`idMiembro`)
    REFERENCES `erp`.`miembro` (`idMiembro`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `erp`.`recurso`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `erp`.`recurso` (
  `idRecurso` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `tipo` VARCHAR(45) NULL,
  `descripcion` VARCHAR(45) NULL,
  `categoria` VARCHAR(45) NULL,
  `no_serie` VARCHAR(45) NULL,
  `estado_recurso` VARCHAR(45) NULL,
  `vida_util` VARCHAR(45) NULL,
  `notas` VARCHAR(45) NULL,
  PRIMARY KEY (`idRecurso`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `erp`.`miembro_has_actividad`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `erp`.`miembro_has_actividad` (
  `miembro_idMiembro` INT NULL,
  `actividad_idActividad` INT NULL,
  `idMiembroActividad` INT NOT NULL AUTO_INCREMENT,
  INDEX `fk_miembro_has_actividad_actividad1_idx` (`actividad_idActividad` ASC) VISIBLE,
  INDEX `fk_miembro_has_actividad_miembro1_idx` (`miembro_idMiembro` ASC) VISIBLE,
  PRIMARY KEY (`idMiembroActividad`),
  CONSTRAINT `fk_miembro_has_actividad_miembro1`
    FOREIGN KEY (`miembro_idMiembro`)
    REFERENCES `erp`.`miembro` (`idMiembro`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_miembro_has_actividad_actividad1`
    FOREIGN KEY (`actividad_idActividad`)
    REFERENCES `erp`.`actividad` (`idActividad`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `erp`.`actividad_has_recurso`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `erp`.`actividad_has_recurso` (
  `idActividad` INT NULL,
  `idRecurso` INT NULL,
  `idARecurso` INT NOT NULL AUTO_INCREMENT,
  INDEX `fk_actividad_has_recurso_recurso1_idx` (`idRecurso` ASC) VISIBLE,
  INDEX `fk_actividad_has_recurso_actividad1_idx` (`idActividad` ASC) VISIBLE,
  PRIMARY KEY (`idARecurso`),
  CONSTRAINT `fk_actividad_has_recurso_actividad1`
    FOREIGN KEY (`idActividad`)
    REFERENCES `erp`.`actividad` (`idActividad`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_actividad_has_recurso_recurso1`
    FOREIGN KEY (`idRecurso`)
    REFERENCES `erp`.`recurso` (`idRecurso`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
