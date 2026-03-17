# Interactive Equity Analyst Agent

An AI-powered financial co-pilot built with the [Agno](https://github.com/agno-agi/agno) framework. Unlike static dashboards (Investing.com/Webull), this system allows users to interrogate and debate market analyses and earnings reports using Multi-Agent orchestration and RAG.

## Key Features

### Analyst Critique (Differentiator)
Challenge Wall Street consensus with your own investment thesis. The system fetches real analyst ratings (55+ analysts for major stocks) and compares them to your views.

### Multi-Agent Workflow
- **Finance Agent**: Real-time stock data, fundamentals, and analyst recommendations via YFinance
- **Research Agent**: Latest news and market sentiment via DuckDuckGo
- **RAG Agent**: Query earnings call transcripts stored in vector database

### Persistent Memory
PostgreSQL (Supabase) stores your investment theses, allowing the agent to remind you of your original logic months later.

## Tech Stack

- **Orchestration**: Agno Framework
- **LLM**: GPT-4o (via Agno OpenAIChat)
- **Database**: Supabase PostgreSQL (sessions + pgvector for RAG)
- **Tools**: YFinance, DuckDuckGo, Crawl4AI

## Setup

### 1. Clone and Install Dependencies

```bash
git clone <repo-url>
cd interactive-equity-analyst
uv sync
```

### 2. Install Playwright (for web scraping)

```bash
playwright install
```

### 3. Configure Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_key
DATABASE_URL=postgresql+psycopg://postgres.xxx:password@aws-0-region.pooler.supabase.com:6543/postgres
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_KEY=your_service_key
```

### 4. Run Database Migrations

```bash
uv run alembic upgrade head
```

### 5. Enable pgvector in Supabase

Run in Supabase SQL Editor:
```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

## Usage

```bash
uv run main.py
```

## Example Workflows

### 1. Save Your Investment Thesis

```
I'm bullish on NVDA. AI datacenter demand will triple by 2027, and they have 80% market share in training GPUs. Current price around $185, target $300.
```

### 2. Get Wall Street Analyst Ratings

```
Get analyst ratings for NVDA
```

**Output**: Real data from 55 analysts - Strong Buy consensus, mean target $267, high target $380.

### 3. Compare Your Thesis to Consensus (Analyst Critique)

```
Compare my NVDA thesis to Wall Street consensus
```

**Output**: Side-by-side comparison showing your $300 target vs analyst mean of $267.

### 4. Research Latest News

```
What's the latest news on Tesla?
```

### 5. Get Stock Fundamentals

```
Give me a complete analysis of AAPL - fundamentals and recent news
```

### 6. Search for Earnings Transcripts

```
Find NVDA earnings transcripts
```

### 7. Scrape and Save a Transcript

```
Scrape and save the transcript from https://www.investing.com/news/transcripts/...
```

### 8. Query the Knowledge Base

```
What did NVIDIA management say about AI demand in their earnings call?
```

### 9. Track Your Thesis Over Time

```
What are my investment theses on NVDA?
```

```
Give me current NVDA data and compare it to my original thesis.
```

## Project Structure

```
interactive-equity-analyst/
├── src/
│   ├── agents/
│   │   ├── finance_agent.py    # YFinance tools
│   │   ├── research_agent.py   # DuckDuckGo search
│   │   ├── rag_agent.py        # Knowledge base queries
│   │   └── team.py             # Multi-agent orchestration
│   ├── tools/
│   │   ├── thesis_tools.py     # Save/retrieve investment theses
│   │   ├── transcript_tools.py # Scrape earnings transcripts
│   │   └── analyst_tools.py    # Fetch Wall Street ratings
│   └── knowledge/
│       └── earnings.py         # Vector DB configuration
├── alembic/                    # Database migrations
├── main.py                     # Entry point
├── pyproject.toml
└── .env
```

## Database Tables

- `investment_theses`: Your bull/bear cases with price targets
- `analyst_opinions`: Wall Street ratings and price targets
- `ai.earnings_documents`: Vectorized earnings transcripts (pgvector)
- `ai.agno_sessions`: Conversation history

## License

MIT
