from agno.agent import Agent
from agno.models.openai import OpenAIChat

from src.knowledge.earnings import get_earnings_knowledge


def get_rag_agent() -> Agent:
    return Agent(
        name="RAG Agent",
        model=OpenAIChat(id="gpt-4o"),
        role="Analyzes earnings call transcripts and financial documents from the knowledge base",
        knowledge=get_earnings_knowledge(),
        search_knowledge=True,
        instructions=[
            "You analyze earnings call transcripts and financial documents.",
            "Extract qualitative insights about management tone, guidance, and strategy.",
            "Search the knowledge base for relevant information before answering.",
            "Quote relevant passages when possible.",
        ],
        markdown=True,
    )
