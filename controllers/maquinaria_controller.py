from tkinter import messagebox
from models.maquinaria_model import MaquinariaModel
from views.maquinaria_view import FIELDS
from views.base_view import (build_panel, load_tree, make_buttons,
                              get_val, set_val, clear_entries, get_tree_data)
from utils.exportar_excel import exportar_excel
from utils.exportar_pdf   import exportar_pdf
from utils.validaciones   import (validar_campos, campo_requerido,
                                   longitud_valida, es_numero, es_positivo,
                                   sin_caracteres_especiales)

class MaquinariaController:
    def __init__(self, tab):
        _, self.entries, self.tree, self.sv, self.btn_frame = \
            build_panel(tab, "GESTIÓN DE MAQUINARIA", FIELDS, "#3d5c7a")
        make_buttons(self.btn_frame, self.save, self.update, self.delete,
                     lambda: clear_entries(self.entries), self.refresh,
                     excel_cmd=self.exportar_excel, pdf_cmd=self.exportar_pdf)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.sv.trace_add("write", lambda *_: self.refresh())
        self.refresh()

    def refresh(self):
        result = MaquinariaModel.get_all()
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
            (campo_requerido,           get_val(e,"Marca"),  "Marca"),
            (longitud_valida,           get_val(e,"Marca"),  "Marca", 2, 40),
            (sin_caracteres_especiales, get_val(e,"Marca"),  "Marca"),
            (campo_requerido,           get_val(e,"Modelo"), "Modelo"),
            (es_numero,                 get_val(e,"Año Fabricación") or "0", "Año Fabricación"),
            (es_numero,                 get_val(e,"Potencia (HP)") or "0",   "Potencia (HP)"),
            (es_positivo,               get_val(e,"Potencia (HP)") or "0",   "Potencia (HP)"),
            (es_numero,                 get_val(e,"Horómetro (hrs)") or "0", "Horómetro (hrs)"),
        ])

    def save(self):
        if not self._validar(): return
        e = self.entries
        if MaquinariaModel.insert(
            get_val(e,"Marca"), get_val(e,"Modelo"),
            get_val(e,"Año Fabricación") or 0,
            get_val(e,"Potencia (HP)") or 0,
            get_val(e,"Tipo Combustible"),
            get_val(e,"Horómetro (hrs)") or 0,
            get_val(e,"Estado Operativo"),
        ):
            messagebox.showinfo("✅ Maquinaria", "Máquina guardada correctamente.")
            clear_entries(e); self.refresh()

    def update(self):
        mid = get_val(self.entries, "Código Máquina")
        if not mid:
            messagebox.showwarning("Actualizar", "Selecciona una máquina."); return
        if not self._validar(): return
        if not messagebox.askyesno("Confirmar", f"¿Actualizar máquina ID {mid}?"): return
        e = self.entries
        if MaquinariaModel.update(
            mid, get_val(e,"Marca"), get_val(e,"Modelo"),
            get_val(e,"Año Fabricación") or 0,
            get_val(e,"Potencia (HP)") or 0,
            get_val(e,"Tipo Combustible"),
            get_val(e,"Horómetro (hrs)") or 0,
            get_val(e,"Estado Operativo"),
        ):
            messagebox.showinfo("✅ Maquinaria", "Máquina actualizada correctamente."); self.refresh()

    def delete(self):
        mid = get_val(self.entries, "Código Máquina")
        if not mid:
            messagebox.showwarning("Eliminar", "Selecciona una máquina."); return
        if messagebox.askyesno("⚠️ Confirmar", f"¿Eliminar máquina ID {mid}?"):
            if MaquinariaModel.delete(mid):
                messagebox.showinfo("✅ Maquinaria", "Máquina eliminada.")
                clear_entries(self.entries); self.refresh()

    def exportar_excel(self):
        cols, filas = get_tree_data(self.tree)
        exportar_excel("Maquinaria", cols, filas)

    def exportar_pdf(self):
        cols, filas = get_tree_data(self.tree)
        exportar_pdf("Maquinaria", cols, filas)
