DROP DATABASE if EXISTS agrocontrol;
CREATE DATABASE agrocontrol;
USE agrocontrol;

CREATE TABLE uso (
   numero_uso INT(10) PRIMARY KEY AUTO_INCREMENT,
	Nombre_encargado VARCHAR(20) NOT NULL
);

CREATE TABLE Fincas(
	Finca_ID INT(10) PRIMARY KEY AUTO_INCREMENT,
	Nombre VARCHAR(20) NOT NULL,
	latitud DECIMAL(9,6),
	longitud DECIMAL(9,6),
	ubicacion VARCHAR(30) NOT NULL , 
	Hectareas INT(10) NOT NULL,
   altitud INT(10) NOT NULL, 
   Temperatura INT(3) NOT NULL, 
   tipo_suelo VARCHAR(10) NOT NULL
);

CREATE TABLE Parcelas (
  parcelas_ID INT(10) PRIMARY KEY AUTO_INCREMENT,
  Hectareas INT(10) NOT NULL, 
  sistema_riego VARCHAR(15),
  uso_id INT(10) NULL,
  finca_id INT(10) NOT NULL,
  FOREIGN KEY (uso_id) REFERENCES uso(numero_uso),
  FOREIGN KEY (finca_id) REFERENCES Fincas(Finca_ID)
);

CREATE TABLE historial_uso (
  id_historial INT PRIMARY KEY AUTO_INCREMENT,
  parcela_id INT,
  uso_id INT,
  fecha_inicio DATE,
  fecha_fin DATE,
  FOREIGN KEY (parcela_id) REFERENCES Parcelas(parcelas_ID),
  FOREIGN KEY (uso_id) REFERENCES uso(numero_uso)
);

CREATE TABLE cultivos(
	cultivo_id INT(10) PRIMARY KEY AUTO_INCREMENT,
	nombre_cientifico VARCHAR(20) NOT NULL UNIQUE,
	nombre_comun VARCHAR(20) NOT NULL,
	tiempo_crecimiento INT(10) NOT NULL,
	temperatura_optima INT(5) NOT NULL,
	agua INT(10) NOT NULL
);

CREATE TABLE temporada(
	id_siembra INT(10) PRIMARY KEY AUTO_INCREMENT, 
	parcela_id INT(10) NOT NULL,
	cultivo_id INT(10) NOT NULL,
	fecha_siembra DATE NOT NULL,
	fecha_estimada_cosecha DATE,
	densidad_siembra INT(10) NOT NULL,
   rendimiento_esperado INT(10) NOT NULL,
   FOREIGN KEY (parcela_id) REFERENCES Parcelas(parcelas_ID),
   FOREIGN KEY (cultivo_id) REFERENCES cultivos(cultivo_id)
);

CREATE TABLE inventario(
	Codigo_id INT(10) PRIMARY KEY AUTO_INCREMENT,
	nombre_comercial VARCHAR(20) NOT NULL,
	Tipo VARCHAR(15) NOT NULL,
	unidad_medida VARCHAR(10),
	ubicacion VARCHAR(20) NOT NULL,
	cantidad_stok INT(10),
	fecha_caducidad DATE NOT NULL,
	precio INT(10) NOT NULL
);

CREATE TABLE movimiento_insumos(
	movimiento_id INT(10) PRIMARY KEY AUTO_INCREMENT,
	fecha DATE NOT NULL,
	tipo_movimiento VARCHAR(10) NOT NULL,
	cantidad INT(10) NOT NULL,
	responsable VARCHAR(20),
	destino VARCHAR(30),
	Codigo_id INT(10),
	FOREIGN KEY (Codigo_id) REFERENCES inventario(Codigo_id)
);

CREATE TABLE maquinaria(
	codigo_maquina INT(10) PRIMARY KEY AUTO_INCREMENT,
	marca VARCHAR(20),
	modelo VARCHAR(20),
	anio_fabricacion INT(4),
	potencia INT(10),
	tipo_combustible VARCHAR(15),
	horometro INT(10),
	estado VARCHAR(15)
);

CREATE TABLE mantenimiento(
	mantenimiento_id INT(10) PRIMARY KEY AUTO_INCREMENT,
	fecha DATE NOT NULL,
	tipo_mantenimiento VARCHAR(20),
	descripcion_trabajos VARCHAR(200),
	piezas_remplazadas VARCHAR(30),
	costo INT(10),
	responsable VARCHAR(20),
	codigo_maquina INT(10),
	FOREIGN KEY (codigo_maquina) REFERENCES maquinaria(codigo_maquina)
);

