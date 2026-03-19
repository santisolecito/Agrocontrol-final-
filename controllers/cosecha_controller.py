from tkinter import messagebox
from models.cosecha_model import CosechaModel
from views.cosecha_view import FIELDS
from views.base_view import (build_panel, load_tree, make_buttons,
                              get_val, set_val, clear_entries, get_tree_data)
from utils.exportar_excel import exportar_excel
from utils.exportar_pdf   import exportar_pdf
from utils.validaciones   import (validar_campos, campo_requerido,
                                   es_numero, es_positivo)

class CosechaController:
    def __init__(self, tab):
        _, self.entries, self.tree, self.sv, self.btn_frame = \
            build_panel(tab, "REGISTRO DE COSECHAS", FIELDS, "#2d7a5a")
        make_buttons(self.btn_frame, self.save, self.update, self.delete,
                     lambda: clear_entries(self.entries), self.refresh,
                     excel_cmd=self.exportar_excel, pdf_cmd=self.exportar_pdf)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.sv.trace_add("write", lambda *_: self.refresh())
        self.refresh()

    def refresh(self):
        result = CosechaModel.get_all()
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
            (campo_requerido, get_val(e,"Parcela ID"), "Parcela ID"),
            (es_numero,       get_val(e,"Parcela ID"), "Parcela ID"),
            (campo_requerido, get_val(e,"Cultivo ID"), "Cultivo ID"),
            (es_numero,       get_val(e,"Cultivo ID"), "Cultivo ID"),
            (es_numero,       get_val(e,"Cantidad (kg)") or "0", "Cantidad (kg)"),
            (es_positivo,     get_val(e,"Cantidad (kg)") or "0", "Cantidad (kg)"),
            (campo_requerido, get_val(e,"Calidad"),        "Calidad"),
            (campo_requerido, get_val(e,"Método Cosecha"), "Método Cosecha"),
        ])

    def save(self):
        if not self._validar(): return
        e = self.entries
        if CosechaModel.insert(
            get_val(e,"Parcela ID") or None,
            get_val(e,"Cultivo ID") or None,
            get_val(e,"Fecha Inicio") or None,
            get_val(e,"Fecha Fin") or None,
            get_val(e,"Cantidad (kg)") or 0,
            get_val(e,"Calidad"),
            get_val(e,"Método Cosecha"),
        ):
            messagebox.showinfo("✅ Cosecha", "Cosecha registrada correctamente.")
            clear_entries(e); self.refresh()

    def update(self):
        hid = get_val(self.entries, "Código Cosecha")
        if not hid:
            messagebox.showwarning("Actualizar", "Selecciona una cosecha."); return
        if not self._validar(): return
        if not messagebox.askyesno("Confirmar", f"¿Actualizar cosecha ID {hid}?"): return
        e = self.entries
        if CosechaModel.update(
            hid,
            get_val(e,"Parcela ID") or None,
            get_val(e,"Cultivo ID") or None,
            get_val(e,"Fecha Inicio") or None,
            get_val(e,"Fecha Fin") or None,
            get_val(e,"Cantidad (kg)") or 0,
            get_val(e,"Calidad"),
            get_val(e,"Método Cosecha"),
        ):
            messagebox.showinfo("✅ Cosecha", "Cosecha actualizada correctamente."); self.refresh()

    def delete(self):
        hid = get_val(self.entries, "Código Cosecha")
        if not hid:
            messagebox.showwarning("Eliminar", "Selecciona una cosecha."); return
        if messagebox.askyesno("⚠️ Confirmar", f"¿Eliminar cosecha ID {hid}?"):
            if CosechaModel.delete(hid):
                messagebox.showinfo("✅ Cosecha", "Cosecha eliminada.")
                clear_entries(self.entries); self.refresh()

    def exportar_excel(self):
        cols, filas = get_tree_data(self.tree)
        exportar_excel("Cosechas", cols, filas)

    def exportar_pdf(self):
        cols, filas = get_tree_data(self.tree)
        exportar_pdf("Cosechas", cols, filas)
