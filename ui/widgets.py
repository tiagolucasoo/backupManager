import customtkinter as ctk
from config.theme import *

class SectionFrame(ctk.CTkFrame):
    def __init__(self, master, title):
        super().__init__(
            master,
            fg_color=BG_CARD,
            corner_radius=RADIUS,
            border_width=1,
            border_color=BORDER_COLOR
        )

        self.title = ctk.CTkLabel(
            self,
            text=title,
            font=FONT_SECTION,
            text_color=TEXT_SECONDARY
        )

        self.title.pack(
            anchor="w",
            padx=15,
            pady=(12, 8)
        )

def create_input(master, placeholder, password=False):
    return ctk.CTkEntry(
        master,
        placeholder_text=placeholder,
        height=40,
        corner_radius=8,
        fg_color=BG_INPUT,
        border_color=BORDER_COLOR,
        font=FONT_NORMAL,
        show="*" if password else ""
    )

def create_button(master, text, command, color=BLUE, hover=BLUE_HOVER):
    return ctk.CTkButton(
        master,
        text=text,
        command=command,
        height=40,
        corner_radius=8,
        fg_color=color,
        hover_color=hover,
        font=FONT_BUTTON
    )