CREATE TABLE empleados(
	empleados_id INT(10) AUTO_INCREMENT PRIMARY KEY,
	DNI INT(11) UNIQUE NOT NULL, 
	nombres VARCHAR(20) NOT NULL,
	apellidos VARCHAR(25) NOT NULL,
	fecha_nacimiento DATE NOT NULL,
	direccion VARCHAR(20),
	telefono VARCHAR(15) NOT NULL,
	especialidad VARCHAR(15) NOT NULL,
	fecha_contratacion DATE NOT NULL,
	salario INT(10) NOT NULL
);

CREATE TABLE area_asignada(
	area_id INT(10) PRIMARY KEY AUTO_INCREMENT,
	empleado INT(10) NOT NULL,
	tarea VARCHAR(20),
	parcela INT(10),
	fecha DATETIME,
	horas_trabajadas INT(5),
	observaciones VARCHAR(50),
	FOREIGN KEY (empleado) REFERENCES empleados(empleados_id),
	FOREIGN KEY (parcela) REFERENCES Parcelas(parcelas_ID)
);

CREATE TABLE cosecha (
	cosecha_id INT(10) PRIMARY KEY AUTO_INCREMENT,
	parcela INT(10),
	cultivo INT(10),
	inicio DATE,
	fin DATE,
	cantidad INT(10),
	calidad_producto VARCHAR(15),
	metodo_cosecha VARCHAR(20),
	FOREIGN KEY (parcela) REFERENCES Parcelas(parcelas_ID),
	FOREIGN KEY (cultivo) REFERENCES cultivos(cultivo_id)
);

CREATE TABLE clientes( 
	cliente_id INT(10) PRIMARY KEY AUTO_INCREMENT,
	nombre VARCHAR(20) NOT NULL,
	RUC_o_DNI VARCHAR(15) NOT NULL UNIQUE,
	direccion_fiscal VARCHAR(30),
	telefono VARCHAR(15),
	correo_electronico VARCHAR(25),
	linea_credito INT(10)
);

CREATE TABLE proveedores(
	proveedor_id INT(10) PRIMARY KEY AUTO_INCREMENT,
	nombre VARCHAR(20) NOT NULL,
	RUC_o_DNI VARCHAR(15) NOT NULL UNIQUE,
	direccion_fiscal VARCHAR(30),
	telefono VARCHAR(15),
	correo_electronico VARCHAR(25),
	credito INT(10),
	especialidad VARCHAR(20),
	condiciones_pago VARCHAR(30)
);

CREATE TABLE ventas( 
	venta_id INT(10) PRIMARY KEY AUTO_INCREMENT,
	fecha DATE,
	cliente INT(10),
	productos VARCHAR(20),
	cantidades INT(10),
	precio_unitario INT(10),
	descuentos INT(10),
	impuestos INT(10),
	forma_pago VARCHAR(15),
	total_facturado INT(10),
	FOREIGN KEY (cliente) REFERENCES clientes(cliente_id)
);

CREATE TABLE analisis_suelos(
	analisis_id INT(10) PRIMARY KEY AUTO_INCREMENT,
	fecha_muestreo DATE,
	parcela INT(10),
	ph INT(5),
	nitrogeno INT(5),
	fosforo INT(5),
	potasio INT(5),
	materia_organica INT(10),
	conductividad INT(10),
	nombre_laboratorio VARCHAR(20),
	recomendaciones VARCHAR(100),
	FOREIGN KEY (parcela) REFERENCES Parcelas(parcelas_ID)
);

USE agrocontrol;

INSERT INTO uso (Nombre_encargado) VALUES
('Carlos Rojas'),
('Ana Pérez'),
('Luis Gómez');

INSERT INTO Fincas (Nombre, latitud, longitud, ubicacion, Hectareas, altitud, Temperatura, tipo_suelo) VALUES
('El Sol', 5.123456, -72.654321, 'Vereda La Vega', 30, 250, 22, 'Arcilloso'),
('La Esperanza', 4.987654, -73.321456, 'Vereda Santa Fe', 50, 300, 24, 'Arenoso'),
('Los Olivos', 4.876543, -73.654789, 'Vereda San José', 45, 280, 23, 'Franco');

