import streamlit as st
from db.database import init_db
from db.seed_data import seed_products
from ai.embeddings import embed_products
from ui import products_page, chat_page, orders_page

# ── Page Config ─────────────────────────────────────────────
st.set_page_config(page_title="AI Shopping Assistant", page_icon="🛒", layout="wide")

# ── Initialize on first run ─────────────────────────────────
if "db_ready" not in st.session_state:
    with st.spinner("Setting up..."):
        init_db()
        seed_products()
        embed_products()
    st.session_state.db_ready = True

# ── Navigation ──────────────────────────────────────────────
st.sidebar.title("🛒 ShopAI")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigate", ["🏪 Products", "🤖 AI Assistant", "📦 Orders"], label_visibility="collapsed")

# ── Route to page ───────────────────────────────────────────
if page == "🏪 Products":
    products_page.render()
elif page == "🤖 AI Assistant":
    chat_page.render()
elif page == "📦 Orders":
    orders_page.render()

# ── Footer ──────────────────────────────────────────────────
st.sidebar.markdown("---")
st.sidebar.markdown(
    "<p style='color:#888; font-size:11px;'>Built with Streamlit, LangChain, Groq, ChromaDB</p>",
    unsafe_allow_html=True,
)
