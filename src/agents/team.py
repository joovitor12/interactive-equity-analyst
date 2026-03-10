from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.team import Team, TeamMode
from src.agents.finance_agent import get_finance_agent
from src.agents.research_agent import get_research_agent

def get_analyst_team() -> Team:
    return Team(
        name="Equity Analyst Team",
        mode=TeamMode.route,
        model=OpenAIResponses(id="gpt-4o"),
        members=[get_finance_agent(), get_research_agent()],
        instructions=[
              "You are the lead equity analyst coordinating your team.",
              "Use the Finance Agent for fundamentals and price data.",
              "Use the Research Agent for news and market sentiment.",
              "Synthesize findings into actionable insights.",
          ],
        markdown=True,
    )