INSERT INTO Parcelas (Hectareas, sistema_riego, uso_id, finca_id) VALUES
(5, 'Goteo', 1, 1),
(8, 'Aspersión', 2, 2),
(6, 'Manual', 3, 3);

INSERT INTO historial_uso (parcela_id, uso_id, fecha_inicio, fecha_fin) VALUES
(1, 1, '2024-01-10', '2024-06-15'),
(1, 2, '2024-06-16', '2024-12-10'),
(2, 2, '2024-03-01', '2024-09-20'),
(3, 3, '2024-04-05', '2024-10-10');

INSERT INTO cultivos (nombre_cientifico, nombre_comun, tiempo_crecimiento, temperatura_optima, agua) VALUES
('Zea mays', 'Maíz', 120, 25, 600),
('Oryza sativa', 'Arroz', 150, 28, 900),
('Solanum tuberosum', 'Papa', 110, 18, 700);

INSERT INTO temporada (parcela_id, cultivo_id, fecha_siembra, fecha_estimada_cosecha, densidad_siembra, rendimiento_esperado) VALUES
(1, 1, '2024-01-12', '2024-05-20', 200, 4500),
(2, 2, '2024-03-10', '2024-08-15', 180, 5200),
(3, 3, '2024-04-01', '2024-09-10', 220, 4000);

INSERT INTO inventario (nombre_comercial, Tipo, unidad_medida, ubicacion, cantidad_stok, fecha_caducidad, precio) VALUES
('Fertimax', 'Fertilizante', 'Kg', 'Bodega A', 150, '2026-05-20', 45000),
('Semilla Dorada', 'Semilla', 'Kg', 'Bodega B', 200, '2025-11-30', 25000),
('Plaguistop', 'Plaguicida', 'Lt', 'Bodega C', 100, '2026-01-15', 38000);

INSERT INTO movimiento_insumos (fecha, tipo_movimiento, cantidad, responsable, destino, Codigo_id) VALUES
('2024-01-15', 'Entrada', 50, 'Carlos Rojas', 'Bodega A', 1),
('2024-02-10', 'Salida', 20, 'Ana Pérez', 'Parcela 1', 1),
('2024-03-05', 'Salida', 15, 'Luis Gómez', 'Parcela 2', 2),
('2024-04-01', 'Entrada', 30, 'Carlos Rojas', 'Bodega C', 3);

INSERT INTO maquinaria (marca, modelo, anio_fabricacion, potencia, tipo_combustible, horometro, estado) VALUES
('John Deere', 'JD2040', 2020, 90, 'Diésel', 1200, 'Operativa'),
('Kubota', 'KBX150', 2019, 75, 'Gasolina', 1500, 'Operativa'),
('New Holland', 'NH340', 2021, 100, 'Diésel', 800, 'Mantenimiento');

INSERT INTO mantenimiento (fecha, tipo_mantenimiento, descripcion_trabajos, piezas_remplazadas, costo, responsable, codigo_maquina) VALUES
('2024-03-20', 'Preventivo', 'Cambio de aceite y filtro', 'Filtro aceite', 250000, 'Luis Gómez', 1),
('2024-05-10', 'Correctivo', 'Reemplazo de correa principal', 'Correa', 320000, 'Ana Pérez', 2),
('2024-07-18', 'Preventivo', 'Engrase general y revisión', 'Ninguna', 150000, 'Carlos Rojas', 3);

INSERT INTO empleados (DNI, nombres, apellidos, fecha_nacimiento, direccion, telefono, especialidad, fecha_contratacion, salario) VALUES
(10111222, 'Carlos', 'Rojas', '1988-06-10', 'Cra 12 #4-10', '3205678901', 'Agrónomo', '2019-01-15', 2500000),
(10111333, 'Ana', 'Pérez', '1990-03-25', 'Calle 8 #3-21', '3102345678', 'Técnica agrícola', '2020-02-10', 1800000),
(10111444, 'Luis', 'Gómez', '1985-11-18', 'Av 10 #20-45', '3113456789', 'Mecánico', '2018-07-05', 2000000);

