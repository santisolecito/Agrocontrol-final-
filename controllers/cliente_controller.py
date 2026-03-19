from tkinter import messagebox
from models.cliente_model import ClienteModel
from views.cliente_view import FIELDS
from views.base_view import (build_panel, load_tree, make_buttons,
                              get_val, set_val, clear_entries, get_tree_data)
from utils.exportar_excel import exportar_excel
from utils.exportar_pdf   import exportar_pdf
from utils.validaciones   import (validar_campos, campo_requerido,
                                   longitud_valida, es_numero,
                                   es_email_valido, es_dni_valido,
                                   es_telefono_valido,
                                   sin_caracteres_especiales)

class ClienteController:
    def __init__(self, tab):
        _, self.entries, self.tree, self.sv, self.btn_frame = \
            build_panel(tab, "GESTIÓN DE CLIENTES", FIELDS, "#7a3d2d")
        make_buttons(self.btn_frame, self.save, self.update, self.delete,
                     lambda: clear_entries(self.entries), self.refresh,
                     excel_cmd=self.exportar_excel, pdf_cmd=self.exportar_pdf)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.sv.trace_add("write", lambda *_: self.refresh())
        self.refresh()

    def refresh(self):
        result = ClienteModel.get_all()
        if result:
            rows, cols = result
            load_tree(self.tree, rows, cols, self.sv.get())

    def _on_select(self, event):
        sel = self.tree.selection()
        if not sel: return
        vals = self.tree.item(sel[0], "values")
        keys = ["Código Cliente","Razón Social","RUC / DNI",
                "Dirección Fiscal","Teléfono","Correo","Línea de Crédito"]
        for k, v in zip(keys, vals):
            set_val(self.entries, k, v)

    def _validar(self):
        e = self.entries
        correo = get_val(e,"Correo")
        reglas = [
            (campo_requerido,           get_val(e,"Razón Social"),  "Razón Social"),
            (longitud_valida,           get_val(e,"Razón Social"),  "Razón Social", 2, 80),
            (sin_caracteres_especiales, get_val(e,"Razón Social"),  "Razón Social"),
            (es_telefono_valido,        get_val(e,"Teléfono")),
            (es_numero,                 get_val(e,"Línea de Crédito") or "0", "Línea de Crédito"),
        ]
        if correo:
            reglas.append((es_email_valido, correo))
        return validar_campos(reglas)

    def save(self):
        if not self._validar(): return
        e = self.entries
        if ClienteModel.insert(
            get_val(e,"Razón Social"), get_val(e,"RUC / DNI"),
            get_val(e,"Dirección Fiscal"), get_val(e,"Teléfono"),
            get_val(e,"Correo"), get_val(e,"Línea de Crédito") or 0,
        ):
            messagebox.showinfo("✅ Cliente", "Cliente guardado correctamente.")
            clear_entries(e); self.refresh()

    def update(self):
        cid = get_val(self.entries, "Código Cliente")
        if not cid:
            messagebox.showwarning("Actualizar", "Selecciona un cliente."); return
        if not self._validar(): return
        if not messagebox.askyesno("Confirmar", f"¿Actualizar cliente ID {cid}?"): return
        e = self.entries
        if ClienteModel.update(
            cid,
            get_val(e,"Razón Social"), get_val(e,"RUC / DNI"),
            get_val(e,"Dirección Fiscal"), get_val(e,"Teléfono"),
            get_val(e,"Correo"), get_val(e,"Línea de Crédito") or 0,
        ):
            messagebox.showinfo("✅ Cliente", "Cliente actualizado correctamente."); self.refresh()

    def delete(self):
        cid = get_val(self.entries, "Código Cliente")
        if not cid:
            messagebox.showwarning("Eliminar", "Selecciona un cliente."); return
        if messagebox.askyesno("⚠️ Confirmar", f"¿Eliminar cliente ID {cid}?"):
            if ClienteModel.delete(cid):
                messagebox.showinfo("✅ Cliente", "Cliente eliminado.")
                clear_entries(self.entries); self.refresh()

    def exportar_excel(self):
        cols, filas = get_tree_data(self.tree)
        exportar_excel("Clientes", cols, filas)

    def exportar_pdf(self):
        cols, filas = get_tree_data(self.tree)
        exportar_pdf("Clientes", cols, filas)
