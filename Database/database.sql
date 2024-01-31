CREATE DATABASE gestion_sw;

USE gestion_sw;

-- Tabla admin
CREATE TABLE admin (
    id_admin INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    correo_electronico VARCHAR(100) NOT NULL,
    contrasena VARCHAR(50) NOT NULL,
    PRIMARY KEY (id_admin)
);

-- Tabla equipo
CREATE TABLE equipo (
  id_equipo INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(255) NOT NULL,
  PRIMARY KEY (id_equipo)
);

-- Tabla rol
CREATE TABLE rol (
  id_rol INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(255) NOT NULL,
  PRIMARY KEY (id_rol)
);

-- Tabla miembro
CREATE TABLE miembro (
  id_miembro INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(255) NOT NULL,
  correo_electronico VARCHAR(255) NOT NULL,
  contrasena VARCHAR(255) NOT NULL,
  fk_rol INT NOT NULL,
  fk_equipo INT NOT NULL,
  PRIMARY KEY (id_miembro),
  FOREIGN KEY (fk_rol) REFERENCES rol (id_rol),
  FOREIGN KEY (fk_equipo) REFERENCES equipo (id_equipo)
);

-- Tabla recurso
CREATE TABLE recurso (
  id_recurso INT NOT NULL AUTO_INCREMENT,
  tipo_recurso VARCHAR(255) NOT NULL,
  nombre VARCHAR(255) NOT NULL,
  funcionalidad VARCHAR(255) NOT NULL,
  PRIMARY KEY (id_recurso)
);

-- Tabla estado
CREATE TABLE   (
  id_estado INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(255) NOT NULL,
  PRIMARY KEY (id_estado)
);

-- Tabla proyecto
CREATE TABLE proyecto (
  id_proyecto INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(255) NOT NULL,
  descripcion VARCHAR(255) NOT NULL,
  fecha_inicio DATE NOT NULL,
  fk_equipo INT NOT NULL,
  fk_estado INT NOT NULL,
  fk_recurso INT NOT NULL,
  PRIMARY KEY (id_proyecto),
  FOREIGN KEY (fk_equipo) REFERENCES equipo (id_equipo),
  FOREIGN KEY (fk_estado) REFERENCES estado (id_estado),
  FOREIGN KEY (fk_recurso) REFERENCES recurso (id_recurso)
);