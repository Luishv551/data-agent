# CloudWalk Data Agent

Natural language interface for analyzing CloudWalk transaction data. Query business KPIs using plain English, powered by OpenAI and built with FastAPI + Next.js.

## Features

- **Natural Language Queries**: Ask questions like "What was the TPV for the last 3 days?" or "Which product has the highest average ticket?"
- **Business KPIs**: TPV, Average Ticket, transaction counts, merchant counts
- **Smart Segmentation**: Analyze by entity, product, payment method, price tier, anticipation method
- **Automated Visualizations**: Bar charts, line charts, responsive design
- **Daily Alerts**: Automated anomaly detection with D-1, D-7, D-30 variations
- **Query Transparency**: View reasoning summary and generated query intent

## Tech Stack

**Backend**
- FastAPI (Python 3.12+)
- Pandas for data operations
- OpenAI API (GPT-4o-mini)
- Pydantic for validation
- UV for dependency management

**Frontend**
- Next.js 15 (App Router)
- React 19
- TypeScript
- Tailwind CSS
- Recharts for visualizations

## Architecture

```
User Question → FastAPI Backend
                    ↓
              LLM Handler (OpenAI)
                    ↓
         Query Intent (JSON)
                    ↓
         Query Executor (Pandas)
                    ↓
              Data Handler
                    ↓
         JSON Response → Next.js Frontend
                              ↓
                    Recharts Visualization
```

### Query Translation Flow

1. **User Input**: Natural language question
2. **LLM Processing**: OpenAI converts to structured query intent
3. **Query Intent**: JSON object with metric, filters, grouping, sorting
4. **Pandas Execution**: Direct data operations (no SQL)
5. **Response**: Results + metadata + reasoning summary
6. **Visualization**: Automatic chart type selection

## Setup

### Prerequisites

- Python 3.12+
- Node.js 18+
- OpenAI API key

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install UV (if not installed)
pip install uv

# Install dependencies
uv add fastapi "uvicorn[standard]" pandas openai pydantic-settings python-dotenv

# Configure environment
echo "OPENAI_API_KEY=your_key_here" > .env

# Run server
uv run uvicorn app.main:app --reload
```

API documentation: http://localhost:8000/api/docs

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Application: http://localhost:3000

### Data Setup

Place your `transactions.csv` in the `data/` directory with the following schema:

```csv
day,entity,product,price_tier,anticipation_method,payment_method,installments,amount_transacted,quantity_transactions,quantity_of_merchants
```

## Usage Examples

### Natural Language Queries

- "Which product has the highest TPV?"
- "How do weekdays influence TPV?"
- "What was the average ticket for businesses last week?"
- "Show me the top 3 products by transaction volume"
- "What is the most used anticipation method by individuals?"

### API Endpoints

**Query Endpoint**
```http
POST /api/query
Content-Type: application/json

{
  "question": "What is the TPV for pix transactions?"
}
```

**Alerts Endpoint**
```http
GET /api/alerts?period=d30&metric=tpv
```

**Data Summary**
```http
GET /api/data/summary
```

## Project Structure

```
data-agent/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/         # API endpoints
│   │   │   └── dependencies.py # Dependency injection
│   │   ├── core/
│   │   │   ├── config.py       # Configuration
│   │   │   ├── data_handler.py # Data operations
│   │   │   ├── llm_handler.py  # OpenAI integration
│   │   │   ├── query_executor.py # Query execution
│   │   │   └── alerts_handler.py # Alert logic
│   │   ├── models/
│   │   │   ├── requests.py     # Request models
│   │   │   └── responses.py    # Response models
│   │   └── main.py            # FastAPI app
│   ├── .env                   # Environment variables
│   └── pyproject.toml         # Dependencies
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx     # Root layout
│   │   │   └── page.tsx       # Main page
│   │   ├── components/        # React components
│   │   ├── lib/api.ts         # API client
│   │   └── types/index.ts     # TypeScript types
│   ├── package.json
│   └── tailwind.config.js
├── data/
│   └── transactions.csv       # Dataset
└── README.md
```

## Code Standards

- **Object-Oriented Design**: Single responsibility, composition over inheritance
- **Clean Code**: Descriptive naming, type hints, focused functions
- **No Overengineering**: Simple solutions, YAGNI principle
- **Error Handling**: Validation at boundaries, specific exceptions
- **Testing**: Pure functions, dependency injection for testability

## Alerts System

### Daily Summary
- Current metric value (TPV, Average Ticket, Transactions)
- Percentage variation vs D-1, D-7, D-30

### Anomaly Detection
- **Method**: Z-score based (threshold: ±2σ or ±15%)
- **Segments**: Product, Entity, Payment Method
- **Metrics**: TPV, Average Ticket

### Top Insights
- Largest drop (most negative variation)
- Main contributor (highest absolute value)
- Highest growth (most positive variation)

## Design System

**Color Palette**
- Primary: #1A1A1A (black)
- Surface: #F5F5F5 (light gray)
- Secondary: #666666 (gray)
- Dark accents: #374151, #1f2937

**Components**
- Minimalist card-based layout
- Monochrome theme (black/white/gray)
- Responsive design
- Data-first approach

## Development Notes

### Evolution

1. **Phase 1**: Streamlit prototype for rapid backend testing
2. **Phase 2**: Migrated to Next.js for production-grade UI

### Technical Decisions

- **Pandas over SQL**: Simpler for analytics, no database setup, in-memory operations
- **Few-shot prompting**: Structured JSON output, no LangChain/LlamaIndex complexity
- **FastAPI**: Modern Python, automatic OpenAPI docs, async support
- **Next.js 15**: Server/client components, optimal performance

## License

MIT License - See LICENSE file for details

## Author

Built as a technical assessment for CloudWalk.
