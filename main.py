from dotenv import load_dotenv

load_dotenv()

from src.agents.team import get_analyst_team

team = get_analyst_team(session_id="123")

while True:
    query = input("\n Ask the analyst or 'exit' to quit: ")
    if query.lower() == "exit":
        break
    response = team.print_response(query)
