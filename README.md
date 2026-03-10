Project Brief: Interactive Equity Analyst Agent (Agno Framework)
Core Concept
An AI-powered financial co-pilot built with the Agno (formerly Phidata) framework. Unlike static dashboards (Investing.com/Webull), this system allows users to interrogate and debate market analyses and earnings reports using Multi-Agent orchestration and RAG.

Key Features
The "Analyst Critique" (Differentiator): Scrapes or ingests market opinions (e.g., Investing.com) and allows the user to ask follow-up questions to challenge the consensus.

Multi-Agent Workflow:

Research Agent: Uses DuckDuckGo or Firecrawl to fetch the latest market sentiment and news.

Finance Agent: Uses YFinanceTools to pull real-time fundamental data (P/E, EV/EBITDA, Analyst Ratings).

RAG Agent: Processes uploaded PDFs (Quarterly Earnings Calls) to extract qualitative insights (management "tone" vs. hard numbers).

Persistent Memory: Uses PostgreSQL to store investment theses, allowing the agent to remind the user of their original logic months later.

Tech Stack
Orchestration: Agno Framework

LLM: GPT-4o or Claude 3.5 Sonnet (via Agno OpenAIChat or Anthropic)

Database/Memory: PostgreSQL (for session storage and vector search via pgvector)

Tools: YFinanceTools, DuckDuckGo, FileTools (for PDF processing)

UI (Optional): Streamlit or FastHTML

Instructions for Cursor Agent
Initialize an Agno project structure with a dedicated agent.py.

Implement a Multi-Agent system where a MarketAnalyst agent hands off data to a ResearchAgent.

Setup a RAG pipeline using LanceDB or PostgreSQL to store Earnings Call transcripts.

Create a function-calling tool that specifically pulls Valuation Multiples to compare them with sector averages.