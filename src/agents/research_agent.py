from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools


research_agent = Agent(
    name="Research Agent",
    model=OpenAIChat(id="gpt-4o"),
    tools=[
        DuckDuckGoTools(
            enable_search=True,
            enable_news=True,
        )
    ],
    role="Searches the web for news and market sentiment",
    instructions=[
        "You are a financial research analyst.",
        "Search for the latest news, market sentiment, and analyst opinions.",
        "Summarize findings concisely with source context.",
        "Focus on material information that could impact investment decisions.",
    ],
    markdown=True,
)
