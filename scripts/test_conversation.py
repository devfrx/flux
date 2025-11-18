"""Test del conversation manager."""
import asyncio
from flux_agent.conversation import conversation_manager
from flux_agent.storage import db
from flux_agent.logging_config import logger


async def main():
    # Inizializza DB
    await db.initialize()
    
    # Crea conversazione
    conv_id = await conversation_manager.create_conversation("Test Chat")
    logger.info(f"✅ Conversazione creata: {conv_id}")
    
    print("\n" + "="*60)
    print("💬 CHAT INTERATTIVA CON L'AGENT")
    print("="*60)
    print("Comandi speciali:")
    print("  - 'exit' o 'quit' per uscire")
    print("  - 'history' per vedere lo storico")
    print("="*60 + "\n")
    
    while True:
        user_input = input("Tu: ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() in ["exit", "quit"]:
            print("\n👋 Arrivederci!")
            break
        
        if user_input.lower() == "history":
            history = await conversation_manager.get_conversation_history()
            print("\n📜 Storico conversazione:")
            for msg in history:
                print(f"  [{msg['timestamp']}] {msg['role']}: {msg['content'][:100]}...")
            print()
            continue
        
        # Genera risposta
        try:
            response = await conversation_manager.chat(user_input, max_tokens=500)
            print(f"AI: {response}\n")
        except Exception as e:
            print(f"❌ Errore: {e}\n")


if __name__ == "__main__":
    asyncio.run(main())