from dotenv import load_dotenv

load_dotenv()

from src.agents.finance_agent import get_finance_agent
from src.agents.research_agent import get_research_agent
from src.agents.team import get_analyst_team

finance_agent = get_finance_agent()
research_agent = get_research_agent()

import sys
if len(sys.argv) > 1:
    if sys.argv[1] == "research":
        agent = get_research_agent()
    elif sys.argv[1] == "team":
        agent = get_analyst_team()
    else:
        agent = get_finance_agent()
else:
    agent = get_analyst_team()

agent.print_response("Give me a complete analysis of NVDA - both fundamentals and recent news")