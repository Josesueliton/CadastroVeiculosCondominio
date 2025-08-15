import customtkinter as ctk
from database import conectar
from tkinter import messagebox

class AgendaPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.build_page()

    def build_page(self):
        # Título
        ctk.CTkLabel(self, text="Agenda de Contatos", font=("Arial", 24)).pack(pady=10)

        
        # Campo Nome
        self.entry_nome = ctk.CTkEntry(self, placeholder_text="Nome")
        self.entry_nome.pack(pady=5)

        # Campo Lote
        self.entry_lote = ctk.CTkEntry(self, placeholder_text="Lote")
        self.entry_lote.pack(pady=5)

        # Campo Celular
        self.entry_celular = ctk.CTkEntry(self, placeholder_text="Celular")
        self.entry_celular.pack(pady=5)

        # Botão Adicionar
        btn_add = ctk.CTkButton(self, text="Adicionar Contato", command=self.adicionar_contato)
        btn_add.pack(pady=10)

        # Lista de contatos
        self.lista_frame = ctk.CTkScrollableFrame(self, height=250, fg_color="transparent")
        self.lista_frame.pack(fill="both", expand=True)

        self.carregar_contatos()

    def adicionar_contato(self):
        nome = self.entry_nome.get().strip()
        lote = self.entry_lote.get().strip()
        celular = self.entry_celular.get().strip()

        if nome and lote and celular:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO contatos (nome, lote, celular) VALUES (?, ?, ?)",
                           (nome, lote, celular))
            conn.commit()
            conn.close()

            self.entry_nome.delete(0, 'end')
            self.entry_lote.delete(0, 'end')
            self.entry_celular.delete(0, 'end')

            self.carregar_contatos()
        else:
            messagebox.showerror("Erro", "Preencha todos os campos")

    def carregar_contatos(self):
        for widget in self.lista_frame.winfo_children():
            widget.destroy()

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT nome, lote, celular FROM contatos ORDER BY nome")
        
        for nome, lote, celular in cursor.fetchall():
            linha = ctk.CTkFrame(self.lista_frame)
            linha.pack(fill="x", padx=5, pady=5)
            ctk.CTkLabel(linha, text=f"Nome: {nome}", anchor="w").pack(fill="x", padx=5)
            ctk.CTkLabel(linha, text=f"Casa/Quadra: {lote}", anchor="w").pack(fill="x", padx=5)
            ctk.CTkLabel(linha, text=f"Celular: {celular}", anchor="w").pack(fill="x", padx=5)
        conn.close()


