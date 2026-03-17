import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine, text
from src.agents.team import get_analyst_team

st.set_page_config(
    page_title="Interactive Equity Analyst",
    page_icon="📊",
    layout="wide",
)

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = f"streamlit-{os.urandom(4).hex()}"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "team" not in st.session_state:
    st.session_state.team = get_analyst_team(session_id=st.session_state.session_id)


def get_theses():
    """Fetch all investment theses from database."""
    engine = create_engine(os.getenv("DATABASE_URL"))
    query = text("""
        SELECT ticker, thesis_type, content, price_at_creation, target_price, created_at
        FROM investment_theses
        ORDER BY created_at DESC
        LIMIT 10
    """)
    with engine.connect() as conn:
        result = conn.execute(query)
        return result.fetchall()


def stream_response(query: str):
    """Stream response from the agent team."""
    team = st.session_state.team
    
    response_stream = team.run(query, stream=True)
    
    previous_content = ""
    for chunk in response_stream:
        if hasattr(chunk, 'content') and chunk.content:
            # Yield only the new content (delta)
            new_content = chunk.content
            if new_content.startswith(previous_content):
                delta = new_content[len(previous_content):]
                if delta:
                    yield delta
            else:
                yield new_content
            previous_content = new_content


# Sidebar
with st.sidebar:
    st.title("📊 Equity Analyst")
    st.markdown("---")
    
    # My Theses Section
    st.subheader("📝 My Theses")
    
    try:
        theses = get_theses()
        if theses:
            for thesis in theses:
                ticker, thesis_type, content, price_at, target, created = thesis
                icon = "🐂" if thesis_type == "bull" else "🐻"
                with st.expander(f"{icon} {ticker} - ${target:.0f}" if target else f"{icon} {ticker}"):
                    st.write(f"**Type:** {thesis_type.upper()}")
                    if price_at:
                        st.write(f"**Entry:** ${price_at:.2f}")
                    if target:
                        st.write(f"**Target:** ${target:.2f}")
                    st.write(f"**Thesis:** {content[:100]}...")
                    st.caption(f"Saved: {created.strftime('%Y-%m-%d')}")
        else:
            st.info("No theses saved yet. Start by telling the analyst your investment view!")
    except Exception as e:
        st.warning("Could not load theses")
    
    st.markdown("---")
    
    # Quick Actions
    st.subheader("⚡ Quick Actions")
    
    col1, col2 = st.columns(2)
    
    ticker_input = st.text_input("Ticker", placeholder="NVDA", key="ticker_input")
    
    if col1.button("📈 Analyze", use_container_width=True):
        if ticker_input:
            st.session_state.quick_action = f"Give me a complete analysis of {ticker_input} - fundamentals and recent news"
    
    if col2.button("⚖️ Compare", use_container_width=True):
        if ticker_input:
            st.session_state.quick_action = f"Compare my {ticker_input} thesis to Wall Street consensus"
    
    if st.button("🔄 Get Analyst Ratings", use_container_width=True):
        if ticker_input:
            st.session_state.quick_action = f"Get analyst ratings for {ticker_input}"
    
    st.markdown("---")
    
    # Guidelines Section
    with st.expander("📖 How to Use", expanded=False):
        st.markdown("""
        **Save a Thesis**
        > "I'm bullish on NVDA with a $200 target because of AI demand"
        
        **Get Analysis**
        > "Analyze AAPL fundamentals and recent news"
        
        **Challenge Consensus**
        > "Compare my NVDA thesis to Wall Street"
        
        **Research Transcripts**
        > "Find MSFT earnings transcripts"
        """)
    
    with st.expander("💡 Best Practices", expanded=False):
        st.markdown("""
        1. **Be specific** - Include ticker symbols and price targets
        
        2. **State your view** - Bull or bear, with reasoning
        
        3. **Ask for comparisons** - Challenge your thesis against analyst consensus
        
        4. **Use transcripts** - Search and ingest earnings calls for deeper research
        
        5. **Iterate** - Ask follow-up questions to refine your analysis
        """)
    
    st.markdown("---")
    st.caption(f"Session: {st.session_state.session_id[:12]}...")


# Main chat area
st.title("💬 Interactive Equity Analyst")
st.markdown("Ask me about stocks, save your investment thesis, or challenge Wall Street consensus.")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle quick action buttons
if "quick_action" in st.session_state and st.session_state.quick_action:
    prompt = st.session_state.quick_action
    st.session_state.quick_action = None
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Stream assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.write_stream(stream_response(prompt))
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    st.rerun()

# Chat input
if prompt := st.chat_input("Ask the analyst..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Stream assistant response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            try:
                response = st.write_stream(stream_response(prompt))
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
