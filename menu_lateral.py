# components/menu_lateral.py
import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox
from database import conectar
from veiculos_page import VeiculosPage
from pesquisa_veiculo_page import PlacaBuscaPage



class MenuLateral(ctk.CTkFrame):
    def __init__(self, master, callback_mudar_pagina, veiculos_page):
        super().__init__(master, width=180)
        self.callback = callback_mudar_pagina
        self.veiculos_page = veiculos_page
        self.build_menu()
        self.atualizar_datahora()

    

    def build_menu(self):

        self.entry_pesquisa = ctk.CTkEntry(self, placeholder_text="Buscar por placa")
        self.entry_pesquisa.pack(pady=(20, 5), padx=10, fill="x")
        self.entry_pesquisa.bind("<Return>", self.pressionar_enter) 


        ctk.CTkButton(self, text="🔍 Pesquisar", command=self.pesquisar_nome).pack(pady=5, padx=10, fill="x")
        

        ctk.CTkLabel(self, text="").pack(pady=60)

        btn_veiculos = ctk.CTkButton(self, text="Veículos", command=lambda: self.callback("veiculos"))
        btn_veiculos.pack(pady=10, padx=20, fill="x")

        btn_encomendas = ctk.CTkButton(self, text="Encomendas", command=lambda: self.callback("encomendas"))
        btn_encomendas.pack(pady=10, padx=20, fill="x")

        self.label_datahora = ctk.CTkLabel(self, text="", font=("Arial", 15))
        self.label_datahora.pack(side="bottom", pady=10)

    def atualizar_datahora(self):
        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.label_datahora.configure(text=agora)
        self.after(1000, self.atualizar_datahora)



    def pesquisar_nome(self, event=None):
        placa = self.entry_pesquisa.get()
        if not placa:
            messagebox.showwarning("Atenção", "Digite a placa para buscar.")
            return
        
        conn = conectar()
        cursor = conn.cursor()
        resultado = cursor.execute("SELECT * FROM veiculos WHERE placa = ? ORDER BY id DESC LIMIT 2", (placa,)).fetchone()
        conn.close()

        self.callback('veiculos')
    
        if resultado:
            
            self.callback('placa_busca')
            self.master.paginas['placa_busca'].buscar_placa(placa)
        else:
            messagebox.showinfo("Não encontrado", f"{placa} não foi encontrado. Faça novo cadastro.")
            self.callback('veiculos')  # tela em branco
    
    
    def pressionar_enter(self, event):
        self.pesquisar_nome()

