from agno.models.openai import OpenAIResponses
from agno.team import Team, TeamMode
from agno.tools.yfinance import YFinanceTools
from src.agents.finance_agent import finance_agent
from agno.db.postgres import PostgresDb
import os
from dotenv import load_dotenv
from src.agents.research_agent import research_agent
from src.tools.thesis_tools import save_thesis, get_theses
load_dotenv()
db_url = os.getenv("DATABASE_URL")
db = PostgresDb(db_url=db_url)

def get_analyst_team(session_id: str) -> Team:
    return Team(
        name="Equity Analyst Team",
        mode=TeamMode.route,
        model=OpenAIResponses(id="gpt-4o"),
        members=[finance_agent, research_agent],
        tools=[save_thesis, get_theses, YFinanceTools()],
        instructions=[
            "You are the lead equity analyst.",
            "You have direct access to stock prices via YFinance tools.",
            "Delegate to Finance Agent for detailed fundamentals and analyst ratings.",
            "Delegate to Research Agent for news and market sentiment.",
            "Use save_thesis ONLY when the user explicitly provides a thesis.",
            "Use get_theses to retrieve saved theses.",
            "When comparing a thesis to current data:",
            "1) First call get_theses to retrieve the thesis",
            "2) Then get the current stock price",
            "3) Synthesize into a comprehensive comparison",
        ],
        add_history_to_context=True,
        markdown=True,
        session_id=session_id,
        db=db,
        show_members_responses=True,
    )