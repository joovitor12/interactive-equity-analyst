from dotenv import load_dotenv

load_dotenv()

from src.agents.finance_agent import get_finance_agent

finance_agent = get_finance_agent()

finance_agent.print_response("What is the current price of Tesla?")