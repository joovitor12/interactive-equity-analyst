import os
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.vectordb.pgvector import PgVector
from agno.vectordb.search import SearchType


def get_earnings_knowledge() -> Knowledge:
    return Knowledge(
        vector_db=PgVector(
            table_name="earnings_documents",
            db_url=os.getenv("DATABASE_URL"),
            embedder=OpenAIEmbedder(id="text-embedding-3-small"),
            search_type=SearchType.hybrid,
        ),
    )
