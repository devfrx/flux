flux_agent/
├── config.py          → Carica .env, variabili globali (già presente)
├── logging_config.py  → Setup dei logger (già presente)
├── storage.py         → Persistenza/cache (già presente)
│
├── models/            → **RUNTIME E MODELLI** (nuovo)
│   ├── __init__.py
│   ├── interface.py        → Protocol/ABC per tutti i modelli
│   └── adapters/
│       ├── __init__.py
│       └── dummy_adapter.py  → Esempio base (testo fisso)
│
├── manager.py         → **GESTIONE MODELLI** (carica/scarica/registro)
├── workers.py         → **ESECUZIONE ASINCRONA** (job queue semplice)
├── api.py             → **ENDPOINTS HTTP** (FastAPI)
│
├── agent.py           → Orchestrator principale (già presente)
└── sdk_client.py      → Client per chiamare l'API (già presente)


Dipendenze:
.env → config.py
          ↓
    logging_config.py
          ↓
      storage.py
          ↓
   models/interface.py
          ↓
   models/adapters/*
          ↓
      manager.py  ← usa adapters + storage + config
          ↓
      workers.py  ← usa manager per eseguire job
          ↓
        api.py    ← espone HTTP, delega a workers
          ↓
      agent.py    ← usa api o direttamente manager