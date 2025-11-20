# Quick Start

## Pré-requisitos

- Python 3.12+
- Node.js 18+
- uv (gerenciador Python)
- OpenAI API key

## Setup Backend

```bash
cd backend

# Criar e ativar ambiente virtual
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Instalar dependências
uv add fastapi "uvicorn[standard]" pandas openai pydantic-settings python-dotenv

# Configurar .env
# Editar backend/.env e adicionar:
# OPENAI_API_KEY=sua_chave_aqui

# Rodar servidor
uv run uvicorn app.main:app --reload
```

Backend: `http://localhost:8000`
API Docs: `http://localhost:8000/api/docs`

## Setup Frontend

```bash
cd frontend

# Instalar dependências
npm install

# Rodar dev server
npm run dev
```

Frontend: `http://localhost:3000`

## Testar

Abra `http://localhost:3000` e pergunte:
- "Which product has the highest TPV?"
- "How do weekdays influence TPV?"
- "Which segment has the highest average ticket?"

## Estrutura

```
data-agent/
├── backend/
│   ├── app/              # FastAPI
│   ├── .venv/           # Python env
│   ├── .env             # Variáveis
│   └── pyproject.toml   # Config uv
│
├── frontend/
│   ├── src/             # Next.js
│   └── package.json     # Config npm
│
└── data/
    └── transactions.csv
```

## Troubleshooting

**Backend não inicia:**
- Verifique se `.env` tem `OPENAI_API_KEY`
- Certifique-se que `data/transactions.csv` existe

**Frontend não conecta:**
- Backend deve estar rodando em `localhost:8000`
- Verifique CORS em `backend/app/core/config.py`
