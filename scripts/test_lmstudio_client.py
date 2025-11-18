"""Test della classe base ModelInterface."""
import asyncio
from flux_agent.models.interface import ModelInterface, Message
from flux_agent.models.lmstudio_client import LMStudioClient


async def main():
    # Verifica che LMStudioClient sia una sottoclasse corretta
    assert issubclass(LMStudioClient, ModelInterface)
    print("✅ LMStudioClient implementa ModelInterface correttamente")
    
    # Test istanza
    client = LMStudioClient()
    print(f"✅ Istanza creata: {client}")
    
    # Test metodi astratti implementati
    messages = [Message(role="user", content="ricorda la parola banana")]
    try:
        response = await client.generate(messages, max_tokens=2000)
        print(f"✅ Generate funziona: {len(response)} caratteri")
    except Exception as e:
        print(f"⚠️ Generate errore (atteso se LMStudio non è attivo): {e}")
    
    await client.close()
    print("✅ Client chiuso correttamente")


if __name__ == "__main__":
    asyncio.run(main())