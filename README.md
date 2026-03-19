# 🌿 AgroControl — Campos Fértiles S.A.

Sistema de gestión agrícola de escritorio desarrollado en Python con arquitectura MVC.

## Requisitos

- Python 3.10+
- MySQL Server corriendo en localhost
- Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Configuración de la base de datos

1. Abrir MySQL y ejecutar primero:
   ```
   config/agrocontrol.sql
   ```
2. Luego ejecutar:
   ```
   config/stored_procedures.sql
   ```

## Ejecutar la aplicación

```bash
python main.py
```

## Estructura del proyecto

```
agrocontrol/
├── main.py
├── requirements.txt
├── config/          → conexión a BD + scripts SQL
├── models/          → acceso a datos (stored procedures)
├── views/           → interfaz gráfica (Tkinter)
├── controllers/     → lógica que conecta vista y modelo
├── utils/           → exportación Excel/PDF, validaciones, imágenes
└── assets/          → favicon, logo, imágenes
```

## Módulos

| Módulo      | Descripción                          |
|-------------|--------------------------------------|
| Fincas      | Gestión de fincas y propiedades      |
| Cultivos    | Registro de tipos de cultivo         |
| Insumos     | Inventario de insumos agrícolas      |
| Maquinaria  | Control de equipos y maquinaria      |
| Empleados   | Gestión del personal                 |
| Cosechas    | Registro de cosechas por parcela     |
| Clientes    | Base de datos de clientes            |
