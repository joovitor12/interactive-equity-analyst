from typing import Optional
from agno.tools import tool
from agno.tools.crawl4ai import Crawl4aiTools
from agno.tools.duckduckgo import DuckDuckGoTools

from src.knowledge.earnings import get_earnings_knowledge


_crawler = Crawl4aiTools(max_length=None, timeout=120)
_search = DuckDuckGoTools(enable_search=True, enable_news=True)


@tool()
def scrape_and_save_transcript(url: str, company: str, quarter: Optional[str] = None) -> str:
    """
    Scrape an earnings call transcript from a URL and save it to the knowledge base.

    Use this when the user provides a transcript URL to add to the knowledge base.

    Args:
        url: The URL of the earnings transcript to scrape
        company: Company name/ticker (e.g., "NVDA", "AAPL")
        quarter: Optional quarter identifier (e.g., "Q4 2024")

    Returns:
        Confirmation message
    """
    result = _crawler.crawl(url)

    if not result or len(result) < 100:
        return f"Failed to scrape content from {url}"

    knowledge = get_earnings_knowledge()
    knowledge.insert(
        text_content=result,
        metadata={
            "company": company.upper(),
            "quarter": quarter or "Unknown",
            "source_url": url,
            "type": "earnings_transcript",
        },
    )

    return f"Transcript for {company.upper()} ({quarter or 'Unknown quarter'}) saved to knowledge base. Scraped {len(result)} characters."


@tool()
def search_transcripts(ticker: str) -> str:
    """
    Search for earnings call transcripts for a specific company.
    
    Use this to find transcript URLs for a company before scraping them.
    
    Args:
        ticker: Stock ticker symbol (e.g., "NVDA", "AAPL", "TSLA")
    
    Returns:
        Search results with transcript URLs from Investing.com
    """
    query = f"site:investing.com/news/transcripts {ticker} earnings call transcript"
    result = _search.web_search(query, max_results=5)
    return f"Found transcripts for {ticker}:\n\n{result}"
