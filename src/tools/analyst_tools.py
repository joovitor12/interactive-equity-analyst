import os
from typing import Optional
from agno.tools import tool
import yfinance as yf
from sqlalchemy import create_engine, text


_engine = None


def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(os.getenv("DATABASE_URL"))
    return _engine


@tool()
def fetch_analyst_ratings(ticker: str) -> str:
    """
    Fetch and save current analyst ratings and price targets for a stock using YFinance.
    
    This gets Wall Street consensus - Buy/Hold/Sell ratings, price targets, and recommendations.
    Use this to get the "market opinion" that the user can then challenge or debate.
    
    Args:
        ticker: Stock ticker symbol (e.g., "NVDA", "AAPL", "TSLA")
    
    Returns:
        Summary of analyst ratings and price targets
    """
    stock = yf.Ticker(ticker.upper())
    
    # Get analyst recommendations
    try:
        recommendations = stock.recommendations
        if recommendations is not None and len(recommendations) > 0:
            recent_recs = recommendations.tail(10)
            rec_summary = recent_recs.to_string()
        else:
            rec_summary = "No recent recommendations available"
    except Exception:
        rec_summary = "Could not fetch recommendations"
    
    # Get price targets
    try:
        info = stock.info
        target_high = info.get('targetHighPrice', 'N/A')
        target_low = info.get('targetLowPrice', 'N/A')
        target_mean = info.get('targetMeanPrice', 'N/A')
        target_median = info.get('targetMedianPrice', 'N/A')
        recommendation = info.get('recommendationKey', 'N/A')
        num_analysts = info.get('numberOfAnalystOpinions', 'N/A')
        current_price = info.get('currentPrice', info.get('regularMarketPrice', 'N/A'))
    except Exception:
        target_high = target_low = target_mean = target_median = 'N/A'
        recommendation = num_analysts = current_price = 'N/A'
    
    # Build summary
    summary = f"""Analyst Consensus for {ticker.upper()}:
- Recommendation: {recommendation}
- Number of Analysts: {num_analysts}
- Current Price: ${current_price}
- Price Target (Mean): ${target_mean}
- Price Target (Median): ${target_median}
- Price Target (High): ${target_high}
- Price Target (Low): ${target_low}

Recent Recommendations:
{rec_summary}"""
    
    # Determine rating string
    rating = str(recommendation).upper() if recommendation != 'N/A' else None
    
    # Save to database
    query = text("""
        INSERT INTO analyst_opinions (ticker, source, rating, price_target, summary, raw_content)
        VALUES (:ticker, :source, :rating, :price_target, :summary, :raw_content)
        RETURNING id
    """)
    
    with get_engine().connect() as conn:
        result = conn.execute(query, {
            "ticker": ticker.upper(),
            "source": "YFinance (Wall Street Consensus)",
            "rating": rating,
            "price_target": float(target_mean) if target_mean != 'N/A' else None,
            "summary": summary[:500],
            "raw_content": summary,
        })
        conn.commit()
        opinion_id = result.fetchone()[0]
    
    return f"Analyst ratings for {ticker.upper()} saved.\n\n{summary}"


@tool()
def get_analyst_opinions(ticker: str) -> str:
    """
    Retrieve saved analyst opinions for a stock.
    
    Args:
        ticker: Stock ticker symbol
    
    Returns:
        All saved analyst opinions for the ticker
    """
    query = text("""
        SELECT source, rating, price_target, summary, scraped_at
        FROM analyst_opinions
        WHERE ticker = :ticker
        ORDER BY scraped_at DESC
        LIMIT 5
    """)
    
    with get_engine().connect() as conn:
        result = conn.execute(query, {"ticker": ticker.upper()})
        rows = result.fetchall()
    
    if not rows:
        return f"No analyst opinions found for {ticker.upper()}. Use scrape_analyst_opinions first."
    
    output = f"Analyst opinions for {ticker.upper()}:\n\n"
    for row in rows:
        source, rating, target, summary, scraped = row
        output += f"**{source}** (scraped {scraped.strftime('%Y-%m-%d')})\n"
        if rating:
            output += f"Rating: {rating}\n"
        if target:
            output += f"Price Target: ${target:.2f}\n"
        if summary:
            output += f"Summary: {summary[:300]}...\n"
        output += "\n"
    
    return output


@tool()
def compare_thesis_to_consensus(ticker: str) -> str:
    """
    Compare the user's investment thesis to Wall Street analyst consensus.
    
    This is the "Analyst Critique" feature - it retrieves:
    1. The user's saved thesis (bull/bear case)
    2. Wall Street analyst opinions
    And presents them side-by-side for debate.
    
    Args:
        ticker: Stock ticker symbol
    
    Returns:
        Side-by-side comparison of user thesis vs analyst consensus
    """
    # Get user's thesis
    thesis_query = text("""
        SELECT thesis_type, content, price_at_creation, target_price, created_at
        FROM investment_theses
        WHERE ticker = :ticker
        ORDER BY created_at DESC
        LIMIT 1
    """)
    
    # Get analyst opinions
    analyst_query = text("""
        SELECT source, rating, price_target, summary, scraped_at
        FROM analyst_opinions
        WHERE ticker = :ticker
        ORDER BY scraped_at DESC
        LIMIT 3
    """)
    
    with get_engine().connect() as conn:
        thesis_result = conn.execute(thesis_query, {"ticker": ticker.upper()})
        thesis_row = thesis_result.fetchone()
        
        analyst_result = conn.execute(analyst_query, {"ticker": ticker.upper()})
        analyst_rows = analyst_result.fetchall()
    
    output = f"# Thesis vs Consensus: {ticker.upper()}\n\n"
    
    # User's thesis
    output += "## Your Investment Thesis\n\n"
    if thesis_row:
        thesis_type, content, price_at, target, created = thesis_row
        output += f"**{thesis_type.upper()}** (created {created.strftime('%Y-%m-%d')})\n"
        output += f"- Entry price: ${price_at:.2f}\n" if price_at else ""
        output += f"- Your target: ${target:.2f}\n" if target else ""
        output += f"- Reasoning: {content}\n\n"
    else:
        output += "No thesis saved. Use save_thesis to record your investment view.\n\n"
    
    # Wall Street consensus
    output += "## Wall Street Consensus\n\n"
    if analyst_rows:
        for row in analyst_rows:
            source, rating, target, summary, scraped = row
            output += f"**{source}**\n"
            if rating:
                output += f"- Rating: {rating}\n"
            if target:
                output += f"- Price Target: ${target:.2f}\n"
            if summary:
                output += f"- View: {summary[:200]}...\n"
            output += "\n"
    else:
        output += "No analyst opinions saved. Use scrape_analyst_opinions to fetch Wall Street views.\n\n"
    
    # Comparison prompt
    if thesis_row and analyst_rows:
        output += "## Key Questions to Consider\n\n"
        output += "- Where does your thesis differ from consensus?\n"
        output += "- What does Wall Street see that you might be missing?\n"
        output += "- What do YOU see that analysts might be overlooking?\n"
    
    return output
