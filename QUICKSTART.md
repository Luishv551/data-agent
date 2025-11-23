# Quick Start

## Prerequisites

- Python 3.12+
- Node.js 18+
- OpenAI API key

## Backend Setup

**Install uv** (if not already installed):
```bash
pip install uv
```

**Setup:**
```bash
cd backend

# Create virtual environment
uv venv

# Activate virtual environment
.venv\Scripts\activate       # Windows

# Install dependencies
uv sync

# Configure environment variables
# Create .env file with: OPENAI_API_KEY=your_key_here

# Start development server
uv run uvicorn app.main:app --reload
```

- Backend: http://localhost:8000
- API Docs: http://localhost:8000/api/docs

## Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

- Frontend: http://localhost:3000

## Testing

Open http://localhost:3000 and try:
- "Which product has the highest TPV?"
- "How do weekdays influence TPV?"
- "Which segment has the highest average ticket?"

## Troubleshooting

**Backend won't start:**
- Verify `.env` contains `OPENAI_API_KEY`
- Ensure `data/transactions.csv` exists

**Frontend can't connect:**
- Backend must be running on `localhost:8000`
