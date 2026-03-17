import os
from dotenv import load_dotenv

from agno.models.openai import OpenAIChat
from agno.team import Team
from agno.team.mode import TeamMode
from agno.tools.yfinance import YFinanceTools
from agno.db.postgres import PostgresDb

from src.agents.finance_agent import finance_agent
from src.agents.research_agent import research_agent
from src.agents.rag_agent import get_rag_agent
from src.tools.thesis_tools import save_thesis, get_theses
from src.tools.transcript_tools import scrape_and_save_transcript, search_transcripts
from src.tools.analyst_tools import fetch_analyst_ratings, get_analyst_opinions, compare_thesis_to_consensus

load_dotenv()

db_url = os.getenv("DATABASE_URL")
db = PostgresDb(db_url=db_url)


def get_analyst_team(session_id: str) -> Team:
    return Team(
        name="Equity Analyst Team",
        mode=TeamMode.coordinate,
        model=OpenAIChat(id="gpt-4o"),
        members=[finance_agent, research_agent, get_rag_agent()],
        tools=[
            save_thesis,
            get_theses,
            YFinanceTools(enable_stock_price=True),
            scrape_and_save_transcript,
            search_transcripts,
            fetch_analyst_ratings,
            get_analyst_opinions,
            compare_thesis_to_consensus,
        ],
        instructions=[
            "You are the lead equity analyst coordinating your team.",
            "You have direct access to stock prices via YFinance tools.",
            "Delegate to Finance Agent for detailed fundamentals and analyst ratings.",
            "Delegate to Research Agent for news and market sentiment.",
            "Delegate to RAG Agent for questions about earnings calls, transcripts, and financial documents.",
            "Use save_thesis ONLY when the user explicitly provides a thesis.",
            "Use get_theses to retrieve saved theses.",
            "Use search_transcripts to find earnings call transcripts for a company by ticker.",
            "Use scrape_and_save_transcript to add earnings transcripts from URLs to the knowledge base.",
            "ANALYST CRITIQUE FEATURE:",
            "- Use fetch_analyst_ratings to get Wall Street consensus ratings and price targets from YFinance.",
            "- Use get_analyst_opinions to retrieve saved analyst views.",
            "- Use compare_thesis_to_consensus to show side-by-side: user's thesis vs Wall Street opinion.",
            "When the user wants to challenge or debate market opinions, use compare_thesis_to_consensus.",
            "When comparing a thesis to current data:",
            "1) First call get_theses to retrieve the thesis",
            "2) Then get the current stock price",
            "3) Synthesize into a comprehensive comparison",
            "CRITICAL: After gathering data from tools AND agents, synthesize ALL results into a single comprehensive response.",
        ],
        db=db,
        session_id=session_id,
        add_history_to_context=True,
        show_members_responses=True,
        markdown=True,
    )
