CREATE DATABASE gestion_sw;

USE gestion_sw;

-- Tabla admin
CREATE TABLE admin (
    id_admin INT AUTO_INCREMENT,
    nombre VARCHAR(50),
    correo_electronico VARCHAR(100),
    contrasena VARCHAR(50),
    PRIMARY KEY (id_admin)
);

-- Tabla equipo
CREATE TABLE equipo (
  id_equipo INT AUTO_INCREMENT,
  nombre VARCHAR(255),
  PRIMARY KEY (id_equipo)
);

-- Tabla rol
CREATE TABLE rol (
  id_rol INT AUTO_INCREMENT,
  nombre VARCHAR(255),
  PRIMARY KEY (id_rol)
);

-- Tabla miembro
CREATE TABLE miembro (
  id_miembro INT AUTO_INCREMENT,
  nombre VARCHAR(255),
  correo_electronico VARCHAR(255),
  contrasena VARCHAR(255),
  fk_rol INT,
  fk_equipo INT,
  PRIMARY KEY (id_miembro),
  FOREIGN KEY (fk_rol) REFERENCES rol (id_rol),
  FOREIGN KEY (fk_equipo) REFERENCES equipo (id_equipo)
);

-- Tabla recurso
CREATE TABLE recurso (
  id_recurso INT AUTO_INCREMENT,
  tipo_recurso VARCHAR(255),
  nombre VARCHAR(255),
  funcionalidad VARCHAR(255),
  PRIMARY KEY (id_recurso)
);

-- Tabla estado
CREATE TABLE estado (
  id_estado INT AUTO_INCREMENT,
  nombre VARCHAR(255),
  PRIMARY KEY (id_estado)
);

-- Tabla proyecto
CREATE TABLE proyecto (
  id_proyecto INT AUTO_INCREMENT,
  nombre VARCHAR(255),
  descripcion VARCHAR(255),
  fecha_inicio DATE,
  fk_equipo INT,
  fk_estado INT,
  fk_recurso INT,
  PRIMARY KEY (id_proyecto),
  FOREIGN KEY (fk_equipo) REFERENCES equipo (id_equipo),
  FOREIGN KEY (fk_estado) REFERENCES estado (id_estado),
  FOREIGN KEY (fk_recurso) REFERENCES recurso (id_recurso)
);

