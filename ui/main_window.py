import os
import webbrowser
from tkinter import filedialog
from PIL import Image
import customtkinter as ctk

from config.theme import *
from ui.widgets import SectionFrame, create_input, create_button
from ui.dialogs import NovaConexaoWindow

from database.profiles import (
    listar_nomes_perfis, 
    obter_bancos_por_perfil, 
    adicionar_banco_ao_perfil, 
    obter_credenciais
)
from services.backup import inicializador_backup
from services.logger import format_log

class BackupToolApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Backup Tool")
        self.geometry("760x860")
        self.configure(fg_color=BG_MAIN)

        self.pasta_destino = ""
        self.checkboxes_bancos = {}

        self.build_ui()
        self.carregar_servidores()

    def build_ui(self):
        self.build_header()
        self.build_server_section()
        self.build_config_type_database()
        self.build_config_section()
        self.build_database_section()
        self.build_action_section()
        self.build_console()

    def build_header(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="x", padx=PADDING_X, pady=(20, 15))

        left = ctk.CTkFrame(frame, fg_color="transparent")
        left.pack(side="left", anchor="w")

        if os.path.exists(LOGO_PATH):
            imagem = ctk.CTkImage(
                light_image=Image.open(LOGO_PATH),
                dark_image=Image.open(LOGO_PATH),
                size=(100, 30)
            )
            logo = ctk.CTkLabel(left, image=imagem, text="")
            logo.pack(side="left", padx=(0, 15))

        text_container = ctk.CTkFrame(left, fg_color="transparent")
        text_container.pack(side="left")

        title = ctk.CTkLabel(
            text_container, text="Gerenciador de Backup .BACPAC", 
            font=FONT_TITLE, text_color=TEXT_PRIMARY
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            text_container, text="Azure SQL & SQL Server Backup Tool", 
            font=FONT_NORMAL, text_color=TEXT_MUTED
        )
        subtitle.pack(anchor="w")

        badgeDoc = ctk.CTkButton(
            frame, text="Abrir Documentação", width=150, height=30,
            corner_radius=999, fg_color="#1E3A8A", hover_color="#2563EB",
            text_color="white", font=("Roboto", 12, "bold"),
            command=lambda: webbrowser.open(DOC_URL)
        )
        badgeDoc.pack(side="right", padx=(5, 0))

    def build_server_section(self):
        self.server_section = SectionFrame(self, "1. Perfil de Conexão")
        self.server_section.pack(fill="x", padx=PADDING_X, pady=(0, PADDING_Y))

        row = ctk.CTkFrame(self.server_section, fg_color="transparent")
        row.pack(fill="x", padx=15, pady=(0, 15))

        self.combo_servidor = ctk.CTkOptionMenu(
            row, values=["Nenhum"], height=40, fg_color=BG_INPUT,
            button_color=BLUE, button_hover_color=BLUE_HOVER,
            command=self.troca_servidor
        )
        self.combo_servidor.pack(side="left", fill="x", expand=True, padx=(0, 10))

        btn = create_button(row, "＋ Novo", self.novo_servidor)
        btn.configure(width=120)
        btn.pack(side="left")

    def build_config_type_database(self):
        self.config_type = SectionFrame(self, "2. Tipo de Banco de Dados")
        self.config_type.pack(fill="x", padx=PADDING_X, pady=(0, PADDING_Y))

        row = ctk.CTkFrame(self.config_type, fg_color="transparent")
        row.pack(fill="x", padx=15, pady=(0, 15))

        self.radio_var = ctk.IntVar(value=1) 

        radiobutton_1 = ctk.CTkRadioButton(row, text="SQL Server", variable=self.radio_var, value=1)
        radiobutton_1.pack(side="left", padx=(0, 20)) # padx afasta um botão do outro
        
        radiobutton_2 = ctk.CTkRadioButton(row, text="MySQL", variable=self.radio_var, value=2)
        radiobutton_2.pack(side="left", padx=(0, 20))
        
        radiobutton_3 = ctk.CTkRadioButton(row, text="MongoDB", variable=self.radio_var, value=3)
        radiobutton_3.pack(side="left", padx=(0, 20))
        
        radiobutton_4 = ctk.CTkRadioButton(row, text="SQLite", variable=self.radio_var, value=4)
        radiobutton_4.pack(side="left")

    def build_config_section(self):
        self.config_section = SectionFrame(self, "3. Configurações Gerais")
        self.config_section.pack(fill="x", padx=PADDING_X, pady=(0, PADDING_Y))

        self.entry_sqlpackage = create_input(self.config_section, "Caminho do SqlPackage.exe")
        self.entry_sqlpackage.pack(fill="x", padx=15, pady=(0, 12))

        btn = create_button(self.config_section, "Selecionar Pasta de Destino", self.selecionar_pasta)
        btn.pack(padx=15, pady=(0, 8), fill="x")

        self.lbl_destino = ctk.CTkLabel(
            self.config_section, text="Nenhuma pasta selecionada", 
            text_color=TEXT_MUTED, font=FONT_NORMAL
        )
        self.lbl_destino.pack(pady=(0, 15))

    def build_database_section(self):
        self.database_section = SectionFrame(self, "4. Lista de Bancos de Dados")
        self.database_section.pack(fill="x", padx=PADDING_X, pady=(0, PADDING_Y))

        row = ctk.CTkFrame(self.database_section, fg_color="transparent")
        row.pack(fill="x", padx=15, pady=(0, 12))

        self.entry_novo_banco = create_input(row, "Adicionar banco...")
        self.entry_novo_banco.pack(side="left", fill="x", expand=True, padx=(0, 10))

        btn = create_button(row, "Adicionar", self.banco_dinamico)
        btn.configure(width=50)
        btn.pack(side="left")

        self.scroll_bancos = ctk.CTkScrollableFrame(self.database_section, height=140, fg_color=BG_MAIN)
        self.scroll_bancos.pack(fill="x", padx=15, pady=(0, 15))

    def build_action_section(self):
        self.btn_extrair = create_button(self, "INICIAR EXTRAÇÃO", self.iniciar_extracao, GREEN, GREEN_HOVER)
        self.btn_extrair.configure(height=48)
        self.btn_extrair.pack(fill="x", padx=PADDING_X, pady=(0, PADDING_Y))

    def build_console(self):
        self.console = ctk.CTkTextbox(
            self, height=180, fg_color="#0D0D0D", border_color=BORDER_COLOR,
            border_width=1, font=FONT_CONSOLE, text_color=TEXT_PRIMARY
        )
        self.console.pack(fill="both", expand=True, padx=PADDING_X, pady=(0, 20))
        self.log("Sistema iniciado.", "info")

    def log(self, text, level="info"):
        log_text = format_log(text, level)
        self.console.insert("end", log_text)
        self.console.see("end")

    def novo_servidor(self):
        NovaConexaoWindow(self, self.carregar_servidores)

    def selecionar_pasta(self):
        pasta = filedialog.askdirectory()
        if pasta:
            self.pasta_destino = pasta
            self.lbl_destino.configure(text=pasta, text_color=GREEN)

    def carregar_servidores(self, selecionar=None):
        nomes = listar_nomes_perfis()
        
        if not nomes:
            return

        self.combo_servidor.configure(values=nomes)
        primeiro = selecionar if selecionar else nomes[0]
        self.combo_servidor.set(primeiro)
        self.troca_servidor(primeiro)

    def troca_servidor(self, nome):
        for chk in self.checkboxes_bancos.values():
            chk.destroy()
        
        self.checkboxes_bancos.clear()
        
        bancos = obter_bancos_por_perfil(nome)
        for banco in bancos:
            self.criar_checkbox_banco(banco)

    def criar_checkbox_banco(self, nome):
        chk = ctk.CTkCheckBox(self.scroll_bancos, text=nome, fg_color=BLUE, font=FONT_NORMAL)
        chk.pack(anchor="w", pady=6, padx=5)
        chk.select()
        self.checkboxes_bancos[nome] = chk

    def banco_dinamico(self):
        banco = self.entry_novo_banco.get().strip()
        perfil = self.combo_servidor.get()

        if not banco or banco in self.checkboxes_bancos:
            return

        self.criar_checkbox_banco(banco)
        self.entry_novo_banco.delete(0, "end")
        
        adicionar_banco_ao_perfil(perfil, banco)

    def iniciar_extracao(self):
        perfil = self.combo_servidor.get()
        credenciais = obter_credenciais(perfil)
        bancos = [nome for nome, chk in self.checkboxes_bancos.items() if chk.get() == 1]

        if not bancos:
            self.log("Selecione pelo menos um banco.", "error")
            return
            
        if not self.pasta_destino:
            self.log("Selecione uma pasta destino.", "error")
            return

        caminho = self.entry_sqlpackage.get().strip()
        sqlpackage = caminho if caminho else "C:\\Program Files\\SqlPackage\\sqlpackage.exe"

        if not os.path.exists(sqlpackage):
            self.log("SqlPackage não encontrado.", "error")
            return

        self.btn_extrair.configure(state="disabled", text="EXTRAINDO...")
        
        inicializador_backup(
            bancos=bancos,
            sqlpackage_path=sqlpackage,
            credenciais=credenciais,
            pasta_destino=self.pasta_destino,
            log_callback=self.log,
            on_finish_callback=self.finalizar_extracao
        )
        
    def finalizar_extracao(self):
        self.after(0, lambda: self.btn_extrair.configure(state="normal", text="INICIAR EXTRAÇÃO"))