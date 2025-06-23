-- Crear la base de datos (si no existe)
CREATE DATABASE cmdb;

-- Conectarse a la base de datos
\c cmdb

-- Crear enumeraciones personalizadas
CREATE TYPE ci_tipo AS ENUM ('Hardware', 'Software');
CREATE TYPE estado_actual AS ENUM ('Activo', 'Inactivo');
CREATE TYPE nivel_seguridad AS ENUM ('Alto', 'Medio', 'Bajo');
CREATE TYPE cumplimiento AS ENUM ('Cumple', 'No Cumple');
CREATE TYPE estado_configuracion AS ENUM ('Aprobado', 'No Aprobado');

-- Crear tabla CIS
CREATE TABLE cis (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    tipo ci_tipo NOT NULL,
    descripción TEXT,
    número_serie VARCHAR(50),
    versión VARCHAR(20),
    fecha_adquisición TIMESTAMP,
    estado_actual estado_actual NOT NULL,
    relaciones JSON,
    ubicación_física VARCHAR(255),
    propietario_responsable VARCHAR(255),
    fecha_cambio TIMESTAMP,
    descripción_cambio TEXT,
    documentación_relacionada VARCHAR(255),
    enlaces_incidentes_problemas VARCHAR(255),
    nivel_seguridad nivel_seguridad,
    cumplimiento cumplimiento,
    estado_configuración estado_configuracion,
    número_licencia VARCHAR(50),
    fecha_vencimiento TIMESTAMP,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla CI_Relaciones
CREATE TABLE ci_relaciones (
    id SERIAL PRIMARY KEY,
    ci_origen_id INT REFERENCES cis(id),
    ci_destino_id INT REFERENCES cis(id),
    tipo VARCHAR(50),
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla Audit_Logs
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    ci_id INT REFERENCES cis(id),
    acción VARCHAR(50) NOT NULL,
    valor_anterior JSON,
    valor_nuevo JSON,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Data de ejemplo
INSERT INTO cis (nombre, tipo, descripción, número_serie, versión, fecha_adquisición, estado_actual, relaciones, ubicación_física, propietario_responsable, fecha_cambio, descripción_cambio, documentación_relacionada, enlaces_incidentes_problemas, nivel_seguridad, cumplimiento, estado_configuración, número_licencia, fecha_vencimiento)
VALUES
    ('Servidor1', 'Hardware', 'Servidor de aplicaciones', 'SN123456', 'v1.0', '2022-01-01 00:00:00', 'Activo', '{"padres": [], "hijos": []}', 'Sala de Servidores', 'Equipo Infraestructura', '2022-02-01 00:00:00', 'Actualización de software', 'Enlace a Manual[url]', 'Enlace a incidente[url]', 'Alto', 'Cumple', 'Aprobado', 'ABC123', '2023-01-01 00:00:00'),
    ('Aplicación1', 'Software', 'Aplicación de contabilidad', 'XYZ456', 'v2.0', '2022-03-15 00:00:00', 'Activo', '{"padres": [], "hijos": []}', 'Servidor1', 'Equipo Desarrollo', '2022-04-01 00:00:00', 'Parche de Seguridad', 'Enlace a Documentación[url]', 'Enlace a incidente[url]', 'Medio', 'Cumple', 'Aprobado', 'XYZ456', '2024-01-01 00:00:00');

INSERT INTO ci_relaciones (ci_origen_id, ci_destino_id, tipo)
VALUES
    ((SELECT id FROM cis WHERE nombre = 'Servidor1'), (SELECT id FROM cis WHERE nombre = 'Aplicación1'), 'ALOJA');

INSERT INTO audit_logs (ci_id, acción, valor_anterior, valor_nuevo)
VALUES
    ((SELECT id FROM cis WHERE nombre = 'Servidor1'), 'CREAR', NULL, '{"nombre": "Servidor1", "tipo": "Hardware", "estado_actual": "Activo"}');

SELECT * FROM cis;
SELECT * FROM ci_relaciones;
SELECT * FROM audit_logs;