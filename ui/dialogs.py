import customtkinter as ctk
from config.theme import *
from ui.widgets import create_input, create_button
from database.profiles import salvar_perfil

class NovaConexaoWindow(ctk.CTkToplevel):
    def __init__(self, master, callback):
        super().__init__(master)
        
        self.callback = callback

        self.title("Novo Servidor")
        self.geometry("430x450")
        self.resizable(False, False)

        self.configure(fg_color=BG_MAIN)

        self.grab_set()
        self.focus()

        self.build_ui()

    def build_ui(self):
        title = ctk.CTkLabel(
            self,
            text="NOVO SERVIDOR",
            font=FONT_TITLE,
            text_color=TEXT_PRIMARY
        )
        title.pack(pady=(20, 20))

        self.entry_nome = create_input(self, "Nome do Perfil")
        self.entry_nome.pack(fill="x", padx=25, pady=(0, 12))

        self.entry_host = create_input(self, "Servidor")
        self.entry_host.pack(fill="x", padx=25, pady=(0, 12))

        self.entry_user = create_input(self, "Usuário")
        self.entry_user.pack(fill="x", padx=25, pady=(0, 12))

        self.entry_pass = create_input(self, "Senha", password=True)
        self.entry_pass.pack(fill="x", padx=25, pady=(0, 12))

        self.entry_bancos = create_input(self, "Bancos separados por vírgula")
        self.entry_bancos.pack(fill="x", padx=25, pady=(0, 20))

        btn = create_button(
            self,
            "Salvar Perfil",
            self.salvar,
            color=GREEN,
            hover=GREEN_HOVER
        )
        btn.pack(padx=25, fill="x")

    def salvar(self):
        nome = self.entry_nome.get().strip()
        host = self.entry_host.get().strip()
        user = self.entry_user.get().strip()
        senha = self.entry_pass.get().strip()
        bancos = self.entry_bancos.get().strip()

        if not all([nome, host, user, senha]):
            return

        salvar_perfil(nome, host, user, senha, bancos)

        self.callback(nome)
        self.destroy()