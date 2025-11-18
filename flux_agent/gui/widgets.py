"""Widget riutilizzabili premium."""
import customtkinter as ctk
from typing import Callable
from flux_agent.gui.theme import C, Theme


class MessageBubble(ctk.CTkFrame):
    """Bubble messaggio stile moderne chat apps."""
    
    def __init__(self, master, role: str, content: str, **kwargs):
        """
        Args:
            master: Widget parent
            role: "user" o "assistant"
            content: Testo del messaggio
        """
        # Colori in base al ruolo
        is_user = role == "user"
        fg_color = C["bubble_user"] if is_user else C["bubble_assistant"]
        text_color = C["bubble_user_text"] if is_user else C["bubble_assistant_text"]
        
        super().__init__(
            master,
            fg_color=fg_color,
            corner_radius=Theme.RADIUS["md"],
            **kwargs
        )
        
        # Contenuto messaggio (no etichetta ruolo, più clean)
        content_label = ctk.CTkLabel(
            self,
            text=content,
            font=Theme.get_font("body"),
            text_color=text_color,
            wraplength=450,  # Max width per bubble
            justify="left",
            anchor="w"
        )
        content_label.pack(
            padx=Theme.SPACING["md"], 
            pady=Theme.SPACING["sm"],
            fill="x"
        )


class ConversationCard(ctk.CTkFrame):
    """Card conversazione nella sidebar - design minimal."""
    
    def __init__(self, master, title: str, conv_id: int, on_click: Callable, **kwargs):
        """
        Args:
            master: Widget parent
            title: Titolo conversazione
            conv_id: ID conversazione
            on_click: Callback click
        """
        super().__init__(
            master,
            fg_color="transparent",
            corner_radius=Theme.RADIUS["sm"],
            **kwargs
        )
        
        self.conv_id = conv_id
        self.is_active = False
        
        # Button interno (occupa tutta la card)
        self.button = ctk.CTkButton(
            self,
            text=title,
            command=lambda: on_click(conv_id),
            fg_color="transparent",
            hover_color=C["hover_light"],
            text_color=C["text_secondary"],
            font=Theme.get_font("body"),
            anchor="w",
            height=44,
            corner_radius=Theme.RADIUS["sm"]
        )
        self.button.pack(fill="both", expand=True, padx=0, pady=0)
    
    def set_active(self, active: bool):
        """Imposta lo stato attivo (evidenziato)."""
        self.is_active = active
        if active:
            self.button.configure(
                fg_color=C["bg_tertiary"],
                text_color=C["text_primary"]
            )
        else:
            self.button.configure(
                fg_color="transparent",
                text_color=C["text_secondary"]
            )


class PrimaryButton(ctk.CTkButton):
    """Pulsante primario con stile premium."""
    
    def __init__(self, master, text: str, **kwargs):
        super().__init__(
            master,
            text=text,
            fg_color=C["accent_blue"],
            hover_color=C["accent_blue_hover"],
            text_color=C["text_primary"],
            font=Theme.get_font("body_bold"),
            corner_radius=Theme.RADIUS["md"],
            height=44,
            **kwargs
        )


class InputBox(ctk.CTkTextbox):
    """Input box con stile premium."""
    
    def __init__(self, master, placeholder: str = "Scrivi un messaggio...", **kwargs):
        super().__init__(
            master,
            fg_color=C["bg_input"],
            border_color=C["border_subtle"],
            border_width=1,
            text_color=C["text_primary"],
            font=Theme.get_font("body"),
            corner_radius=Theme.RADIUS["md"],
            **kwargs
        )
        
        # Placeholder (simulato)
        self.placeholder = placeholder
        self.has_content = False
        
        # Mostra placeholder inizialmente
        self.insert("1.0", placeholder)
        self.configure(text_color=C["text_tertiary"])
        
        # Bind eventi per gestire placeholder
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)
        self.bind("<KeyRelease>", self._on_key_release)
    
    def _on_focus_in(self, event):
        """Rimuove placeholder quando si clicca."""
        current = self.get("1.0", "end-1c")
        if current == self.placeholder:
            self.delete("1.0", "end")
            self.configure(text_color=C["text_primary"])
    
    def _on_focus_out(self, event):
        """Ripristina placeholder se vuoto."""
        current = self.get("1.0", "end-1c").strip()
        if not current:
            self.insert("1.0", self.placeholder)
            self.configure(text_color=C["text_tertiary"])
    
    def _on_key_release(self, event):
        """Traccia se ha contenuto."""
        current = self.get("1.0", "end-1c")
        self.has_content = bool(current.strip()) and current != self.placeholder
    
    def get_content(self) -> str:
        """Restituisce il contenuto (senza placeholder)."""
        current = self.get("1.0", "end-1c")
        if current == self.placeholder:
            return ""
        return current.strip()
    
    def clear_content(self):
        """Pulisce il contenuto."""
        self.delete("1.0", "end")
        self.insert("1.0", self.placeholder)
        self.configure(text_color=C["text_tertiary"])
        self.has_content = False