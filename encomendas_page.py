# pages/encomendas_page.py
import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox
from database import conectar

class EncomendasPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.build_page()

    def build_page(self):
        ctk.CTkLabel(self, text="Cadastro de Encomendas", font=("Arial", 20)).pack(pady=10)

        self.entry_destinatario = ctk.CTkEntry(self, placeholder_text="Destinatário")
        self.entry_destinatario.pack(pady=5)

        self.entry_lote = ctk.CTkEntry(self, placeholder_text="Lote")
        self.entry_lote.pack(pady=5)

        self.entry_codigo = ctk.CTkEntry(self, placeholder_text="Código da Encomenda")
        self.entry_codigo.pack(pady=5)

        self.entry_destinatario.bind("<Return>", self.salvar_com_enter)
        self.entry_lote.bind("<Return>", self.salvar_com_enter)
        self.entry_codigo.bind("<Return>", self.salvar_com_enter)

        ctk.CTkButton(self, text="Salvar Encomenda", command=self.salvar_encomenda).pack(pady=10)

        self.lista_frame = ctk.CTkScrollableFrame(self,  height=250, fg_color="transparent")
        self.lista_frame.pack(fill="both", expand=True)
        self.carregar_encomendas()

    def salvar_encomenda(self):
        destinatario = self.entry_destinatario.get()
        lote = self.entry_lote.get()
        codigo = self.entry_codigo.get()
        datahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        horaentrega = ''

        if destinatario and codigo:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO encomendas (datahora, destinatario, lote, codigo, status, horaentrega) VALUES (?, ?, ?, ?, ?, ?)",
                           (datahora, destinatario, lote, codigo, 'Não Entregue', horaentrega))
            conn.commit()
            conn.close()
            self.entry_destinatario.delete(0, 'end')
            self.entry_lote.delete(0, 'end')
            self.entry_codigo.delete(0, 'end')
            self.carregar_encomendas()
        else:
            messagebox.showerror("Erro", "Preencha os campos obrigatórios")

    def salvar_com_enter(self, event):
        self.salvar_encomenda()

    def carregar_encomendas(self):
        for widget in self.lista_frame.winfo_children():
            widget.destroy()

        conn = conectar()
        cursor = conn.cursor()
        for row in cursor.execute("SELECT * FROM encomendas ORDER BY id DESC"):
            id_, datahora, destinatario, lote, codigo, status , horaentrega = row
           
            if status == "Entregue":
                cor = "#444444" 
            else:
                cor= "#2b2b2b"
            
            linha = ctk.CTkFrame(self.lista_frame, fg_color=cor)
            linha.pack(fill="x", padx=5, pady=5)

            def alterar_status(id_=id_, atual=status):
                conn = conectar()
                cursor = conn.cursor()
                
                if atual == "Não Entregue": 
                    novo = "Entregue" 
                    entrega = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                else:
                    novo = "Não Entregue"
                    entrega = ""
                cursor.execute("UPDATE encomendas SET status=? WHERE id=?", (novo, id_))
                cursor.execute("UPDATE encomendas SET horaentrega=? WHERE id=?", (entrega, id_))
                conn.commit()
                conn.close()
                self.carregar_encomendas()

            def apagar(id_=id_):
                conn = conectar()
                cursor = conn.cursor()
                if messagebox.askyesno("Confirmar", "Deseja apagar esta encomenda?"):
                    cursor.execute("DELETE FROM encomendas WHERE id=?", (id_,))
                    conn.commit()
                    conn.close()
                    self.carregar_encomendas()

             
            if status == "Não Entregue":
                btn_txt = "Entregue"
            else:
                btn_txt = "Não entregue"

            ctk.CTkButton(linha, text="Apagar", width=70, fg_color="red", command=apagar).pack(side="right", padx=5)
            ctk.CTkButton(linha, text=btn_txt, width=70, fg_color="gray", command=alterar_status).pack(side="right", padx=5)

            ctk.CTkLabel(linha, text=f"Recebi: {datahora}", anchor="w").pack(fill="x", padx=5)
            ctk.CTkLabel(linha, text=f"Nome: {destinatario}", anchor="w").pack(fill="x", padx=5)
            ctk.CTkLabel(linha, text=f"Casa/Quadra: {lote}", anchor="w").pack(fill="x", padx=5)
            ctk.CTkLabel(linha, text=f"Código: {codigo}", anchor="w").pack(fill="x", padx=5)
            ctk.CTkLabel(linha, text=f"Entregue: {horaentrega}", anchor="w").pack(fill="x", padx=5)

            
        conn.close()
