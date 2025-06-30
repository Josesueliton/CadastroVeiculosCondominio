# pages/veiculos_page.py
import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox
from database import conectar

class VeiculosPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.build_page()

    def build_page(self):
        ctk.CTkLabel(self, text="Cadastro de Veículos", font=("Arial", 20)).pack(pady=10)

        self.entry_nome = ctk.CTkEntry(self, placeholder_text="Nome")
        self.entry_nome.pack(pady=5)

        self.entry_lote = ctk.CTkEntry(self, placeholder_text="Lote")
        self.entry_lote.pack(pady=5)

        self.entry_placa = ctk.CTkEntry(self, placeholder_text="Placa")
        self.entry_placa.pack(pady=5)

        self.entry_modelo = ctk.CTkEntry(self, placeholder_text="Modelo")
        self.entry_modelo.pack(pady=5)

        self.entry_nome.bind("<Return>", self.salvar_com_enter)
        self.entry_lote.bind("<Return>", self.salvar_com_enter)
        self.entry_placa.bind("<Return>", self.salvar_com_enter)
        self.entry_modelo.bind("<Return>", self.salvar_com_enter)
        # Automaticamente se existir a placa
        self.entry_placa.bind("<FocusOut>", self.verificar_placa_existente)
        self.entry_placa.bind("<Return>", self.verificar_placa_existente)


        ctk.CTkButton(self, text="Salvar Veículo", command=self.salvar_veiculo).pack(pady=10)


        self.lista_frame = ctk.CTkScrollableFrame(self, height=250, fg_color="transparent")
        self.lista_frame.pack(fill="both", expand=True)
        self.carregar_veiculos()

    
    def preencher_campos(self, dados):
        if dados:
            _, datahora, nome, lote, placa, modelo, status, saida = dados
            self.entry_nome.delete(0, "end")
            self.entry_nome.insert(0, nome)

            self.entry_lote.delete(0, "end")
            self.entry_lote.insert(0, lote)

            self.entry_placa.delete(0, "end")
            self.entry_placa.insert(0, placa)

            self.entry_modelo.delete(0, "end")
            self.entry_modelo.insert(0, modelo)


    def verificar_placa_existente(self, event=None):
        placa = self.entry_placa.get()
        if not placa:
            return

        conn = conectar()
        cursor = conn.cursor()
        resultado = cursor.execute("SELECT * FROM veiculos WHERE placa = ? ORDER BY id DESC LIMIT 1", (placa,)).fetchone()
        conn.close()

        if resultado:
            self.preencher_campos(resultado)


     
    def salvar_veiculo(self):
        nome = self.entry_nome.get()
        lote = self.entry_lote.get()
        placa = self.entry_placa.get()
        modelo = self.entry_modelo.get()
        datahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        saida = ''

        if nome and lote and placa and modelo:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO veiculos (datahora, nome, lote, placa, modelo, status, saidadatahora) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (datahora, nome, lote, placa, modelo, 'Entrou', saida))
            conn.commit()
            conn.close()
            self.entry_nome.delete(0, 'end')
            self.entry_lote.delete(0, 'end')
            self.entry_placa.delete(0, 'end')
            self.entry_modelo.delete(0, 'end')
            self.carregar_veiculos()
        else:
            messagebox.showerror("Erro", "Preencha todos os campos")

    def salvar_com_enter(self, event):
        self.salvar_veiculo()
        
    def carregar_veiculos(self):
        for widget in self.lista_frame.winfo_children():
            widget.destroy()

        conn = conectar()
        cursor = conn.cursor()
        
        for row in cursor.execute("SELECT * FROM veiculos ORDER BY id DESC"):
            id_, datahora, nome, lote, placa, modelo, status, saida = row

            
            if status == f"Saiu":
                
                cor = "#444444"
            else: 
                cor = "#2b2b2b"

            linha = ctk.CTkFrame(self.lista_frame, fg_color=cor)
            linha.pack(fill="x", padx=5, pady=5)

            def alterar_status(id_=id_, atual=status):
                conn = conectar()
                cursor = conn.cursor()
                if atual == "Entrou":
                    novo = f"Saiu"
                    horasaida = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                else:
                    novo = "Entrou"
                    horasaida = ""
                cursor.execute("UPDATE veiculos SET status = ? WHERE id = ?", (novo, id_))
                cursor.execute("UPDATE veiculos SET saidadatahora = ? WHERE id = ?", (horasaida, id_))

                conn.commit()
                conn.close()
                self.carregar_veiculos()

            def apagar(id_=id_):
                conn = conectar()
                cursor = conn.cursor()
                if messagebox.askyesno("Confirmar", "Deseja apagar este veículo?"):
                    cursor.execute("DELETE FROM veiculos WHERE id=?", (id_,))
                    conn.commit()
                    conn.close()
                    self.carregar_veiculos()
                
                

            
            if status == "Saiu":
                btn_cor = "Voltou" 

            else:
                btn_cor = "Saiu"
            ctk.CTkButton(linha, text="Apagar", width=70, fg_color="red", command=apagar).pack(side="right", padx=5)
            ctk.CTkButton(linha, text=btn_cor, width=70, fg_color="gray", command=alterar_status).pack(side="right", padx=5)
            

            ctk.CTkLabel(linha, text=f"Data/Hora: {datahora}", anchor="w").pack(fill="x", padx=5)
            ctk.CTkLabel(linha, text=f"Nome: {nome}", anchor="w").pack(fill="x", padx=5)
            ctk.CTkLabel(linha, text=f"Casa/Quadra: {lote}", anchor="w").pack(fill="x", padx=5)
            ctk.CTkLabel(linha, text=f"Placa: {placa}", anchor="w").pack(fill="x", padx=5)
            ctk.CTkLabel(linha, text=f"Modelo: {modelo}", anchor="w").pack(fill="x", padx=5)
            ctk.CTkLabel(linha, text=f"Saida: {saida}", anchor="w").pack(fill="x", padx=5)
    



            
        conn.close()