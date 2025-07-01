# pages/placa_busca_page.py
import customtkinter as ctk
from database import conectar
from datetime import datetime

class PlacaBuscaPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.build_page()

    def build_page(self):
        ctk.CTkLabel(self, text="Resultado da Busca por Placa", font=("Arial", 20)).pack(pady=10)

        self.label_erro = ctk.CTkLabel(self, text="", text_color="red")
        self.label_erro.pack(pady=(0,5))

        # Filtrar por data
        frame_filtros = ctk.CTkFrame(self)
        frame_filtros.pack(pady=5, fill="x", padx=10)

        ctk.CTkLabel(frame_filtros, text="Data Inicial (dd/mm/aaaa):").pack(side="left", padx=(0,5))
        self.entry_data_inicial = ctk.CTkEntry(frame_filtros, width=100)
        self.entry_data_inicial.pack(side="left", padx=(0,15))

        ctk.CTkLabel(frame_filtros, text="Data Final (dd/mm/aaaa):").pack(side="left", padx=(0,5))
        self.entry_data_final = ctk.CTkEntry(frame_filtros, width=100)
        self.entry_data_final.pack(side="left", padx=(0,15))

        self.entry_placa = ctk.CTkEntry(frame_filtros, placeholder_text="Digite a placa", width=150)
        self.entry_placa.pack(side="left", padx=(0,10))

        btn_buscar = ctk.CTkButton(frame_filtros, text="Buscar", command=self.buscar)
        btn_buscar.pack(side="left")

        self.entry_data_inicial.bind("<KeyRelease>", self.formatar_data)
        self.entry_data_final.bind("<KeyRelease>", self.formatar_data)

        self.lista_frame = ctk.CTkScrollableFrame(self, height=400, fg_color="transparent")
        self.lista_frame.pack(fill="both", expand=True)


    def formatar_data(self, event):
        entry = event.widget
        texto = entry.get()
        cursor_pos = entry.index("insert")

        # Remove tudo que não seja número
        numeros = ''.join(filter(str.isdigit, texto))

        # Monta a string com barras nos índices 2 e 4, se possível
        nova_data = ""
        for i, digito in enumerate(numeros):
            nova_data += digito
            if i == 1 or i == 3 and i != len(numeros) -1:
                nova_data += "/"
      

        # Guarda a posição antes e depois pra evitar pular o cursor
        entry.delete(0, "end")
        entry.insert(0, nova_data)

        # Ajusta o cursor (vai até o fim se estiver editando normalmente)
        if event.keysym.lower() != "backspace":
            entry.icursor(len(nova_data))
        else:
            # Se apagando, mantém posição mais próxima possível
            entry.icursor(min(cursor_pos, len(nova_data)))


    def buscar(self):
        placa = self.entry_placa.get().strip()
        data_inicial = self.entry_data_inicial.get().strip()
        data_final = self.entry_data_final.get().strip()

        # Validar datas
        formato_data = "%d/%m/%Y"
        try:
            if data_inicial:
                dt_inicial = datetime.strptime(data_inicial, formato_data)
            else:
                dt_inicial = None
            if data_final:
                dt_final = datetime.strptime(data_final, formato_data)
            else:
                dt_final = None
        except ValueError:
            # Data inválida
            self.label_erro.configure(text="Formato de data inválido. Use dd/mm/aaaa.")
            return
        
        self.label_erro.configure(text="") 

        self.buscar_placa(placa, dt_inicial, dt_final)


    def buscar_placa(self, placa,  dt_inicial=None, dt_final=None):
        for widget in self.lista_frame.winfo_children():
            widget.destroy()

        conn = conectar()
        cursor = conn.cursor()

        query = "SELECT * FROM veiculos WHERE 1=1"
        params = []

        if placa:
            query += " AND placa = ?"
            params.append(placa)

        if dt_inicial:
            # Datas no banco estão como string dd/mm/yyyy hh:mm:ss
            # Vamos comparar convertendo substring para 'YYYY-MM-DD' formato (SQLite aceita)
            query += " AND date(substr(datahora, 7,4) || '-' || substr(datahora, 4,2) || '-' || substr(datahora, 1,2)) >= ?"
            params.append(dt_inicial.strftime("%Y-%m-%d"))

        if dt_final:
            query += " AND date(substr(datahora, 7,4) || '-' || substr(datahora, 4,2) || '-' || substr(datahora, 1,2)) <= ?"
            params.append(dt_final.strftime("%Y-%m-%d"))

        query += " ORDER BY id DESC"
        resultados =  cursor.execute(query, params).fetchall()
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
