import streamlit as st
from services.product_service import get_all_products, get_categories

EMOJI = {"electronics": "💻", "clothing": "👕", "books": "📚", "home": "🏠", "accessories": "🎧"}


def render():
    st.title("🏪 Product Catalog")
    st.markdown("---")

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        categories = ["All"] + get_categories()
        selected = st.selectbox("Category", categories)
    with col2:
        max_price = st.number_input("Max Price (Rs.)", min_value=0, value=0, step=1000)

    # Fetch & filter
    category = selected if selected != "All" else None
    products = get_all_products(category=category)
    if max_price > 0:
        products = [p for p in products if p["price"] <= max_price]

    st.markdown(f"**{len(products)} products**")

    # Product grid
    for i in range(0, len(products), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(products):
                p = products[i + j]
                emoji = EMOJI.get(p["category"], "📦")
                stock_color = "green" if p["stock"] > 0 else "red"
                stock_text = f"In Stock ({p['stock']})" if p["stock"] > 0 else "Out of Stock"
                with col:
                    st.markdown(f"""
                    <div style="border:1px solid #ddd; border-radius:10px; padding:15px; margin-bottom:10px; height:250px;">
                        <h3>{emoji} {p['name']}</h3>
                        <p style="font-size:22px; font-weight:bold; color:#1a73e8;">Rs.{p['price']:,.0f}</p>
                        <p>⭐ {p['rating']}/5 &nbsp;|&nbsp; <span style="color:{stock_color};">{stock_text}</span></p>
                        <p style="color:#666; font-size:13px;">{p['description'][:80]}...</p>
                        <p style="color:#888; font-size:12px;">ID: {p['id']} | {p['category'].title()}</p>
                    </div>
                    """, unsafe_allow_html=True)
