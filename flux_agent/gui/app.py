"""Finestra principale con design premium."""
import customtkinter as ctk
import asyncio
import threading
from flux_agent.gui.sidebar import Sidebar
from flux_agent.gui.chat_panel import ChatPanel
from flux_agent.gui.theme import C, Theme
from flux_agent.conversation import conversation_manager
from flux_agent.storage import db
from flux_agent.logging_config import logger


class FluxAgentApp(ctk.CTk):
    """App principale con design moderno e premium."""
    
    def __init__(self):
        super().__init__()
        
        # Configurazione finestra
        self.title("Flux Agent")
        self.geometry("1400x900")
        
        # Applica tema custom
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Colore background principale
        self.configure(fg_color=C["bg_primary"])
        
        # Event loop asyncio
        self.loop = asyncio.new_event_loop()
        self.loop_thread = threading.Thread(target=self._run_event_loop, daemon=True)
        self.loop_thread.start()
        
        # Layout grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)  # Sidebar fissa
        self.grid_columnconfigure(1, weight=1)  # Chat espandibile
        
        # Sidebar
        self.sidebar = Sidebar(
            self,
            on_new_chat=self.create_new_chat,
            on_select_chat=self.select_chat
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Chat panel
        self.chat_panel = ChatPanel(
            self,
            on_send_message=self.send_message
        )
        self.chat_panel.grid(row=0, column=1, sticky="nsew")
        
        # Inizializza
        self.run_async(self._initialize())
    
    def _run_event_loop(self):
        """Esegue event loop asyncio."""
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()
    
    def run_async(self, coro):
        """Esegue coroutine nell'event loop."""
        return asyncio.run_coroutine_threadsafe(coro, self.loop)
    
    async def _initialize(self):
        """Inizializza database."""
        await db.initialize()
        logger.info("✅ GUI avviata")
        await self.create_new_chat()
    
    def create_new_chat(self):
        """Crea nuova conversazione."""
        self.run_async(self._create_new_chat())
    
    async def _create_new_chat(self):
        """Crea nuova conversazione (async)."""
        conv_id = await conversation_manager.create_conversation("Nuova Chat")
        self.after(0, lambda: self.sidebar.add_conversation(conv_id, "Nuova Chat"))
        self.after(0, self.chat_panel.clear_messages)
        logger.info(f"Nuova chat: {conv_id}")
    
    def select_chat(self, conv_id: int):
        """Carica conversazione."""
        self.run_async(self._select_chat(conv_id))
    
    async def _select_chat(self, conv_id: int):
        """Carica conversazione (async)."""
        conversation_manager.current_conversation_id = conv_id
        history = await conversation_manager.get_conversation_history()
        
        def update_ui():
            self.chat_panel.clear_messages()
            for msg in history:
                if msg["role"] in ["user", "assistant"]:
                    self.chat_panel.add_message(msg["role"], msg["content"])
        
        self.after(0, update_ui)
        logger.info(f"Caricata conversazione: {conv_id}")
    
    async def send_message(self, message: str) -> str:
        """Invia messaggio e riceve risposta."""
        try:
            response = await conversation_manager.chat(message, max_tokens=1000)
            return response
        except Exception as e:
            logger.error(f"Errore: {e}")
            return f"Errore: {e}"
    
    def run(self):
        """Avvia mainloop."""
        try:
            self.mainloop()
        finally:
            self.loop.call_soon_threadsafe(self.loop.stop)