"""Gestione database SQLite."""
import aiosqlite
from pathlib import Path
from flux_agent.config import settings
from flux_agent.logging_config import logger

class Database:
    """Gestore del database SQLite."""

    def __init__(self, db_path: str | None = None):
        self.db_path = db_path or settings.database_path
        Path(self.db_path).parent.mkdir(parents = True, exist_ok = True)

    async def initialize(self) -> None:
        """Crea le tabelle se non esistono."""
        async with aiosqlite.connect(self.db_path) as db:
            # Tabella conversazioni
            await db.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    title TEXT
                )
            """)

            # Tabella messaggi
            await db.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id INTEGER NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
                )
            """)

            await db.commit()
            logger.info(f"Database inizializzato: {self.db_path}")

    async def save_message(self, conversation_id: int, role: str, content: str) -> int:
        """Salva un messaggio."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
                (conversation_id, role, content)
            )

            await db.commit()
            return cursor.lastrowid

# Istanza globale
db = Database()