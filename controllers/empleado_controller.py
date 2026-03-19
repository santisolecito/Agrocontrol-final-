import os
from tkinter import messagebox
from models.empleado_model import EmpleadoModel
from views.empleado_view import FIELDS
from views.base_view import (build_panel, load_tree, make_buttons,
                              get_val, set_val, clear_entries, get_tree_data)
from utils.exportar_excel import exportar_excel
from utils.exportar_pdf   import exportar_pdf
from utils.validaciones   import (validar_campos, campo_requerido,
                                   longitud_valida, es_numero,
                                   es_dni_valido, es_telefono_valido,
                                   sin_caracteres_especiales)
from utils.imagen_handler import guardar_imagen

ASSETS_IMG = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                           "assets", "imagenes")

class EmpleadoController:
    def __init__(self, tab):
        _, self.entries, self.tree, self.sv, self.btn_frame = \
            build_panel(tab, "GESTIÓN DE EMPLEADOS", FIELDS, "#6b3d7a")
        make_buttons(self.btn_frame, self.save, self.update, self.delete,
                     lambda: clear_entries(self.entries), self.refresh,
                     excel_cmd=self.exportar_excel,
                     pdf_cmd=self.exportar_pdf)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.sv.trace_add("write", lambda *_: self.refresh())
        self.refresh()

    def refresh(self):
        result = EmpleadoModel.get_all()
        if result:
            rows, cols = result
            load_tree(self.tree, rows, cols, self.sv.get())

    def _on_select(self, event):
        sel = self.tree.selection()
        if not sel: return
        vals = self.tree.item(sel[0], "values")
        for k, v in zip(list(self.entries.keys()), vals):
            if k == "__img_estados__": break
            set_val(self.entries, k, v)

    def _validar(self):
        e = self.entries
        return validar_campos([
            (es_dni_valido,          get_val(e,"DNI")),
            (campo_requerido,        get_val(e,"Nombres"),   "Nombres"),
            (longitud_valida,        get_val(e,"Nombres"),   "Nombres", 2, 50),
            (sin_caracteres_especiales, get_val(e,"Nombres"),"Nombres"),
            (campo_requerido,        get_val(e,"Apellidos"), "Apellidos"),
            (longitud_valida,        get_val(e,"Apellidos"), "Apellidos", 2, 60),
            (es_telefono_valido,     get_val(e,"Teléfono")),
            (es_numero,              get_val(e,"Salario") or "0", "Salario"),
        ])

    def _guardar_foto(self, id_emp):
        estados = self.entries.get("__img_estados__", {})
        foto_estado = estados.get("Foto Empleado", {})
        ruta = foto_estado.get("ruta")
        if ruta:
            guardar_imagen(ruta, ASSETS_IMG, f"empleado_{id_emp}")

    def save(self):
        if not self._validar(): return
        e = self.entries
        if EmpleadoModel.insert(
            get_val(e,"DNI"), get_val(e,"Nombres"), get_val(e,"Apellidos"),
            get_val(e,"Fecha Nacimiento") or None,
            get_val(e,"Dirección"), get_val(e,"Teléfono"),
            get_val(e,"Especialidad"),
            get_val(e,"Fecha Contratación") or None,
            get_val(e,"Salario") or 0,
        ):
            self._guardar_foto("nuevo")
            messagebox.showinfo("✅ Empleado", "Empleado guardado correctamente.")
            clear_entries(e); self.refresh()

    def update(self):
        eid = get_val(self.entries, "Código Empleado")
        if not eid:
            messagebox.showwarning("Actualizar", "Selecciona un empleado."); return
        if not self._validar(): return
        if not messagebox.askyesno("Confirmar", f"¿Actualizar empleado ID {eid}?"): return
        e = self.entries
        if EmpleadoModel.update(
            eid, get_val(e,"DNI"), get_val(e,"Nombres"), get_val(e,"Apellidos"),
            get_val(e,"Fecha Nacimiento") or None,
            get_val(e,"Dirección"), get_val(e,"Teléfono"),
            get_val(e,"Especialidad"),
            get_val(e,"Fecha Contratación") or None,
            get_val(e,"Salario") or 0,
        ):
            self._guardar_foto(eid)
            messagebox.showinfo("✅ Empleado", "Empleado actualizado correctamente.")
            self.refresh()

    def delete(self):
        eid = get_val(self.entries, "Código Empleado")
        if not eid:
            messagebox.showwarning("Eliminar", "Selecciona un empleado."); return
        if messagebox.askyesno("⚠️ Confirmar eliminación",
                                f"¿Eliminar empleado ID {eid}?\nEsta acción no se puede deshacer."):
            if EmpleadoModel.delete(eid):
                messagebox.showinfo("✅ Empleado", "Empleado eliminado.")
                clear_entries(self.entries); self.refresh()

    def exportar_excel(self):
        cols, filas = get_tree_data(self.tree)
        exportar_excel("Empleados", cols, filas)

    def exportar_pdf(self):
        cols, filas = get_tree_data(self.tree)
        exportar_pdf("Empleados", cols, filas)
