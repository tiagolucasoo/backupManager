import customtkinter as ctk
from database.connection import init_db
from ui.main_window import BackupToolApp

def main():
    init_db()

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = BackupToolApp()
    app.mainloop()

if __name__ == "__main__":
    main()