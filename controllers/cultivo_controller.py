import os
from tkinter import messagebox
from models.cultivo_model import CultivoModel
from views.cultivo_view import FIELDS
from views.base_view import (build_panel, load_tree, make_buttons,
                              get_val, set_val, clear_entries, get_tree_data)
from utils.exportar_excel import exportar_excel
from utils.exportar_pdf   import exportar_pdf
from utils.validaciones   import (validar_campos, campo_requerido,
                                   longitud_valida, es_numero,
                                   sin_caracteres_especiales)

class CultivoController:
    def __init__(self, tab):
        _, self.entries, self.tree, self.sv, self.btn_frame = \
            build_panel(tab, "GESTIÓN DE CULTIVOS", FIELDS, "#5a6e27")
        make_buttons(self.btn_frame, self.save, self.update, self.delete,
                     lambda: clear_entries(self.entries), self.refresh,
                     excel_cmd=self.exportar_excel, pdf_cmd=self.exportar_pdf)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.sv.trace_add("write", lambda *_: self.refresh())
        self.refresh()

    def refresh(self):
        result = CultivoModel.get_all()
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
            (campo_requerido,           get_val(e,"Nombre Científico"), "Nombre Científico"),
            (longitud_valida,           get_val(e,"Nombre Científico"), "Nombre Científico", 3, 80),
            (campo_requerido,           get_val(e,"Nombre Común"),      "Nombre Común"),
            (sin_caracteres_especiales, get_val(e,"Nombre Común"),      "Nombre Común"),
            (es_numero,                 get_val(e,"Tiempo de Crecimiento") or "0", "Tiempo de Crecimiento"),
            (es_numero,                 get_val(e,"Temp. Óptima (°C)") or "0",     "Temp. Óptima (°C)"),
            (es_numero,                 get_val(e,"Req. Agua (mm/año)") or "0",    "Req. Agua (mm/año)"),
        ])

    def save(self):
        if not self._validar(): return
        e = self.entries
        if CultivoModel.insert(
            get_val(e,"Nombre Científico"), get_val(e,"Nombre Común"),
            get_val(e,"Tiempo de Crecimiento") or 0,
            get_val(e,"Temp. Óptima (°C)") or 0,
            get_val(e,"Req. Agua (mm/año)") or 0,
        ):
            messagebox.showinfo("✅ Cultivo", "Cultivo guardado correctamente.")
            clear_entries(e); self.refresh()

    def update(self):
        cid = get_val(self.entries, "Código Cultivo")
        if not cid:
            messagebox.showwarning("Actualizar", "Selecciona un cultivo."); return
        if not self._validar(): return
        if not messagebox.askyesno("Confirmar", f"¿Actualizar cultivo ID {cid}?"): return
        e = self.entries
        if CultivoModel.update(
            cid, get_val(e,"Nombre Científico"), get_val(e,"Nombre Común"),
            get_val(e,"Tiempo de Crecimiento") or 0,
            get_val(e,"Temp. Óptima (°C)") or 0,
            get_val(e,"Req. Agua (mm/año)") or 0,
        ):
            messagebox.showinfo("✅ Cultivo", "Cultivo actualizado correctamente."); self.refresh()

    def delete(self):
        cid = get_val(self.entries, "Código Cultivo")
        if not cid:
            messagebox.showwarning("Eliminar", "Selecciona un cultivo."); return
        if messagebox.askyesno("⚠️ Confirmar", f"¿Eliminar cultivo ID {cid}?"):
            if CultivoModel.delete(cid):
                messagebox.showinfo("✅ Cultivo", "Cultivo eliminado.")
                clear_entries(self.entries); self.refresh()

    def exportar_excel(self):
        cols, filas = get_tree_data(self.tree)
        exportar_excel("Cultivos", cols, filas)

    def exportar_pdf(self):
        cols, filas = get_tree_data(self.tree)
        exportar_pdf("Cultivos", cols, filas)
