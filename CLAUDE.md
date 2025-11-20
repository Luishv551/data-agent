# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CloudWalk Data Agent is a natural language interface for analyzing CloudWalk transaction data. Built with FastAPI backend and Next.js frontend, it uses OpenAI's API to convert natural language questions into structured queries executed against a transactions dataset.

**Tech Stack:**
- **Backend**: FastAPI, Python 3.12+, Pandas, OpenAI SDK
- **Frontend**: Next.js 15, React 19, TypeScript, Tailwind CSS, Recharts
- **Design**: Minimalist monochrome (black/white/gray palette)

## Development Commands

### Backend

```bash
cd backend

# Setup environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies with uv
uv add fastapi "uvicorn[standard]" pandas openai pydantic-settings python-dotenv

# Configure .env
# Create backend/.env and add:
# OPENAI_API_KEY=your_key_here

# Run server
uv run uvicorn app.main:app --reload
```

API docs available at: `http://localhost:8000/api/docs`

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
npm start
```

Frontend available at: `http://localhost:3000`

## Architecture

### High-Level Flow
1. User enters question in Next.js UI (React)
2. Frontend calls FastAPI backend via REST API
3. `LLMHandler` sends question to OpenAI with structured prompt
4. LLM returns JSON "query intent" (metric, filters, grouping)
5. `QueryExecutor` translates intent into pandas operations
6. `DataHandler` executes data operations and returns results
7. Backend returns JSON response to frontend
8. Frontend displays results with Recharts visualizations

### Backend Structure (`backend/`)

```
backend/
├── .venv/                 # Python virtual environment
├── .env                   # Environment variables (OPENAI_API_KEY)
├── pyproject.toml         # uv dependencies config
└── app/
    ├── api/
    │   ├── routes/
    │   │   ├── query.py        # POST /api/query endpoint
    │   │   └── data.py         # GET /api/data/summary endpoint
    │   └── dependencies.py     # Dependency injection (handlers)
    ├── core/
    │   ├── config.py          # Settings and configuration
    │   ├── data_handler.py    # Data operations
    │   ├── llm_handler.py     # OpenAI integration
    │   └── query_executor.py  # Query execution logic
    ├── models/
    │   ├── requests.py        # Pydantic request models
    │   └── responses.py       # Pydantic response models
    └── main.py               # FastAPI app initialization
```

#### Key Backend Components

**`app/main.py`** - FastAPI application
- CORS middleware for frontend communication
- Route registration
- Health check endpoints

**`app/core/config.py`** - Configuration
- Pydantic Settings for environment variables
- API settings, CORS origins, OpenAI config
- Data path configuration

**`app/core/data_handler.py`** - Data operations
- Loads CSV into memory with pandas
- Calculates TPV and average ticket
- Filters and groups data
- Generates dataset summary

**`app/core/llm_handler.py`** - LLM integration
- OpenAI API client wrapper
- Structured system prompt with examples
- Query intent validation
- Returns standardized JSON structure

**`app/core/query_executor.py`** - Query execution
- Executes LLM intents against data
- Handles grouped vs simple queries
- Applies sorting and limits
- Returns `QueryResult` objects

**`app/api/dependencies.py`** - Dependency injection
- Cached singleton instances using `@lru_cache`
- Provides `DataHandler`, `LLMHandler`, `QueryExecutor`

**`app/models/`** - Pydantic models
- Request/response validation
- Type safety
- Automatic API documentation

### Frontend Structure (`frontend/`)

```
frontend/
├── package.json           # npm dependencies
├── tsconfig.json          # TypeScript config
├── tailwind.config.js     # Tailwind config
├── next.config.js         # Next.js config
├── postcss.config.js      # PostCSS config (for Tailwind)
└── src/
    ├── app/
    │   ├── layout.tsx         # Root layout with metadata
    │   ├── page.tsx          # Main page component
    │   └── globals.css       # Global styles + Tailwind
    ├── components/
    │   ├── DataSummary.tsx   # Dataset statistics display
    │   ├── QueryInput.tsx    # Question input field
    │   ├── ExampleQuestions.tsx  # Quick question buttons
    │   ├── ResultsDisplay.tsx    # Results table and metrics
    │   └── Chart.tsx        # Recharts visualization
    ├── lib/
    │   └── api.ts          # Axios API client
    └── types/
        └── index.ts        # TypeScript interfaces
```

#### Key Frontend Components

**`src/app/page.tsx`** - Main page
- State management (summary, results, loading, error)
- Orchestrates API calls
- Renders all child components

**`src/lib/api.ts`** - API client
- Axios instance configured for backend
- `getDataSummary()`: Fetches dataset stats
- `processQuery()`: Sends questions to backend

**`src/components/`** - React components
- All styled with Tailwind CSS
- Minimalist design: gray/white/black palette
- Responsive layouts

**`src/types/index.ts`** - TypeScript types
- Matches backend Pydantic models
- Type safety across frontend

### Query Intent Structure

The LLM returns this JSON structure (same as before):

```json
{
  "metric": "tpv|average_ticket|transactions|merchants",
  "aggregation": "sum|mean|count",
  "group_by": ["column1", "column2"],
  "filters": {"column": "value"},
  "sort_by": "metric",
  "sort_order": "desc|asc",
  "limit": null|number,
  "explanation": "Brief explanation"
}
```

