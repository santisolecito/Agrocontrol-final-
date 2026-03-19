import mysql.connector
from mysql.connector import Error
from tkinter import messagebox
from config.db_config import DB_CONFIG


def get_connection():
    """Retorna una conexión activa a la base de datos."""
    return mysql.connector.connect(**DB_CONFIG)


def ejecutar(sql, params=(), fetch=False):
    """
    Ejecuta una sentencia SQL (directa o CALL de procedimiento almacenado).

    Parámetros:
        sql    : cadena SQL o CALL sp_Nombre(%s,...)
        params : tupla de parámetros
        fetch  : True → devuelve (filas, columnas); False → ejecuta y commitea

    Retorna:
        - (rows, col_names) si fetch=True
        - True              si fetch=False y todo fue bien
        - None              si ocurre un error
    """
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute(sql, params)

        if fetch:
            result    = cur.fetchall()
            col_names = [d[0] for d in cur.description] if cur.description else []
            while conn.unread_result:
                cur.fetchall()
            cur.close()
            conn.close()
            return result, col_names

        # Consumir todos los result-sets que devuelve el procedimiento
        while True:
            try:
                cur.fetchall()
            except Exception:
                pass
            if not cur.nextset():
                break

        conn.commit()
        cur.close()
        conn.close()
        return True

    except Error as e:
        messagebox.showerror("Error de Base de Datos", str(e))
        return None
