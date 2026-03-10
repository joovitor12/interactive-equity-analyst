from agno.agent import Agent
from agno.tools.yfinance import YFinanceTools
from agno.models.openai import OpenAIChat


finance_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[YFinanceTools(...)],
    instructions=[
      "You are a senior equity analyst.",
      "Always provide data-driven insights.",
      "When analyzing a stock, include: current price, key fundamentals (P/E, EV/EBITDA), and analyst sentiment.",
      "Be concise but thorough.",
    ],
    markdown=True,
)

def get_finance_agent() -> Agent:
    return finance_agent