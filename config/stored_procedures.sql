USE agrocontrol;

-- Cambiar el delimitador para los procedimientos
DELIMITER //

-- =====================================================
-- PROCEDIMIENTOS PARA FINCAS
-- =====================================================

-- 1. INSERTAR FINCA
DROP PROCEDURE IF EXISTS sp_InsertFinca //
CREATE PROCEDURE sp_InsertFinca(
    IN p_nombre       VARCHAR(100),
    IN p_ubicacion    VARCHAR(200),
    IN p_latitud      DECIMAL(10,6),
    IN p_longitud     DECIMAL(10,6),
    IN p_hectareas    DECIMAL(10,2),
    IN p_altitud      INT(11),
    IN p_temperatura  DECIMAL(5,2),
    IN p_tipo_suelo   VARCHAR(50),
    IN p_region       VARCHAR(100)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    INSERT INTO Fincas(Nombre, ubicacion, latitud, longitud, Hectareas, altitud, Temperatura, tipo_suelo, region)
    VALUES (p_nombre, p_ubicacion, p_latitud, p_longitud, p_hectareas, p_altitud, p_temperatura, p_tipo_suelo, p_region);

    COMMIT;

    SELECT LAST_INSERT_ID() AS Finca_ID, 'Finca insertada correctamente' AS Message;
END//

-- 2. ACTUALIZAR FINCA
DROP PROCEDURE IF EXISTS sp_UpdateFinca //
CREATE PROCEDURE sp_UpdateFinca(
    IN p_id           INT(11),
    IN p_nombre       VARCHAR(100),
    IN p_ubicacion    VARCHAR(200),
    IN p_latitud      DECIMAL(10,6),
    IN p_longitud     DECIMAL(10,6),
    IN p_hectareas    DECIMAL(10,2),
    IN p_altitud      INT(11),
    IN p_temperatura  DECIMAL(5,2),
    IN p_tipo_suelo   VARCHAR(50),
    IN p_region       VARCHAR(100)
)
BEGIN
    DECLARE v_count INT DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    SELECT COUNT(*) INTO v_count FROM Fincas WHERE Finca_ID = p_id;

    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La finca no existe';
    END IF;

    UPDATE Fincas
    SET Nombre=p_nombre, ubicacion=p_ubicacion, latitud=p_latitud,
        longitud=p_longitud, Hectareas=p_hectareas, altitud=p_altitud,
        Temperatura=p_temperatura, tipo_suelo=p_tipo_suelo, region=p_region
    WHERE Finca_ID = p_id;

    COMMIT;

    SELECT 'Finca actualizada correctamente' AS Message;
END//

-- 3. ELIMINAR FINCA
DROP PROCEDURE IF EXISTS sp_DeleteFinca //
CREATE PROCEDURE sp_DeleteFinca(
    IN p_id INT(11)
)
BEGIN
    DECLARE v_count INT DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    SELECT COUNT(*) INTO v_count FROM Fincas WHERE Finca_ID = p_id;

    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La finca no existe';
    END IF;

    DELETE FROM Fincas WHERE Finca_ID = p_id;

    COMMIT;

    SELECT 'Finca eliminada correctamente' AS Message;
END//

-- 4. OBTENER TODAS LAS FINCAS
DROP PROCEDURE IF EXISTS sp_GetAllFincas //
CREATE PROCEDURE sp_GetAllFincas()
BEGIN
    SELECT Finca_ID, Nombre, ubicacion, Hectareas, altitud, Temperatura, tipo_suelo, region
    FROM Fincas
    ORDER BY Nombre;
END//

-- 5. BUSCAR FINCAS
DROP PROCEDURE IF EXISTS sp_SearchFincas //
CREATE PROCEDURE sp_SearchFincas(
    IN p_termino VARCHAR(100)
)
BEGIN
    SELECT Finca_ID, Nombre, ubicacion, Hectareas, altitud, Temperatura, tipo_suelo, region
    FROM Fincas
    WHERE Nombre LIKE CONCAT('%', p_termino, '%')
       OR ubicacion LIKE CONCAT('%', p_termino, '%')
       OR region LIKE CONCAT('%', p_termino, '%')
    ORDER BY Nombre;
END//

-- =====================================================
-- PROCEDIMIENTOS PARA CULTIVOS
-- =====================================================

-- 1. INSERTAR CULTIVO
DROP PROCEDURE IF EXISTS sp_InsertCultivo //
CREATE PROCEDURE sp_InsertCultivo(
    IN p_nombre_cientifico  VARCHAR(150),
    IN p_nombre_comun       VARCHAR(100),
    IN p_tiempo_crecimiento INT(11),
    IN p_temperatura_optima DECIMAL(5,2),
    IN p_agua               DECIMAL(10,2)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    INSERT INTO cultivos(nombre_cientifico, nombre_comun, tiempo_crecimiento, temperatura_optima, agua)
    VALUES (p_nombre_cientifico, p_nombre_comun, p_tiempo_crecimiento, p_temperatura_optima, p_agua);

    COMMIT;

    SELECT LAST_INSERT_ID() AS cultivo_id, 'Cultivo insertado correctamente' AS Message;
END//

-- 2. ACTUALIZAR CULTIVO
DROP PROCEDURE IF EXISTS sp_UpdateCultivo //
CREATE PROCEDURE sp_UpdateCultivo(
    IN p_id                 INT(11),
    IN p_nombre_cientifico  VARCHAR(150),
    IN p_nombre_comun       VARCHAR(100),
    IN p_tiempo_crecimiento INT(11),
    IN p_temperatura_optima DECIMAL(5,2),
    IN p_agua               DECIMAL(10,2)
)
BEGIN
    DECLARE v_count INT DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    SELECT COUNT(*) INTO v_count FROM cultivos WHERE cultivo_id = p_id;

    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El cultivo no existe';
    END IF;

    UPDATE cultivos
    SET nombre_cientifico=p_nombre_cientifico, nombre_comun=p_nombre_comun,
        tiempo_crecimiento=p_tiempo_crecimiento, temperatura_optima=p_temperatura_optima,
        agua=p_agua
    WHERE cultivo_id = p_id;

    COMMIT;

    SELECT 'Cultivo actualizado correctamente' AS Message;
END//

-- 3. ELIMINAR CULTIVO
DROP PROCEDURE IF EXISTS sp_DeleteCultivo //
CREATE PROCEDURE sp_DeleteCultivo(
    IN p_id INT(11)
)
BEGIN
    DECLARE v_count INT DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    SELECT COUNT(*) INTO v_count FROM cultivos WHERE cultivo_id = p_id;

    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El cultivo no existe';
    END IF;

    -- Verificar si el cultivo está asociado a cosechas
    SELECT COUNT(*) INTO v_count FROM cosecha WHERE cultivo = p_id;

    IF v_count > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No se puede eliminar: el cultivo tiene cosechas asociadas';
    END IF;

    DELETE FROM cultivos WHERE cultivo_id = p_id;

    COMMIT;

    SELECT 'Cultivo eliminado correctamente' AS Message;
END//

-- 4. OBTENER TODOS LOS CULTIVOS
DROP PROCEDURE IF EXISTS sp_GetAllCultivos //
CREATE PROCEDURE sp_GetAllCultivos()
BEGIN
    SELECT cultivo_id, nombre_cientifico, nombre_comun, tiempo_crecimiento, temperatura_optima, agua
    FROM cultivos
    ORDER BY nombre_comun;
END//

-- 5. BUSCAR CULTIVOS
DROP PROCEDURE IF EXISTS sp_SearchCultivos //
CREATE PROCEDURE sp_SearchCultivos(
    IN p_termino VARCHAR(100)
)
BEGIN
    SELECT cultivo_id, nombre_cientifico, nombre_comun, tiempo_crecimiento, temperatura_optima, agua
    FROM cultivos
    WHERE nombre_comun LIKE CONCAT('%', p_termino, '%')
       OR nombre_cientifico LIKE CONCAT('%', p_termino, '%')
    ORDER BY nombre_comun;
END//

-- =====================================================
-- PROCEDIMIENTOS PARA INVENTARIO (INSUMOS)
-- =====================================================

-- 1. INSERTAR INSUMO
DROP PROCEDURE IF EXISTS sp_InsertInsumo //
CREATE PROCEDURE sp_InsertInsumo(
    IN p_nombre_comercial VARCHAR(150),
    IN p_tipo             VARCHAR(50),
    IN p_unidad_medida    VARCHAR(30),
    IN p_ubicacion        VARCHAR(100),
    IN p_cantidad_stok    DECIMAL(10,2),
    IN p_fecha_caducidad  DATE,
    IN p_precio           DECIMAL(10,2)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    INSERT INTO inventario(nombre_comercial, Tipo, unidad_medida, ubicacion, cantidad_stok, fecha_caducidad, precio)
    VALUES (p_nombre_comercial, p_tipo, p_unidad_medida, p_ubicacion, p_cantidad_stok, p_fecha_caducidad, p_precio);

    COMMIT;

    SELECT LAST_INSERT_ID() AS Codigo_id, 'Insumo insertado correctamente' AS Message;
END//

-- 2. ACTUALIZAR INSUMO
DROP PROCEDURE IF EXISTS sp_UpdateInsumo //
CREATE PROCEDURE sp_UpdateInsumo(
    IN p_id               INT(11),
    IN p_nombre_comercial VARCHAR(150),
    IN p_tipo             VARCHAR(50),
    IN p_unidad_medida    VARCHAR(30),
    IN p_ubicacion        VARCHAR(100),
    IN p_cantidad_stok    DECIMAL(10,2),
    IN p_fecha_caducidad  DATE,
    IN p_precio           DECIMAL(10,2)
)
BEGIN
    DECLARE v_count INT DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    SELECT COUNT(*) INTO v_count FROM inventario WHERE Codigo_id = p_id;

    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El insumo no existe';
    END IF;

    UPDATE inventario
    SET nombre_comercial=p_nombre_comercial, Tipo=p_tipo, unidad_medida=p_unidad_medida,
        ubicacion=p_ubicacion, cantidad_stok=p_cantidad_stok,
        fecha_caducidad=p_fecha_caducidad, precio=p_precio
    WHERE Codigo_id = p_id;

    COMMIT;

    SELECT 'Insumo actualizado correctamente' AS Message;
END//

-- 3. ELIMINAR INSUMO
DROP PROCEDURE IF EXISTS sp_DeleteInsumo //
CREATE PROCEDURE sp_DeleteInsumo(
    IN p_id INT(11)
)
BEGIN
    DECLARE v_count INT DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    SELECT COUNT(*) INTO v_count FROM inventario WHERE Codigo_id = p_id;

    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El insumo no existe';
    END IF;

    DELETE FROM inventario WHERE Codigo_id = p_id;

    COMMIT;

    SELECT 'Insumo eliminado correctamente' AS Message;
END//

-- 4. OBTENER TODOS LOS INSUMOS
DROP PROCEDURE IF EXISTS sp_GetAllInsumos //
CREATE PROCEDURE sp_GetAllInsumos()
BEGIN
    SELECT Codigo_id, nombre_comercial, Tipo, unidad_medida, cantidad_stok, ubicacion, fecha_caducidad, precio
    FROM inventario
    ORDER BY nombre_comercial;
END//

-- 5. BUSCAR INSUMOS
DROP PROCEDURE IF EXISTS sp_SearchInsumos //
CREATE PROCEDURE sp_SearchInsumos(
    IN p_termino VARCHAR(100)
)
BEGIN
    SELECT Codigo_id, nombre_comercial, Tipo, unidad_medida, cantidad_stok, ubicacion, fecha_caducidad, precio
    FROM inventario
    WHERE nombre_comercial LIKE CONCAT('%', p_termino, '%')
       OR Tipo LIKE CONCAT('%', p_termino, '%')
    ORDER BY nombre_comercial;
END//

-- =====================================================
-- PROCEDIMIENTOS PARA MAQUINARIA
-- =====================================================

-- 1. INSERTAR MAQUINARIA
DROP PROCEDURE IF EXISTS sp_InsertMaquinaria //
CREATE PROCEDURE sp_InsertMaquinaria(
    IN p_marca            VARCHAR(100),
    IN p_modelo           VARCHAR(100),
    IN p_anio_fabricacion INT(11),
    IN p_potencia         DECIMAL(8,2),
    IN p_tipo_combustible VARCHAR(30),
    IN p_horometro        DECIMAL(10,2),
    IN p_estado           VARCHAR(50)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    INSERT INTO maquinaria(marca, modelo, anio_fabricacion, potencia, tipo_combustible, horometro, estado)
    VALUES (p_marca, p_modelo, p_anio_fabricacion, p_potencia, p_tipo_combustible, p_horometro, p_estado);

    COMMIT;

    SELECT LAST_INSERT_ID() AS codigo_maquina, 'Maquinaria insertada correctamente' AS Message;
END//

-- 2. ACTUALIZAR MAQUINARIA
DROP PROCEDURE IF EXISTS sp_UpdateMaquinaria //
CREATE PROCEDURE sp_UpdateMaquinaria(
    IN p_id               INT(11),
    IN p_marca            VARCHAR(100),
    IN p_modelo           VARCHAR(100),
    IN p_anio_fabricacion INT(11),
    IN p_potencia         DECIMAL(8,2),
    IN p_tipo_combustible VARCHAR(30),
    IN p_horometro        DECIMAL(10,2),
    IN p_estado           VARCHAR(50)
)
BEGIN
    DECLARE v_count INT DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    SELECT COUNT(*) INTO v_count FROM maquinaria WHERE codigo_maquina = p_id;

    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La maquinaria no existe';
    END IF;

    UPDATE maquinaria
    SET marca=p_marca, modelo=p_modelo, anio_fabricacion=p_anio_fabricacion,
        potencia=p_potencia, tipo_combustible=p_tipo_combustible,
        horometro=p_horometro, estado=p_estado
    WHERE codigo_maquina = p_id;

    COMMIT;

    SELECT 'Maquinaria actualizada correctamente' AS Message;
END//

-- 3. ELIMINAR MAQUINARIA
DROP PROCEDURE IF EXISTS sp_DeleteMaquinaria //
CREATE PROCEDURE sp_DeleteMaquinaria(
    IN p_id INT(11)
)
BEGIN
    DECLARE v_count INT DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    SELECT COUNT(*) INTO v_count FROM maquinaria WHERE codigo_maquina = p_id;

    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La maquinaria no existe';
    END IF;

    DELETE FROM maquinaria WHERE codigo_maquina = p_id;

    COMMIT;

    SELECT 'Maquinaria eliminada correctamente' AS Message;
END//

-- 4. OBTENER TODA LA MAQUINARIA
DROP PROCEDURE IF EXISTS sp_GetAllMaquinaria //
CREATE PROCEDURE sp_GetAllMaquinaria()
BEGIN
    SELECT codigo_maquina, marca, modelo, anio_fabricacion, potencia, tipo_combustible, horometro, estado
    FROM maquinaria
    ORDER BY marca, modelo;
END//

-- 5. BUSCAR MAQUINARIA
DROP PROCEDURE IF EXISTS sp_SearchMaquinaria //
CREATE PROCEDURE sp_SearchMaquinaria(
    IN p_termino VARCHAR(100)
)
BEGIN
    SELECT codigo_maquina, marca, modelo, anio_fabricacion, potencia, tipo_combustible, horometro, estado
    FROM maquinaria
    WHERE marca LIKE CONCAT('%', p_termino, '%')
       OR modelo LIKE CONCAT('%', p_termino, '%')
       OR estado LIKE CONCAT('%', p_termino, '%')
    ORDER BY marca, modelo;
END//

-- =====================================================
-- PROCEDIMIENTOS PARA EMPLEADOS
-- =====================================================

-- 1. INSERTAR EMPLEADO
DROP PROCEDURE IF EXISTS sp_InsertEmpleado //
CREATE PROCEDURE sp_InsertEmpleado(
    IN p_dni                VARCHAR(20),
    IN p_nombres            VARCHAR(100),
    IN p_apellidos          VARCHAR(100),
    IN p_fecha_nacimiento   DATE,
    IN p_direccion          VARCHAR(200),
    IN p_telefono           VARCHAR(20),
    IN p_especialidad       VARCHAR(80),
    IN p_fecha_contratacion DATE,
    IN p_salario            DECIMAL(10,2)
)
BEGIN
    DECLARE v_count INT DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    -- Verificar que el DNI no esté duplicado
    SELECT COUNT(*) INTO v_count FROM empleados WHERE DNI = p_dni;

    IF v_count > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Ya existe un empleado con ese DNI';
    END IF;

    INSERT INTO empleados(DNI, nombres, apellidos, fecha_nacimiento, direccion,
                          telefono, especialidad, fecha_contratacion, salario)
    VALUES (p_dni, p_nombres, p_apellidos, p_fecha_nacimiento, p_direccion,
            p_telefono, p_especialidad, p_fecha_contratacion, p_salario);

    COMMIT;

    SELECT LAST_INSERT_ID() AS empleados_id, 'Empleado insertado correctamente' AS Message;
END//

-- 2. ACTUALIZAR EMPLEADO
DROP PROCEDURE IF EXISTS sp_UpdateEmpleado //
CREATE PROCEDURE sp_UpdateEmpleado(
    IN p_id                 INT(11),
    IN p_dni                VARCHAR(20),
    IN p_nombres            VARCHAR(100),
    IN p_apellidos          VARCHAR(100),
    IN p_fecha_nacimiento   DATE,
    IN p_direccion          VARCHAR(200),
    IN p_telefono           VARCHAR(20),
    IN p_especialidad       VARCHAR(80),
    IN p_fecha_contratacion DATE,
    IN p_salario            DECIMAL(10,2)
)
BEGIN
    DECLARE v_count INT DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    SELECT COUNT(*) INTO v_count FROM empleados WHERE empleados_id = p_id;

    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El empleado no existe';
    END IF;

    UPDATE empleados
    SET DNI=p_dni, nombres=p_nombres, apellidos=p_apellidos,
        fecha_nacimiento=p_fecha_nacimiento, direccion=p_direccion,
        telefono=p_telefono, especialidad=p_especialidad,
        fecha_contratacion=p_fecha_contratacion, salario=p_salario
    WHERE empleados_id = p_id;

    COMMIT;

    SELECT 'Empleado actualizado correctamente' AS Message;
END//

-- 3. ELIMINAR EMPLEADO
DROP PROCEDURE IF EXISTS sp_DeleteEmpleado //
CREATE PROCEDURE sp_DeleteEmpleado(
    IN p_id INT(11)
)
BEGIN
    DECLARE v_count INT DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    SELECT COUNT(*) INTO v_count FROM empleados WHERE empleados_id = p_id;

    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El empleado no existe';
    END IF;

    DELETE FROM empleados WHERE empleados_id = p_id;

    COMMIT;

    SELECT 'Empleado eliminado correctamente' AS Message;
END//

-- 4. OBTENER TODOS LOS EMPLEADOS
DROP PROCEDURE IF EXISTS sp_GetAllEmpleados //
CREATE PROCEDURE sp_GetAllEmpleados()
BEGIN
    SELECT empleados_id, DNI, nombres, apellidos, fecha_nacimiento,
           direccion, telefono, especialidad, fecha_contratacion, salario
    FROM empleados
    ORDER BY apellidos, nombres;
END//

-- 5. BUSCAR EMPLEADOS
DROP PROCEDURE IF EXISTS sp_SearchEmpleados //
CREATE PROCEDURE sp_SearchEmpleados(
    IN p_termino VARCHAR(100)
)
BEGIN
    SELECT empleados_id, DNI, nombres, apellidos, fecha_nacimiento,
           direccion, telefono, especialidad, fecha_contratacion, salario
    FROM empleados
    WHERE nombres LIKE CONCAT('%', p_termino, '%')
       OR apellidos LIKE CONCAT('%', p_termino, '%')
       OR DNI LIKE CONCAT('%', p_termino, '%')
       OR especialidad LIKE CONCAT('%', p_termino, '%')
    ORDER BY apellidos, nombres;
END//

-- =====================================================
-- PROCEDIMIENTOS PARA COSECHAS
-- =====================================================

-- 1. INSERTAR COSECHA
DROP PROCEDURE IF EXISTS sp_InsertCosecha //
CREATE PROCEDURE sp_InsertCosecha(
    IN p_parcela          INT(11),
    IN p_cultivo          INT(11),
    IN p_inicio           DATE,
    IN p_fin              DATE,
    IN p_cantidad         DECIMAL(10,2),
    IN p_calidad_producto VARCHAR(30),
    IN p_metodo_cosecha   VARCHAR(30)
)
BEGIN
    DECLARE v_count INT DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    -- Verificar que el cultivo exista
    SELECT COUNT(*) INTO v_count FROM cultivos WHERE cultivo_id = p_cultivo;

    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El cultivo indicado no existe';
    END IF;

    INSERT INTO cosecha(parcela, cultivo, inicio, fin, cantidad, calidad_producto, metodo_cosecha)
    VALUES (p_parcela, p_cultivo, p_inicio, p_fin, p_cantidad, p_calidad_producto, p_metodo_cosecha);

    COMMIT;

    SELECT LAST_INSERT_ID() AS cosecha_id, 'Cosecha registrada correctamente' AS Message;
END//

-- 2. ACTUALIZAR COSECHA
DROP PROCEDURE IF EXISTS sp_UpdateCosecha //
CREATE PROCEDURE sp_UpdateCosecha(
    IN p_id               INT(11),
    IN p_parcela          INT(11),
    IN p_cultivo          INT(11),
    IN p_inicio           DATE,
    IN p_fin              DATE,
    IN p_cantidad         DECIMAL(10,2),
    IN p_calidad_producto VARCHAR(30),
    IN p_metodo_cosecha   VARCHAR(30)
)
BEGIN
    DECLARE v_count INT DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    SELECT COUNT(*) INTO v_count FROM cosecha WHERE cosecha_id = p_id;

    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La cosecha no existe';
    END IF;

    UPDATE cosecha
    SET parcela=p_parcela, cultivo=p_cultivo, inicio=p_inicio, fin=p_fin,
        cantidad=p_cantidad, calidad_producto=p_calidad_producto,
        metodo_cosecha=p_metodo_cosecha
    WHERE cosecha_id = p_id;

    COMMIT;

    SELECT 'Cosecha actualizada correctamente' AS Message;
END//

-- 3. ELIMINAR COSECHA
DROP PROCEDURE IF EXISTS sp_DeleteCosecha //
CREATE PROCEDURE sp_DeleteCosecha(
    IN p_id INT(11)
)
BEGIN
    DECLARE v_count INT DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    SELECT COUNT(*) INTO v_count FROM cosecha WHERE cosecha_id = p_id;

    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La cosecha no existe';
    END IF;

    DELETE FROM cosecha WHERE cosecha_id = p_id;

    COMMIT;

    SELECT 'Cosecha eliminada correctamente' AS Message;
END//

-- 4. OBTENER TODAS LAS COSECHAS
DROP PROCEDURE IF EXISTS sp_GetAllCosechas //
CREATE PROCEDURE sp_GetAllCosechas()
BEGIN
    SELECT cosecha_id, parcela, cultivo, inicio, fin,
           cantidad, calidad_producto, metodo_cosecha
    FROM cosecha
    ORDER BY inicio DESC;
END//

-- 5. BUSCAR COSECHAS
DROP PROCEDURE IF EXISTS sp_SearchCosechas //
CREATE PROCEDURE sp_SearchCosechas(
    IN p_termino VARCHAR(100)
)
BEGIN
    SELECT cosecha_id, parcela, cultivo, inicio, fin,
           cantidad, calidad_producto, metodo_cosecha
    FROM cosecha
    WHERE calidad_producto LIKE CONCAT('%', p_termino, '%')
       OR metodo_cosecha LIKE CONCAT('%', p_termino, '%')
    ORDER BY inicio DESC;
END//

-- =====================================================
-- PROCEDIMIENTOS PARA CLIENTES
-- =====================================================

-- 1. INSERTAR CLIENTE
DROP PROCEDURE IF EXISTS sp_InsertCliente //
CREATE PROCEDURE sp_InsertCliente(
    IN p_nombre           VARCHAR(150),
    IN p_ruc_dni          VARCHAR(20),
    IN p_direccion_fiscal VARCHAR(200),
    IN p_telefono         VARCHAR(20),
    IN p_correo           VARCHAR(100),
    IN p_linea_credito    DECIMAL(12,2)
)
BEGIN
    DECLARE v_count INT DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    -- Verificar que el RUC/DNI no esté duplicado
    SELECT COUNT(*) INTO v_count FROM clientes WHERE RUC_o_DNI = p_ruc_dni;

    IF v_count > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Ya existe un cliente con ese RUC/DNI';
    END IF;

    INSERT INTO clientes(nombre, RUC_o_DNI, direccion_fiscal, telefono, correo_electronico, linea_credito)
    VALUES (p_nombre, p_ruc_dni, p_direccion_fiscal, p_telefono, p_correo, p_linea_credito);

    COMMIT;

    SELECT LAST_INSERT_ID() AS cliente_id, 'Cliente insertado correctamente' AS Message;
END//

-- 2. ACTUALIZAR CLIENTE
DROP PROCEDURE IF EXISTS sp_UpdateCliente //
CREATE PROCEDURE sp_UpdateCliente(
    IN p_id               INT(11),
    IN p_nombre           VARCHAR(150),
    IN p_ruc_dni          VARCHAR(20),
    IN p_direccion_fiscal VARCHAR(200),
    IN p_telefono         VARCHAR(20),
    IN p_correo           VARCHAR(100),
    IN p_linea_credito    DECIMAL(12,2)
)
BEGIN
    DECLARE v_count INT DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    SELECT COUNT(*) INTO v_count FROM clientes WHERE cliente_id = p_id;

    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El cliente no existe';
    END IF;

    UPDATE clientes
    SET nombre=p_nombre, RUC_o_DNI=p_ruc_dni, direccion_fiscal=p_direccion_fiscal,
        telefono=p_telefono, correo_electronico=p_correo, linea_credito=p_linea_credito
    WHERE cliente_id = p_id;

    COMMIT;

    SELECT 'Cliente actualizado correctamente' AS Message;
END//

-- 3. ELIMINAR CLIENTE
DROP PROCEDURE IF EXISTS sp_DeleteCliente //
CREATE PROCEDURE sp_DeleteCliente(
    IN p_id INT(11)
)
BEGIN
    DECLARE v_count INT DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    SELECT COUNT(*) INTO v_count FROM clientes WHERE cliente_id = p_id;

    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El cliente no existe';
    END IF;

    DELETE FROM clientes WHERE cliente_id = p_id;

    COMMIT;

    SELECT 'Cliente eliminado correctamente' AS Message;
END//

-- 4. OBTENER TODOS LOS CLIENTES
DROP PROCEDURE IF EXISTS sp_GetAllClientes //
CREATE PROCEDURE sp_GetAllClientes()
BEGIN
    SELECT cliente_id, nombre, RUC_o_DNI, direccion_fiscal,
           telefono, correo_electronico, linea_credito
    FROM clientes
    ORDER BY nombre;
END//

-- 5. BUSCAR CLIENTES
DROP PROCEDURE IF EXISTS sp_SearchClientes //
CREATE PROCEDURE sp_SearchClientes(
    IN p_termino VARCHAR(100)
)
BEGIN
    SELECT cliente_id, nombre, RUC_o_DNI, direccion_fiscal,
           telefono, correo_electronico, linea_credito
    FROM clientes
    WHERE nombre LIKE CONCAT('%', p_termino, '%')
       OR RUC_o_DNI LIKE CONCAT('%', p_termino, '%')
       OR correo_electronico LIKE CONCAT('%', p_termino, '%')
    ORDER BY nombre;
END//


DELIMITER ;