INSERT INTO area_asignada (empleado, tarea, parcela, fecha, horas_trabajadas, observaciones) VALUES
(1, 'Siembra', 1, '2024-01-13 08:00:00', 6, 'Buena germinación'),
(2, 'Riego', 2, '2024-03-12 09:00:00', 5, 'Sistema funcional'),
(3, 'Mantenimiento', 3, '2024-04-06 10:00:00', 7, 'Sin fallas');

INSERT INTO cosecha (parcela, cultivo, inicio, fin, cantidad, calidad_producto, metodo_cosecha) VALUES
(1, 1, '2024-05-25', '2024-06-05', 4300, 'Alta', 'Manual'),
(2, 2, '2024-08-20', '2024-09-05', 5000, 'Media', 'Mecanizada'),
(3, 3, '2024-09-15', '2024-10-01', 3800, 'Alta', 'Manual');

INSERT INTO clientes (nombre, RUC_o_DNI, direccion_fiscal, telefono, correo_electronico, linea_credito) VALUES
('Agroventas SAS', '900123456', 'Calle 10 #45-23', '3124567890', 'contacto@agroventas.com', 2000000),
('CampoVivo Ltda', '900654321', 'Av 15 #22-10', '3105674321', 'info@campovivo.com', 3000000),
('Frutales del Sur', '901112233', 'Calle 20 #33-11', '3134567890', 'ventas@frutales.com', 1500000);

INSERT INTO proveedores (nombre, RUC_o_DNI, direccion_fiscal, telefono, correo_electronico, credito, especialidad, condiciones_pago) VALUES
('Agroinsumos SA', '800123456', 'Zona Industrial 12', '3141234567', 'agro@insumos.com', 4000000, 'Fertilizantes', '30 días'),
('Semillando SAS', '830654321', 'Calle 45 #10-22', '3159876543', 'ventas@semillando.com', 2500000, 'Semillas', '15 días'),
('ProtecAgro', '845987654', 'Carrera 8 #9-30', '3125556677', 'info@protecagro.com', 3000000, 'Plaguicidas', '20 días');

INSERT INTO ventas (fecha, cliente, productos, cantidades, precio_unitario, descuentos, impuestos, forma_pago, total_facturado) VALUES
('2024-06-10', 1, 'Maíz', 4000, 1200, 100000, 150000, 'Transferencia', 4750000),
('2024-09-10', 2, 'Arroz', 4800, 1500, 120000, 200000, 'Efectivo', 7000000),
('2024-10-05', 3, 'Papa', 3500, 1100, 90000, 130000, 'Crédito', 4200000);

INSERT INTO analisis_suelos (fecha_muestreo, parcela, ph, nitrogeno, fosforo, potasio, materia_organica, conductividad, nombre_laboratorio, recomendaciones) VALUES
('2024-01-05', 1, 6, 80, 60, 90, 3, 2, 'AgroLab', 'Agregar materia orgánica'),
('2024-03-02', 2, 5, 70, 55, 85, 4, 3, 'EcoSuelo', 'Aplicar fertilizante NPK'),
('2024-04-10', 3, 6, 75, 65, 95, 3, 2, 'BioAnálisis', 'Ajustar riego y pH');
INSERT INTO Parcelas (Hectareas, sistema_riego, uso_id, finca_id) VALUES
(10, 'Goteo', 1, 1),
(7, 'Aspersión', 2, 1),
(4, 'Manual', 3, 1),
(12, 'Goteo', 1, 2),
(9, 'Aspersión', 2, 2),
(11, 'Goteo', 1, 2),
(6, 'Manual', 3, 2),
(8, 'Aspersión', 2, 3),
(5, 'Goteo', 1, 3),
(10, 'Manual', 3, 3);
USE Agrocontrol;

INSERT INTO uso (Nombre_encargado) VALUES
('María Torres'),
('Pedro Sánchez'),
('Laura Mendoza'),
('Javier Castro'),
('Sofia Ramírez');

INSERT INTO Fincas (Nombre, latitud, longitud, ubicacion, Hectareas, altitud, Temperatura, tipo_suelo) VALUES
('Villa Verde', 5.234567, -72.876543, 'Vereda El Carmen', 40, 320, 21, 'Franco'),
('Santa María', 4.765432, -73.123456, 'Vereda La Palma', 35, 290, 23, 'Arcilloso'),
('El Paraíso', 5.345678, -72.987654, 'Vereda Nuevo Horizonte', 55, 270, 25, 'Arenoso');

