import os
from typing import Optional
from agno.tools import tool
from sqlalchemy import create_engine, text

# Create engine at module level
_engine = None
def get_engine():
      global _engine
      if _engine is None:
          _engine = create_engine(os.getenv("DATABASE_URL"))
      return _engine

@tool()
def save_thesis(ticker: str, thesis_type: str, content: str, price_at_creation: Optional[float] = None, target_price: Optional[float] = None) -> str:
    """
      Save an investment thesis for a stock ticker.
      
      Args:
          ticker: Stock symbol (e.g., AAPL, TSLA, NVDA)
          thesis_type: Either 'bull' or 'bear'
          content: The investment thesis reasoning
          price_at_creation: Current stock price when creating thesis
          target_price: Optional price target
      
      Returns:
          Confirmation message with thesis ID
      """
    
    query = text("""
          INSERT INTO investment_theses (ticker, thesis_type, content, price_at_creation, target_price)
          VALUES (:ticker, :thesis_type, :content, :price_at_creation, :target_price)
          RETURNING id
      """)
    
    with get_engine().connect() as conn:
        result = conn.execute(query, {
            "ticker": ticker,
            "thesis_type": thesis_type,
            "content": content,
            "price_at_creation": price_at_creation,
            "target_price": target_price
        })
        conn.commit()
        thesis_id = result.fetchone()[0]
    
    return f"Thesis saved for {ticker.upper()} with ID: {thesis_id}"

@tool()
def get_theses(ticker: str) -> str:
    """
      Retrieve all investment theses for a stock ticker.
      
      Args:
          ticker: Stock symbol to look up (e.g., AAPL, TSLA, NVDA)
      
      Returns:
          Formatted list of all theses for the ticker
      """
    query = text("""
          SELECT thesis_type, content, price_at_creation, target_price, created_at
          FROM investment_theses
          WHERE ticker = :ticker
          ORDER BY created_at DESC
      """)
    
    with get_engine().connect() as conn:
        result = conn.execute(query, {"ticker": ticker.upper()})
        rows = result.fetchall()
    
    if not rows:
        return f"No investment theses found for {ticker.upper()}"

    output = f"Investment theses for {ticker.upper()}:\n\n"

    for row in rows:
          thesis_type, content, price, target, created = row
          output += f"**{thesis_type.upper()}** (saved {created.strftime('%Y-%m-%d')})\n"
          if price:
              output += f"Price at creation: ${price:.2f}\n"
          if target:
              output += f"Target price: ${target:.2f}\n"
          output += f"Thesis: {content}\n\n"
      
    return output
