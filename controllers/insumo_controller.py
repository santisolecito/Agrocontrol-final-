import os
from tkinter import messagebox
from models.insumo_model import InsumoModel
from views.insumo_view import FIELDS
from views.base_view import (build_panel, load_tree, make_buttons,
                              get_val, set_val, clear_entries, get_tree_data)
from utils.exportar_excel import exportar_excel
from utils.exportar_pdf   import exportar_pdf
from utils.validaciones   import (validar_campos, campo_requerido,
                                   longitud_valida, es_numero, es_positivo,
                                   sin_caracteres_especiales)

class InsumoController:
    def __init__(self, tab):
        _, self.entries, self.tree, self.sv, self.btn_frame = \
            build_panel(tab, "GESTIÓN DE INSUMOS", FIELDS, "#7a5c1e")
        make_buttons(self.btn_frame, self.save, self.update, self.delete,
                     lambda: clear_entries(self.entries), self.refresh,
                     excel_cmd=self.exportar_excel, pdf_cmd=self.exportar_pdf)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.sv.trace_add("write", lambda *_: self.refresh())
        self.refresh()

    def refresh(self):
        result = InsumoModel.get_all()
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
            (campo_requerido,           get_val(e,"Nombre Comercial"), "Nombre Comercial"),
            (longitud_valida,           get_val(e,"Nombre Comercial"), "Nombre Comercial", 2, 60),
            (sin_caracteres_especiales, get_val(e,"Nombre Comercial"), "Nombre Comercial"),
            (campo_requerido,           get_val(e,"Tipo"),             "Tipo"),
            (es_numero,                 get_val(e,"Cantidad en Stock") or "0", "Cantidad en Stock"),
            (es_positivo,               get_val(e,"Cantidad en Stock") or "0", "Cantidad en Stock"),
            (es_numero,                 get_val(e,"Precio Unitario")   or "0", "Precio Unitario"),
            (es_positivo,               get_val(e,"Precio Unitario")   or "0", "Precio Unitario"),
        ])

    def save(self):
        if not self._validar(): return
        e = self.entries
        if InsumoModel.insert(
            get_val(e,"Nombre Comercial"), get_val(e,"Tipo"),
            get_val(e,"Unidad de Medida"), get_val(e,"Ubicación Almacén"),
            get_val(e,"Cantidad en Stock") or 0,
            get_val(e,"Fecha de Caducidad") or None,
            get_val(e,"Precio Unitario") or 0,
        ):
            messagebox.showinfo("✅ Insumo", "Insumo guardado correctamente.")
            clear_entries(e); self.refresh()

    def update(self):
        iid = get_val(self.entries, "Código Insumo")
        if not iid:
            messagebox.showwarning("Actualizar", "Selecciona un insumo."); return
        if not self._validar(): return
        if not messagebox.askyesno("Confirmar", f"¿Actualizar insumo ID {iid}?"): return
        e = self.entries
        if InsumoModel.update(
            iid, get_val(e,"Nombre Comercial"), get_val(e,"Tipo"),
            get_val(e,"Unidad de Medida"), get_val(e,"Ubicación Almacén"),
            get_val(e,"Cantidad en Stock") or 0,
            get_val(e,"Fecha de Caducidad") or None,
            get_val(e,"Precio Unitario") or 0,
        ):
            messagebox.showinfo("✅ Insumo", "Insumo actualizado correctamente."); self.refresh()

    def delete(self):
        iid = get_val(self.entries, "Código Insumo")
        if not iid:
            messagebox.showwarning("Eliminar", "Selecciona un insumo."); return
        if messagebox.askyesno("⚠️ Confirmar", f"¿Eliminar insumo ID {iid}?"):
            if InsumoModel.delete(iid):
                messagebox.showinfo("✅ Insumo", "Insumo eliminado.")
                clear_entries(self.entries); self.refresh()

    def exportar_excel(self):
        cols, filas = get_tree_data(self.tree)
        exportar_excel("Insumos", cols, filas)

    def exportar_pdf(self):
        cols, filas = get_tree_data(self.tree)
        exportar_pdf("Insumos", cols, filas)