INSERT INTO Parcelas (Hectareas, sistema_riego, uso_id, finca_id) VALUES
(10, 'Goteo', 1, 1),
(7, 'Aspersión', 2, 1),
(4, 'Manual', 3, 1),
(12, 'Goteo', 4, 2),
(9, 'Aspersión', 5, 2),
(11, 'Goteo', 1, 2),
(6, 'Manual', 2, 2),
(8, 'Aspersión', 3, 3),
(5, 'Goteo', 4, 3),
(10, 'Manual', 5, 3),
(9, 'Goteo', 1, 4),
(13, 'Aspersión', 2, 4),
(8, 'Manual', 3, 5),
(11, 'Goteo', 4, 5),
(7, 'Aspersión', 5, 6);
INSERT INTO historial_uso (parcela_id, uso_id, fecha_inicio, fecha_fin) VALUES
(4, 1, '2024-01-15', '2024-07-20'),
(5, 2, '2024-02-10', '2024-08-15'),
(6, 3, '2024-03-05', '2024-09-10'),
(7, 4, '2024-04-12', '2024-10-18'),
(8, 5, '2024-05-08', '2024-11-12'),
(9, 1, '2024-06-15', NULL),
(10, 2, '2024-07-20', NULL);

INSERT INTO cultivos (nombre_cientifico, nombre_comun, tiempo_crecimiento, temperatura_optima, agua) VALUES
('Phaseolus vulgaris', 'Frijol', 90, 22, 500),
('Manihot esculenta', 'Yuca', 300, 26, 800),
('Musa paradisiaca', 'Plátano', 365, 27, 1200),
('Coffea arabica', 'Café', 1095, 20, 1500),
('Lycopersicon esculentum', 'Tomate', 85, 24, 650);

INSERT INTO temporada (parcela_id, cultivo_id, fecha_siembra, fecha_estimada_cosecha, densidad_siembra, rendimiento_esperado) VALUES
(4, 4, '2024-02-15', '2024-05-25', 210, 4800),
(5, 5, '2024-03-20', '2024-09-10', 190, 5500),
(6, 6, '2024-04-10', '2024-10-05', 200, 6000),
(7, 7, '2024-05-05', '2028-05-05', 150, 8000),
(8, 8, '2024-06-12', '2024-09-10', 230, 4200),
(9, 1, '2024-07-18', '2024-11-20', 195, 4600),
(10, 2, '2024-08-05', '2025-01-10', 175, 5300);

INSERT INTO inventario (nombre_comercial, Tipo, unidad_medida, ubicacion, cantidad_stok, fecha_caducidad, precio) VALUES
('Nutriplan', 'Fertilizante', 'Kg', 'Bodega A', 180, '2026-08-15', 52000),
('HerbicMax', 'Herbicida', 'Lt', 'Bodega C', 75, '2025-12-20', 68000),
('SemillaPro', 'Semilla', 'Kg', 'Bodega B', 250, '2025-10-30', 32000),
('FungiFort', 'Fungicida', 'Lt', 'Bodega C', 90, '2026-03-10', 58000),
('AgroVit', 'Fertilizante', 'Kg', 'Bodega A', 200, '2026-06-25', 48000),
('InsectStop', 'Insecticida', 'Lt', 'Bodega C', 110, '2025-09-18', 72000);

INSERT INTO movimiento_insumos (fecha, tipo_movimiento, cantidad, responsable, destino, Codigo_id) VALUES
('2024-05-12', 'Entrada', 60, 'María Torres', 'Bodega A', 4),
('2024-05-20', 'Salida', 25, 'Pedro Sánchez', 'Parcela 4', 4),
('2024-06-08', 'Entrada', 40, 'Laura Mendoza', 'Bodega B', 6),
('2024-06-15', 'Salida', 18, 'Javier Castro', 'Parcela 5', 5),
('2024-07-10', 'Salida', 22, 'Sofia Ramírez', 'Parcela 6', 7),
('2024-07-25', 'Entrada', 55, 'Carlos Rojas', 'Bodega C', 8),
('2024-08-05', 'Salida', 30, 'Ana Pérez', 'Parcela 7', 9);

