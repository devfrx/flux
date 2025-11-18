"""Pannello chat principale - Design moderno."""
import customtkinter as ctk
from flux_agent.gui.widgets import MessageBubble, PrimaryButton, InputBox
from flux_agent.gui.theme import C, Theme
from typing import Callable


class ChatPanel(ctk.CTkFrame):
    """Pannello chat con bubble design moderno."""
    
    def __init__(self, master, on_send_message: Callable, **kwargs):
        """
        Args:
            master: Widget parent
            on_send_message: Callback async per inviare messaggi
        """
        super().__init__(master, fg_color=C["bg_primary"], **kwargs)
        
        self.on_send_message = on_send_message
        self.master_app = master
        
        # Layout: header + chat + input
        self.grid_rowconfigure(0, weight=0)  # Header fisso
        self.grid_rowconfigure(1, weight=1)  # Chat espandibile
        self.grid_rowconfigure(2, weight=0)  # Input fisso
        self.grid_columnconfigure(0, weight=1)
        
        # Header (minimale)
        self._create_header()
        
        # Area messaggi (scrollabile)
        self.messages_container = ctk.CTkScrollableFrame(
            self,
            fg_color=C["bg_primary"],
            scrollbar_button_color=C["bg_tertiary"],
            scrollbar_button_hover_color=C["hover_light"]
        )
        self.messages_container.grid(
            row=1, column=0, sticky="nsew",
            padx=Theme.SPACING["xl"], 
            pady=Theme.SPACING["md"]
        )
        
        # Input area
        self._create_input_area()
    
    def _create_header(self):
        """Crea header minimale."""
        header = ctk.CTkFrame(self, fg_color="transparent", height=60)
        header.grid(row=0, column=0, sticky="ew", padx=Theme.SPACING["xl"])
        header.grid_propagate(False)
        
        title = ctk.CTkLabel(
            header,
            text="Flux Agent",
            font=Theme.get_font("heading"),
            text_color=C["text_primary"]
        )
        title.pack(side="left", pady=Theme.SPACING["md"])
    
    def _create_input_area(self):
        """Crea area input con stile moderno."""
        input_container = ctk.CTkFrame(self, fg_color="transparent")
        input_container.grid(
            row=2, column=0, sticky="ew",
            padx=Theme.SPACING["xl"],
            pady=Theme.SPACING["lg"]
        )
        input_container.grid_columnconfigure(0, weight=1)
        
        # Input box custom
        self.input_box = InputBox(
            input_container,
            placeholder="Scrivi un messaggio...",
            height=100
        )
        self.input_box.grid(row=0, column=0, sticky="ew", padx=(0, Theme.SPACING["md"]))
        self.input_box.bind("<Return>", self._on_enter)
        
        # Send button
        self.send_button = PrimaryButton(
            input_container,
            text="→",  # Freccia simbolo
            width=100,
            command=self._send_clicked
        )
        self.send_button.grid(row=0, column=1)
    
    def add_message(self, role: str, content: str) -> None:
        """Aggiunge un messaggio con bubble design."""
        bubble = MessageBubble(self.messages_container, role=role, content=content)
        
        # Allineamento: user a destra, assistant a sinistra
        if role == "user":
            bubble.pack(anchor="e", padx=Theme.SPACING["md"], pady=Theme.SPACING["sm"])
        else:
            bubble.pack(anchor="w", padx=Theme.SPACING["md"], pady=Theme.SPACING["sm"])
        
        # Scroll to bottom
        self.messages_container._parent_canvas.yview_moveto(1.0)
    
    def clear_messages(self) -> None:
        """Pulisce tutti i messaggi."""
        for widget in self.messages_container.winfo_children():
            widget.destroy()
    
    def _on_enter(self, event) -> str:
        """Gestisce Enter (senza Shift = invia)."""
        if not event.state & 0x1:  # Shift non premuto
            self._send_clicked()
            return "break"
    
    def _send_clicked(self) -> None:
        """Gestisce invio messaggio."""
        message = self.input_box.get_content()
        if not message:
            return
        
        # Mostra messaggio utente
        self.add_message("user", message)
        self.input_box.clear_content()
        
        # Disabilita input
        self.send_button.configure(state="disabled", text="...")
        self.input_box.configure(state="disabled")
        
        # Invia al backend
        self.master_app.run_async(self._send_and_receive(message))
    
    async def _send_and_receive(self, message: str) -> None:
        """Invia e riceve risposta."""
        try:
            response = await self.on_send_message(message)
            self.master_app.after(0, lambda: self.add_message("assistant", response))
        except Exception as e:
            self.master_app.after(0, lambda: self.add_message("assistant", f"❌ Errore: {e}"))
        finally:
            def re_enable():
                self.send_button.configure(state="normal", text="→")
                self.input_box.configure(state="normal")
            self.master_app.after(0, re_enable)