# main.py
import customtkinter as ctk
from database import criar_tabelas
from veiculos_page import VeiculosPage
from encomendas_page import EncomendasPage
from menu_lateral import MenuLateral
from pesquisa_veiculo_page import PlacaBuscaPage

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x500")
        self.title("Sistema de Cadastro - Condomínio")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        criar_tabelas()

        

        self.container = ctk.CTkFrame(self, corner_radius=0)
        self.container.pack(side="right", fill="both", expand=True)

        self.paginas = {
            "veiculos": VeiculosPage(self.container),
            "encomendas": EncomendasPage(self.container),
            "placa_busca": PlacaBuscaPage(self.container),
           
        }
        
        self.menu = MenuLateral(self, self.mostrar_pagina, self.paginas['veiculos'])
        self.menu.pack(side="left", fill="y")

        self.pagina_atual = None
        self.mostrar_pagina("veiculos")

    def mostrar_pagina(self, nome):
        if self.pagina_atual:
            self.pagina_atual.pack_forget()
        self.pagina_atual = self.paginas[nome]
        self.pagina_atual.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()