INSERT INTO maquinaria (marca, modelo, anio_fabricacion, potencia, tipo_combustible, horometro, estado) VALUES
('Massey Ferguson', 'MF290', 2018, 85, 'Diésel', 2100, 'Operativa'),
('Case IH', 'CIH120', 2022, 120, 'Diésel', 450, 'Operativa'),
('Yanmar', 'YM180', 2020, 80, 'Diésel', 1100, 'Operativa'),
('Mahindra', 'MH475', 2019, 65, 'Diésel', 1800, 'Mantenimiento');

INSERT INTO mantenimiento (fecha, tipo_mantenimiento, descripcion_trabajos, piezas_remplazadas, costo, responsable, codigo_maquina) VALUES
('2024-04-15', 'Preventivo', 'Cambio de filtros y lubricación', 'Filtro aire, Filtro aceite', 280000, 'Luis Gómez', 4),
('2024-06-22', 'Correctivo', 'Reparación sistema hidráulico', 'Manguera hidráulica', 450000, 'Luis Gómez', 5),
('2024-08-10', 'Preventivo', 'Revisión general y ajustes', 'Ninguna', 180000, 'Luis Gómez', 6),
('2024-09-05', 'Correctivo', 'Cambio de batería y alternador', 'Batería, Alternador', 520000, 'Luis Gómez', 7);

INSERT INTO empleados (DNI, nombres, apellidos, fecha_nacimiento, direccion, telefono, especialidad, fecha_contratacion, salario) VALUES
(10111555, 'María', 'Torres', '1992-08-15', 'Calle 15 #12-30', '3156789012', 'Agrónoma', '2021-03-12', 2400000),
(10111666, 'Pedro', 'Sánchez', '1987-05-20', 'Cra 20 #8-15', '3167890123', 'Operario', '2019-06-18', 1600000),
(10111777, 'Laura', 'Mendoza', '1995-12-08', 'Av 5 #18-25', '3178901234', 'Técnica agrícola', '2022-01-20', 1900000),
(10111888, 'Javier', 'Castro', '1989-09-30', 'Calle 22 #14-50', '3189012345', 'Operario', '2020-08-10', 1650000),
(10111999, 'Sofia', 'Ramírez', '1993-04-12', 'Cra 8 #25-18', '3190123456', 'Supervisora', '2021-11-05', 2200000);

INSERT INTO area_asignada (empleado, tarea, parcela, fecha, horas_trabajadas, observaciones) VALUES
(4, 'Fertilización', 4, '2024-02-20 07:00:00', 8, 'Aplicación uniforme'),
(5, 'Cosecha', 5, '2024-09-12 06:00:00', 10, 'Rendimiento alto'),
(6, 'Siembra', 6, '2024-04-15 08:00:00', 7, 'Condiciones óptimas'),
(7, 'Riego', 7, '2024-05-08 09:00:00', 5, 'Sistema eficiente'),
(8, 'Control plagas', 8, '2024-06-18 07:30:00', 6, 'Aplicación preventiva'),
(1, 'Supervisión', 9, '2024-07-22 08:00:00', 8, 'Todo en orden'),
(2, 'Fertilización', 10, '2024-08-10 07:00:00', 7, 'Dosis adecuada');

INSERT INTO cosecha (parcela, cultivo, inicio, fin, cantidad, calidad_producto, metodo_cosecha) VALUES
(4, 4, '2024-05-28', '2024-06-10', 4650, 'Alta', 'Manual'),
(5, 5, '2024-09-12', '2024-09-28', 5400, 'Alta', 'Mecanizada'),
(6, 6, '2024-10-08', '2024-10-22', 5800, 'Media', 'Manual'),
(8, 8, '2024-09-15', '2024-09-28', 4100, 'Alta', 'Manual');

INSERT INTO clientes (nombre, RUC_o_DNI, direccion_fiscal, telefono, correo_electronico, linea_credito) VALUES
('AgroMercado SA', '902345678', 'Calle 30 #15-40', '3145678901', 'ventas@agromercado.com', 2500000),
('Distribuidora Campo', '903456789', 'Av 25 #18-12', '3156789012', 'info@districampo.com', 1800000),
('Cosecha Directa', '904567890', 'Cra 40 #22-35', '3167890123', 'compras@cosechadirecta.com', 2200000),
('FreshProduce Ltda', '905678901', 'Calle 50 #30-18', '3178901234', 'logistica@freshproduce.com', 3500000);

