from agno.models.openai import OpenAIResponses
from agno.team import Team, TeamMode
from src.agents.finance_agent import finance_agent
from agno.db.postgres import PostgresDb
import os
from dotenv import load_dotenv
from src.agents.research_agent import research_agent

load_dotenv()
db_url = os.getenv("DATABASE_URL")
db = PostgresDb(db_url=db_url)

def get_analyst_team() -> Team:
    return Team(
        name="Equity Analyst Team",
        mode=TeamMode.route,
        model=OpenAIResponses(id="gpt-4o"),
        members=[finance_agent, research_agent],
        instructions=[
              "You are the lead equity analyst coordinating your team.",
              "Use the Finance Agent for fundamentals and price data.",
              "Use the Research Agent for news and market sentiment.",
              "Synthesize findings into actionable insights.",
          ],
        markdown=True,
        db=db,
        show_members_responses=True,
    )