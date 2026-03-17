from agno.agent import Agent
from agno.tools.yfinance import YFinanceTools
from agno.models.openai import OpenAIChat


finance_agent = Agent(
    name="Finance Agent",
    model=OpenAIChat(id="gpt-4o"),
    tools=[
        YFinanceTools(
            enable_stock_price=True,
            enable_stock_fundamentals=True,
            enable_analyst_recommendations=True,
            enable_company_info=True,
        )
    ],
    role="Gets stock fundamentals, price data, and analyst ratings",
    instructions=[
        "You are a senior equity analyst.",
        "Always provide data-driven insights.",
        "When analyzing a stock, include: current price, key fundamentals (P/E, EV/EBITDA), and analyst sentiment.",
        "Be concise but thorough.",
    ],
    markdown=True,
)
