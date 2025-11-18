"""Sidebar moderna con conversazioni."""
import customtkinter as ctk
from flux_agent.gui.widgets import ConversationCard, PrimaryButton
from flux_agent.gui.theme import C, Theme
from typing import Callable


class Sidebar(ctk.CTkFrame):
    """Sidebar con design minimal e moderno."""
    
    def __init__(self, master, on_new_chat: Callable, on_select_chat: Callable, **kwargs):
        super().__init__(master, fg_color=C["bg_secondary"], width=280, **kwargs)
        
        self.on_new_chat = on_new_chat
        self.on_select_chat = on_select_chat
        self.active_card = None
        
        # Logo/Brand
        brand_frame = ctk.CTkFrame(self, fg_color="transparent", height=80)
        brand_frame.pack(fill="x", padx=Theme.SPACING["lg"], pady=Theme.SPACING["lg"])
        brand_frame.pack_propagate(False)
        
        logo = ctk.CTkLabel(
            brand_frame,
            text="⚡ Flux",
            font=Theme.get_font("title"),
            text_color=C["text_primary"]
        )
        logo.pack(anchor="w")
        
        # New chat button
        new_chat_btn = PrimaryButton(
            self,
            text="+ Nuova Chat",
            command=self.on_new_chat
        )
        new_chat_btn.pack(
            padx=Theme.SPACING["lg"],
            pady=(0, Theme.SPACING["md"]),
            fill="x"
        )
        
        # Divider
        divider = ctk.CTkFrame(self, height=1, fg_color=C["border_subtle"])
        divider.pack(fill="x", padx=Theme.SPACING["lg"], pady=Theme.SPACING["md"])
        
        # Conversazioni header
        conv_header = ctk.CTkLabel(
            self,
            text="Conversazioni",
            font=Theme.get_font("caption"),
            text_color=C["text_tertiary"],
            anchor="w"
        )
        conv_header.pack(
            padx=Theme.SPACING["lg"],
            pady=(0, Theme.SPACING["sm"]),
            anchor="w"
        )
        
        # Lista conversazioni
        self.conversations_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.conversations_frame.pack(
            fill="both",
            expand=True,
            padx=Theme.SPACING["md"]
        )
    
    def add_conversation(self, conv_id: int, title: str) -> None:
        """Aggiunge una conversazione."""
        card = ConversationCard(
            self.conversations_frame,
            title=title,
            conv_id=conv_id,
            on_click=self._on_card_click
        )
        card.pack(fill="x", pady=Theme.SPACING["xs"])
        
        # Attiva automaticamente se è la prima
        if not self.active_card:
            self._on_card_click(conv_id)
    
    def _on_card_click(self, conv_id: int):
        """Gestisce click su conversazione."""
        # Disattiva card precedente
        if self.active_card:
            self.active_card.set_active(False)
        
        # Attiva nuova card
        for widget in self.conversations_frame.winfo_children():
            if isinstance(widget, ConversationCard) and widget.conv_id == conv_id:
                widget.set_active(True)
                self.active_card = widget
                break
        
        # Callback
        self.on_select_chat(conv_id)
    
    def clear_conversations(self) -> None:
        """Rimuove tutte le conversazioni."""
        for widget in self.conversations_frame.winfo_children():
            widget.destroy()
        self.active_card = None