INSERT INTO proveedores (nombre, RUC_o_DNI, direccion_fiscal, telefono, correo_electronico, credito, especialidad, condiciones_pago) VALUES
('AgroTech Colombia', '850123456', 'Parque Industrial 5', '3201234567', 'ventas@agrotech.com', 3500000, 'Maquinaria', '45 días'),
('Fertilizantes del Valle', '851234567', 'Zona Franca #8', '3212345678', 'info@fertivalle.com', 2800000, 'Fertilizantes', '30 días'),
('Semillas Andinas', '852345678', 'Calle 60 #12-20', '3223456789', 'comercial@semillasandinas.com', 2000000, 'Semillas', '20 días'),
('Control Fitosanitario', '853456789', 'Av Industrial #15', '3234567890', 'pedidos@controlfito.com', 3200000, 'Agroquímicos', '25 días');

INSERT INTO ventas (fecha, cliente, productos, cantidades, precio_unitario, descuentos, impuestos, forma_pago, total_facturado) VALUES
('2024-06-15', 4, 'Frijol', 4500, 1300, 110000, 160000, 'Transferencia', 5900000),
('2024-09-20', 5, 'Yuca', 5200, 900, 95000, 140000, 'Crédito', 4720000),
('2024-10-12', 6, 'Plátano', 5600, 1400, 130000, 210000, 'Efectivo', 7910000),
('2024-10-25', 7, 'Tomate', 3900, 1600, 105000, 185000, 'Transferencia', 6320000),
('2024-11-01', 4, 'Maíz', 4200, 1250, 98000, 155000, 'Crédito', 5307000),
('2024-11-08', 5, 'Arroz', 5000, 1550, 125000, 195000, 'Efectivo', 7820000);

INSERT INTO analisis_suelos (fecha_muestreo, parcela, ph, nitrogeno, fosforo, potasio, materia_organica, conductividad, nombre_laboratorio, recomendaciones) VALUES
('2024-02-10', 4, 6, 85, 62, 88, 4, 2, 'AgroLab', 'Mantener nivel de nutrientes'),
('2024-03-15', 5, 5, 68, 58, 82, 3, 3, 'EcoSuelo', 'Incrementar materia orgánica'),
('2024-04-08', 6, 7, 90, 70, 100, 5, 2, 'BioAnálisis', 'Reducir pH ligeramente'),
('2024-05-12', 7, 6, 78, 63, 92, 4, 2, 'AgroLab', 'Aplicar fertilizante balanceado'),
('2024-06-20', 8, 5, 72, 60, 87, 3, 3, 'EcoSuelo', 'Mejorar drenaje'),
('2024-07-25', 9, 6, 82, 67, 95, 4, 2, 'BioAnálisis', 'Condiciones óptimas'),
('2024-08-18', 10, 6, 79, 64, 91, 4, 2, 'AgroLab', 'Mantener programa actual');
USE Agrocontrol;

ALTER TABLE Fincas 
ADD COLUMN region VARCHAR(30);

UPDATE Fincas SET region = 'Valle Central' WHERE Finca_ID = 1;
UPDATE Fincas SET region = 'Zona Norte' WHERE Finca_ID = 2;
UPDATE Fincas SET region = 'Pacífico Sur' WHERE Finca_ID = 3;
UPDATE Fincas SET region = 'Valle Central' WHERE Finca_ID = 4;
UPDATE Fincas SET region = 'Zona Norte' WHERE Finca_ID = 5;
UPDATE Fincas SET region = 'Pacífico Sur' WHERE Finca_ID = 6;

INSERT INTO Fincas (Nombre, latitud, longitud, ubicacion, Hectareas, altitud, Temperatura, tipo_suelo, region) VALUES
('Hacienda San Pedro', 5.456789, -72.234567, 'Vereda Alto Bonito', 65, 310, 24, 'Franco', 'Valle Central'),
('La Pradera', 6.123456, -71.876543, 'Vereda Las Flores', 48, 280, 22, 'Arcilloso', 'Zona Norte'),
('Costa Verde', 4.654321, -74.123456, 'Vereda El Litoral', 70, 150, 28, 'Arenoso', 'Pacífico Sur'),
('El Mirador', 5.567890, -72.345678, 'Vereda La Cumbre', 42, 340, 20, 'Franco', 'Valle Central'),
('Río Claro', 6.234567, -71.765432, 'Vereda Agua Fría', 55, 295, 23, 'Arcilloso', 'Zona Norte'),
('Bella Vista', 4.543210, -74.234567, 'Vereda Playa Grande', 60, 180, 27, 'Arenoso', 'Pacífico Sur');

