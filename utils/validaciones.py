"""
utils/validaciones.py
Validaciones reutilizables para todos los controllers.
"""
import re
from tkinter import messagebox


# ── Numéricos ─────────────────────────────────────────────────────────────
def es_numero(valor: str, campo: str = "Campo") -> bool:
    """Valida que el valor sea numérico entero o decimal."""
    try:
        float(valor)
        return True
    except (ValueError, TypeError):
        messagebox.showerror("❌ Validación",
                             f"'{campo}' solo acepta valores numéricos.\n"
                             f"Valor ingresado: '{valor}'")
        return False


def es_entero(valor: str, campo: str = "Campo") -> bool:
    """Valida que el valor sea un número entero."""
    try:
        int(valor)
        return True
    except (ValueError, TypeError):
        messagebox.showerror("❌ Validación",
                             f"'{campo}' solo acepta números enteros.\n"
                             f"Valor ingresado: '{valor}'")
        return False


def es_positivo(valor: str, campo: str = "Campo") -> bool:
    """Valida que el número sea mayor o igual a cero."""
    try:
        if float(valor) < 0:
            messagebox.showerror("❌ Validación",
                                 f"'{campo}' no puede ser negativo.")
            return False
        return True
    except (ValueError, TypeError):
        messagebox.showerror("❌ Validación",
                             f"'{campo}' debe ser un número positivo.")
        return False


# ── Texto ─────────────────────────────────────────────────────────────────
def campo_requerido(valor: str, campo: str = "Campo") -> bool:
    """Valida que el campo no esté vacío."""
    if not valor or not valor.strip():
        messagebox.showerror("❌ Campo requerido",
                             f"El campo '{campo}' es obligatorio.")
        return False
    return True


def longitud_valida(valor: str, campo: str = "Campo",
                    minimo: int = 2, maximo: int = 100) -> bool:
    """Valida longitud mínima y máxima."""
    largo = len(valor.strip())
    if largo < minimo:
        messagebox.showerror("❌ Validación",
                             f"'{campo}' debe tener al menos {minimo} caracteres "
                             f"(actual: {largo}).")
        return False
    if largo > maximo:
        messagebox.showerror("❌ Validación",
                             f"'{campo}' no puede superar {maximo} caracteres "
                             f"(actual: {largo}).")
        return False
    return True


def sin_caracteres_especiales(valor: str, campo: str = "Campo") -> bool:
    """Rechaza caracteres especiales peligrosos (<, >, ;, ', \", \\)."""
    patron = r'[<>;\'\"\\]'
    if re.search(patron, valor):
        messagebox.showerror("❌ Validación",
                             f"'{campo}' contiene caracteres no permitidos "
                             f"(< > ; ' \" \\).")
        return False
    return True


# ── Email ─────────────────────────────────────────────────────────────────
def es_email_valido(email: str) -> bool:
    """Valida formato de correo electrónico con regex."""
    patron = r'^[\w\.\-\+]+@[\w\-]+\.[a-zA-Z]{2,}$'
    if re.match(patron, email.strip()):
        return True
    messagebox.showerror("❌ Email inválido",
                         f"El correo '{email}' no tiene formato válido.\n"
                         f"Ejemplo correcto: usuario@dominio.com")
    return False


# ── Fecha ─────────────────────────────────────────────────────────────────
def es_fecha_valida(valor: str, campo: str = "Fecha") -> bool:
    """Valida que la fecha tenga formato YYYY-MM-DD."""
    from datetime import datetime
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            datetime.strptime(valor.strip(), fmt)
            return True
        except ValueError:
            continue
    messagebox.showerror("❌ Fecha inválida",
                         f"'{campo}' debe tener formato YYYY-MM-DD.\n"
                         f"Ejemplo: 2024-05-15")
    return False


# ── DNI / RUC ─────────────────────────────────────────────────────────────
def es_dni_valido(valor: str) -> bool:
    """Valida que el DNI/RUC sea numérico y tenga entre 8 y 15 dígitos."""
    v = valor.strip()
    if not v.isdigit():
        messagebox.showerror("❌ Validación",
                             "El DNI/RUC solo debe contener dígitos numéricos.")
        return False
    if not (8 <= len(v) <= 15):
        messagebox.showerror("❌ Validación",
                             f"El DNI/RUC debe tener entre 8 y 15 dígitos "
                             f"(actual: {len(v)}).")
        return False
    return True


# ── Teléfono ──────────────────────────────────────────────────────────────
def es_telefono_valido(valor: str) -> bool:
    """Valida que el teléfono tenga entre 7 y 15 dígitos (con o sin +)."""
    v = re.sub(r'[\s\-\(\)]', '', valor.strip())
    patron = r'^\+?[0-9]{7,15}$'
    if re.match(patron, v):
        return True
    messagebox.showerror("❌ Teléfono inválido",
                         "El teléfono debe tener entre 7 y 15 dígitos.")
    return False


# ── Validador de bloque completo ──────────────────────────────────────────
def validar_campos(reglas: list) -> bool:
    """
    Ejecuta una lista de validaciones en secuencia.
    Cada regla es una tupla (funcion, *args).
    Retorna True solo si TODAS pasan.

    Ejemplo:
        validar_campos([
            (campo_requerido, nombre, "Nombre"),
            (longitud_valida, nombre, "Nombre", 2, 50),
            (es_numero,       salario, "Salario"),
        ])
    """
    for regla in reglas:
        fn, *args = regla
        if not fn(*args):
            return False
    return True
