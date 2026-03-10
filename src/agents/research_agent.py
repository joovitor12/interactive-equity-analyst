from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools

research_agent = Agent(
    name="Research Agent",
    model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGoTools(...)],
     instructions=[
      "You are a financial research analyst.",
      "Search for the latest news, market sentiment, and analyst opinions.",
      "Summarize findings concisely with source context.",
      "Focus on material information that could impact investment decisions.",
    ],
)

def get_research_agent() -> Agent:
    return research_agent