INSERT INTO Parcelas (Hectareas, sistema_riego, uso_id, finca_id) VALUES
(12, 'Goteo', 1, 7),
(10, 'Aspersión', 2, 7),
(8, 'Manual', 3, 7),
(14, 'Goteo', 4, 7),
(11, 'Aspersión', 5, 8),
(9, 'Manual', 1, 8),
(7, 'Goteo', 2, 8),
(15, 'Aspersión', 3, 9),
(13, 'Goteo', 4, 9),
(10, 'Manual', 5, 9),
(8, 'Aspersión', 1, 9),
(9, 'Goteo', 2, 10),
(11, 'Manual', 3, 10),
(12, 'Aspersión', 4, 10),
(10, 'Goteo', 5, 11),
(14, 'Manual', 1, 11),
(9, 'Aspersión', 2, 11),
(13, 'Goteo', 3, 12),
(11, 'Manual', 4, 12),
(12, 'Aspersión', 5, 12);

INSERT INTO historial_uso (parcela_id, uso_id, fecha_inicio, fecha_fin) VALUES
(14, 1, '2024-01-20', '2024-07-25'),
(15, 2, '2024-02-15', '2024-08-20'),
(16, 3, '2024-03-10', '2024-09-15'),
(17, 4, '2024-04-05', NULL),
(18, 5, '2024-05-12', NULL),
(19, 1, '2024-06-08', NULL),
(20, 2, '2024-07-15', NULL);

INSERT INTO temporada (parcela_id, cultivo_id, fecha_siembra, fecha_estimada_cosecha, densidad_siembra, rendimiento_esperado) VALUES
(14, 1, '2024-01-25', '2024-05-30', 205, 4700),
(15, 2, '2024-02-20', '2024-07-25', 185, 5400),
(16, 3, '2024-03-15', '2024-09-20', 215, 4300),
(17, 4, '2024-04-10', '2024-06-10', 225, 5000),
(18, 5, '2024-05-18', '2024-10-25', 195, 5600),
(19, 6, '2024-06-12', '2025-06-12', 160, 7500),
(20, 7, '2024-07-20', '2027-07-20', 140, 9000);

INSERT INTO area_asignada (empleado, tarea, parcela, fecha, horas_trabajadas, observaciones) VALUES
(1, 'Siembra', 14, '2024-01-26 07:00:00', 8, 'Densidad adecuada'),
(2, 'Fertilización', 15, '2024-03-10 08:00:00', 6, 'Aplicación completa'),
(3, 'Riego', 16, '2024-04-15 09:00:00', 5, 'Sistema funcional'),
(4, 'Control plagas', 17, '2024-05-20 07:30:00', 7, 'Sin infestación'),
(5, 'Cosecha', 18, '2024-10-28 06:00:00', 10, 'Calidad excelente'),
(6, 'Mantenimiento', 19, '2024-07-05 08:00:00', 6, 'Revisión general'),
(7, 'Supervisión', 20, '2024-08-12 08:00:00', 8, 'Todo conforme');

INSERT INTO analisis_suelos (fecha_muestreo, parcela, ph, nitrogeno, fosforo, potasio, materia_organica, conductividad, nombre_laboratorio, recomendaciones) VALUES
('2024-01-18', 14, 6, 83, 65, 93, 4, 2, 'AgroLab', 'Excelentes condiciones'),
('2024-02-12', 15, 5, 71, 59, 86, 3, 3, 'EcoSuelo', 'Aumentar materia orgánica'),
('2024-03-08', 16, 6, 87, 68, 97, 5, 2, 'BioAnálisis', 'Mantener programa'),
('2024-04-02', 17, 7, 92, 72, 102, 5, 2, 'AgroLab', 'Reducir pH levemente'),
('2024-05-10', 18, 6, 76, 62, 89, 4, 2, 'EcoSuelo', 'Aplicar NPK balanceado'),
('2024-06-05', 19, 5, 69, 56, 84, 3, 3, 'BioAnálisis', 'Mejorar fertilización'),
('2024-07-12', 20, 6, 81, 66, 94, 4, 2, 'AgroLab', 'Condiciones óptimas');