### Data Schema
The `transactions.csv` contains:
- `day`: Transaction date
- `entity`: "PF" (individual) or "PJ" (business)
- `product`: pix, pos, tap, link, bank_slip
- `price_tier`: normal, aggressive, intermediary, domination
- `anticipation_method`: D0/Nitro, D1Anticipation, Pix, Bank Slip
- `nitro_or_d0`: Nitro or D0
- `payment_method`: credit, debit, uninformed
- `installments`: Number of installments
- `amount_transacted`: Transaction amount (BRL)
- `quantity_transactions`: Count of transactions
- `quantity_of_merchants`: Count of merchants

### Business Metrics
- **TPV (Total Payment Volume)**: `SUM(amount_transacted)`
- **Average Ticket**: `SUM(amount_transacted) / SUM(quantity_transactions)`

## Code Standards and Best Practices

### Object-Oriented Design
- Use classes to encapsulate related functionality and state
- Each class should have a single, well-defined responsibility
- Use composition over inheritance (e.g., `QueryExecutor` depends on `DataHandler`)
- Keep classes cohesive - if a class does too many things, split it

### Evolutionary Code
- Design for change: separate concerns so modifications are isolated
- Follow the Open/Closed Principle: extend behavior without modifying existing code
- When adding features, first check if existing abstractions support the change
- Refactor as you go - if you notice duplication or unclear logic, improve it

### Clean and Organized Code
- Use descriptive names for variables, functions, and classes
- Keep functions focused on a single task
- Limit function length to what fits on one screen (~50 lines max)
- Group related functions together within classes
- Use type hints for function signatures (already present in codebase)
- Structure modules by responsibility, not by type (e.g., `data_handler.py` for all data operations)

### Professional Comments
- Only comment "why", not "what" - the code should be self-explanatory
- Use docstrings for public classes and methods (following existing format)
- Avoid obvious comments like `# increment counter` or `# loop through items`
- Update comments when code changes - outdated comments are worse than no comments
- Use comments to explain business logic, edge cases, or non-obvious decisions

### Avoid Overengineering
- Don't add abstractions until you need them
- Don't create interfaces or base classes for single implementations
- Avoid premature optimization - make it work, then make it fast if needed
- Don't add configuration for things that won't change
- Keep it simple: if a function works with 3 parameters, don't create a complex config object
- YAGNI (You Aren't Gonna Need It): don't build features for hypothetical future requirements

### Error Handling
- Validate inputs at boundaries (user input, API responses, file loading)
- Let exceptions bubble up unless you can meaningfully handle them
- Use specific exception types, not generic `Exception`
- Provide clear error messages that help users understand what went wrong

### Testing Considerations
- Write code that's easy to test: pure functions, dependency injection
- Keep business logic separate from UI/framework code
- If you can't easily test something, it's a sign the design needs improvement

## Code Patterns

### Adding New Metrics

**Backend:**
1. Update `backend/app/core/llm_handler.py` SYSTEM_PROMPT with new metric
2. Add calculation in `backend/app/core/query_executor.py`:
   - `_execute_grouped_query()` for grouped queries
   - `_execute_simple_query()` for simple queries
   - `_get_metric_name()` for display name
3. Update validation in `LLMHandler._validate_query_intent()`
4. Add to `valid_metrics` list

**Frontend:**
- Update `frontend/src/types/index.ts` QueryIntent type if needed
- Formatting logic in `ResultsDisplay.tsx` may need adjustment

### Adding New API Endpoints

1. Create route in `backend/app/api/routes/`
2. Define Pydantic models in `backend/app/models/`
3. Add route to `backend/app/main.py`
4. Create API function in `frontend/src/lib/api.ts`
5. Use in frontend components

### Modifying Visualizations

**Location:** `frontend/src/components/Chart.tsx`

- Uses Recharts library (BarChart, LineChart)
- Automatically selects:
  - Line chart for time series (`day`)
  - Bar chart with ordered days for `day_of_week`
  - Bar chart for other groupings
- Minimalist styling (black bars/lines, gray grid)

### Frontend Styling

All components use Tailwind CSS with custom theme:

**Colors:**
- `primary`: #1A1A1A (black)
- `primary-light`: #2C2C2C
- `secondary`: #666666 (gray)
- `surface`: #F5F5F5 (light gray)
- `surface-dark`: #E0E0E0

**Custom classes in `globals.css`:**
- `.card`, `.btn-primary`, `.btn-secondary`
- `.input`, `.metric-card`, `.table`

## Important Notes

### Backend
- Uses `uv` for dependency management (not pip)
- All data operations use pandas DataFrames
- DataHandler loads entire CSV into memory (cached with `@lru_cache`)
- OpenAI API key required in `backend/.env`
- LLM uses `response_format={"type": "json_object"}` for reliable JSON
- FastAPI dependency injection provides singleton handlers
- Data path configured in `config.py` (relative to backend/)
- Virtual environment in `backend/.venv/`

### Frontend
- Next.js 15 with App Router (not Pages Router)
- Server/Client components: use `'use client'` directive when needed
- API calls use axios
- State managed with React useState hooks
- Recharts for visualizations
- Tailwind for all styling (no CSS modules)

### Data
- `transactions.csv` must be in `data/` directory
- `day_of_week` computed on load
- Date parsing with pandas `to_datetime`

### Development
- Backend auto-reloads with `uv run uvicorn app.main:app --reload`
- Frontend hot-reloads with `npm run dev`
- CORS configured for localhost:3000
- TypeScript strict mode enabled
- Use `uv add` to add new Python dependencies
- VSCode: Configure Python interpreter to `backend/.venv/Scripts/python.exe`
