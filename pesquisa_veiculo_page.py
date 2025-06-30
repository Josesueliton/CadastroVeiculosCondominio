# pages/placa_busca_page.py
import customtkinter as ctk
from database import conectar

class PlacaBuscaPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.build_page()

    def build_page(self):
        ctk.CTkLabel(self, text="Resultado da Busca por Placa", font=("Arial", 20)).pack(pady=10)
        self.lista_frame = ctk.CTkScrollableFrame(self, height=400, fg_color="transparent")
        self.lista_frame.pack(fill="both", expand=True)

    def buscar_placa(self, placa):
        for widget in self.lista_frame.winfo_children():
            widget.destroy()

        conn = conectar()
        cursor = conn.cursor()
        resultados = cursor.execute("SELECT * FROM veiculos WHERE placa = ? ORDER BY id DESC", (placa,)).fetchall()
        conn.close()

        if not resultados:
            ctk.CTkLabel(self.lista_frame, text="Nenhum resultado encontrado.").pack(pady=10)
            return

        for row in resultados:
            id_, datahora, nome, lote, placa, modelo, status, saida = row
            cor = "#444444" if status == "Saiu" else "#2b2b2b"
            linha = ctk.CTkFrame(self.lista_frame, fg_color=cor)
            linha.pack(fill="x", padx=5, pady=5)

            ctk.CTkLabel(linha, text=f"Data/Hora: {datahora}", anchor="w").pack(fill="x", padx=5)
            ctk.CTkLabel(linha, text=f"Nome: {nome}", anchor="w").pack(fill="x", padx=5)
            ctk.CTkLabel(linha, text=f"Casa/Quadra: {lote}", anchor="w").pack(fill="x", padx=5)
            ctk.CTkLabel(linha, text=f"Placa: {placa}", anchor="w").pack(fill="x", padx=5)
            ctk.CTkLabel(linha, text=f"Modelo: {modelo}", anchor="w").pack(fill="x", padx=5)
            ctk.CTkLabel(linha, text=f"Status: {status}", anchor="w").pack(fill="x", padx=5)
            ctk.CTkLabel(linha, text=f"Saída: {saida}", anchor="w").pack(fill="x", padx=5)
