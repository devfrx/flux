"""Manager delle conversazioni con context window."""

from typing import List
import aiosqlite
from flux_agent.models.interface import Message
from flux_agent.models.lmstudio_client import lm_client
from flux_agent.config import settings
from flux_agent.logging_config import logger

class ConversationManager:
    """Gestisce conversazioni, salvataggio DB e context window."""

    def __init__(self, max_context_messages: int = 10):
        """
        Args:
            max_context_messages: Numero massimo di messaggi da mantenere nel context
        """
        self.max_context_messages = max_context_messages
        self.current_conversation_id: int | None = None
        self.system_prompt = "Sei un assistente personale utile, preciso e conciso."

    async def create_conversation(self, title: str = "New Convo") -> int:
        """Crea una nuova conversazione."""

        async with  aiosqlite.connect(settings.database_path) as conn:
            cursor = await conn.execute(
                 "INSERT INTO conversations (title) VALUES (?)",
                (title,)
            )
            await conn.commit()
            conv_id = cursor.lastrowid

        self.current_conversation_id = conv_id
        logger.info(f"Conversazione creata: ID={conv_id}, title='{title}'")
        return conv_id
        
    async def add_message(self, role: str, content: str) -> None:
        """Aggiunge un messaggio alla conversazione corrente."""
    
        if not self.current_conversation_id:
            await self.create_conversation()

        async with aiosqlite.connect(settings.database_path) as conn:
            cursor = await conn.execute(
                "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
                (self.current_conversation_id, role, content)
            )
            await conn.commit()

        logger.debug(f"Messaggio salvato: {role} - {len(content)} caratteri")

    async def get_messages(self, limit: int | None = None) -> List[Message]:
        """Recupera gli ultimi N messaggi della conversazione."""
        if not self.current_conversation_id:
            return []

        query_limit = limit or self.max_context_messages

        async with aiosqlite.connect(settings.database_path) as conn:
            cursor = await conn.execute(
                 """
                SELECT role, content FROM messages 
                WHERE conversation_id = ? 
                ORDER BY created_at DESC 
                LIMIT ?
                """,
                (self.current_conversation_id, query_limit)
            )
            rows = await cursor.fetchall()

        # Inverto l'ordine (dal più vecchio al più recente)
        messages = [Message(role = row[0], content = row[1]) for row in reversed(rows)]
        return messages

    async def chat(self, user_message: str, temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """
        Invia un messaggio e riceve la risposta.
        
        Args:
            user_message: Messaggio dell'utente
            temperature: Creatività della risposta (0.0-1.0)
            max_tokens: Lunghezza massima della risposta
        
        Returns:
            str: Risposta dell'assistente
        """

        # Salva messaggio utente
        await self.add_message("user", user_message)

        # Recupera contenxt
        messages = await self.get_messages()

        # Aggiungo system prompt se è il primo messaggio
        if len(messages) == 1:
            messages.insert(0, Message(role = "system", content = self.system_prompt))

        # Genero risposta
        logger.info(f"Generazione risposta (context: {len(messages)} messaggi)")
        response = await lm_client.generate(messages, temperature = temperature, max_tokens = max_tokens)

        # Salvo la risposta
        await self.add_message("assistant", response)

        return response

    async def get_conversation_history(self) -> List[dict]:
        """Restituisce lo storico completo della conversazione corrente."""

        if not self.current_conversation_id:
            return []

        async with aiosqlite.connect(settings.database_path) as conn:
            cursor = await conn.execute(
                                """
                SELECT role, content, created_at FROM messages 
                WHERE conversation_id = ? 
                ORDER BY created_at ASC
                """,
                (self.current_conversation_id,)
            )
            rows = await cursor.fetchall()

        return [
            {"role": row[0], "content": row[1], "timestamp": row[2]}
            for row in rows
        ]

# Istanza globale
conversation_manager = ConversationManager()