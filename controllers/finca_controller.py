import os
from tkinter import messagebox
from models.finca_model import FincaModel
from views.finca_view import FIELDS
from views.base_view import (build_panel, load_tree, make_buttons,
                              get_val, set_val, clear_entries, get_tree_data)
from utils.exportar_excel import exportar_excel
from utils.exportar_pdf   import exportar_pdf
from utils.validaciones   import (validar_campos, campo_requerido,
                                   longitud_valida, es_numero,
                                   sin_caracteres_especiales)
from utils.imagen_handler import guardar_imagen

ASSETS_IMG = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                           "assets", "imagenes")

class FincaController:
    def __init__(self, tab):
        _, self.entries, self.tree, self.sv, self.btn_frame = \
            build_panel(tab, "GESTIÓN DE FINCAS", FIELDS, "#2d5a27")
        make_buttons(self.btn_frame, self.save, self.update, self.delete,
                     lambda: clear_entries(self.entries), self.refresh,
                     excel_cmd=self.exportar_excel,
                     pdf_cmd=self.exportar_pdf)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.sv.trace_add("write", lambda *_: self.refresh())
        self.refresh()

    def refresh(self):
        result = FincaModel.get_all()
        if result:
            rows, cols = result
            load_tree(self.tree, rows, cols, self.sv.get())

    def _on_select(self, event):
        sel = self.tree.selection()
        if not sel: return
        vals = self.tree.item(sel[0], "values")
        keys = ["Código Finca","Nombre","Ubicación","Extensión (ha)",
                "Altitud (msnm)","Temp. Promedio (°C)","Tipo de Suelo","Región"]
        for k, v in zip(keys, vals):
            set_val(self.entries, k, v)

    def _validar(self):
        e = self.entries
        return validar_campos([
            (campo_requerido,        get_val(e,"Nombre"),         "Nombre"),
            (longitud_valida,        get_val(e,"Nombre"),         "Nombre", 2, 50),
            (sin_caracteres_especiales, get_val(e,"Nombre"),      "Nombre"),
            (campo_requerido,        get_val(e,"Ubicación"),      "Ubicación"),
            (es_numero,              get_val(e,"Extensión (ha)") or "0", "Extensión (ha)"),
            (es_numero,              get_val(e,"Altitud (msnm)") or "0", "Altitud (msnm)"),
            (es_numero,              get_val(e,"Temp. Promedio (°C)") or "0", "Temp. Promedio (°C)"),
        ])

    def _guardar_foto(self, id_finca):
        estados = self.entries.get("__img_estados__", {})
        foto_estado = estados.get("Fotografía", {})
        ruta = foto_estado.get("ruta")
        if ruta:
            guardar_imagen(ruta, ASSETS_IMG, f"finca_{id_finca}")

    def save(self):
        if not self._validar(): return
        e = self.entries
        resultado = FincaModel.insert(
            get_val(e,"Nombre"), get_val(e,"Ubicación"),
            get_val(e,"Latitud") or None, get_val(e,"Longitud") or None,
            get_val(e,"Extensión (ha)") or 0,
            get_val(e,"Altitud (msnm)") or 0,
            get_val(e,"Temp. Promedio (°C)") or 0,
            get_val(e,"Tipo de Suelo"),
            get_val(e,"Región") or None,
        )
        if resultado:
            self._guardar_foto("nueva")
            messagebox.showinfo("✅ Finca", "Finca guardada correctamente.")
            clear_entries(e); self.refresh()

    def update(self):
        fid = get_val(self.entries, "Código Finca")
        if not fid:
            messagebox.showwarning("Actualizar", "Selecciona una finca de la tabla."); return
        if not self._validar(): return
        if not messagebox.askyesno("Confirmar", f"¿Actualizar finca ID {fid}?"): return
        e = self.entries
        if FincaModel.update(
            fid, get_val(e,"Nombre"), get_val(e,"Ubicación"),
            get_val(e,"Latitud") or None, get_val(e,"Longitud") or None,
            get_val(e,"Extensión (ha)") or 0,
            get_val(e,"Altitud (msnm)") or 0,
            get_val(e,"Temp. Promedio (°C)") or 0,
            get_val(e,"Tipo de Suelo"),
            get_val(e,"Región") or None,
        ):
            self._guardar_foto(fid)
            messagebox.showinfo("✅ Finca", "Finca actualizada correctamente.")
            self.refresh()

    def delete(self):
        fid = get_val(self.entries, "Código Finca")
        if not fid:
            messagebox.showwarning("Eliminar", "Selecciona una finca de la tabla."); return
        if messagebox.askyesno("⚠️ Confirmar eliminación",
                                f"¿Eliminar finca ID {fid}?\nEsta acción no se puede deshacer."):
            if FincaModel.delete(fid):
                messagebox.showinfo("✅ Finca", "Finca eliminada.")
                clear_entries(self.entries); self.refresh()

    def exportar_excel(self):
        cols, filas = get_tree_data(self.tree)
        exportar_excel("Fincas", cols, filas)

    def exportar_pdf(self):
        cols, filas = get_tree_data(self.tree)
        exportar_pdf("Fincas", cols, filas)
