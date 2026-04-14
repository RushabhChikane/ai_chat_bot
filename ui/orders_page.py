import streamlit as st
from services.order_service import get_all_orders


def render():
    st.title("📦 Order History")
    st.markdown("---")

    orders = get_all_orders()

    if not orders:
        st.info("No orders yet. Use the AI Assistant to place your first order!")
        return

    st.markdown(f"**Total Orders: {len(orders)}**")

    for order in orders:
        emoji = {"confirmed": "✅", "shipped": "🚚", "delivered": "📬"}.get(order["status"], "📋")

        with st.expander(f"{emoji} Order #{order['id']} — {order['product_name']} — Rs.{order['total_price']:,.0f}"):
            c1, c2, c3 = st.columns(3)
            c1.metric("Product", order["product_name"])
            c2.metric("Quantity", order["quantity"])
            c3.metric("Total", f"Rs.{order['total_price']:,.0f}")
            st.markdown(f"**Status:** {order['status'].title()} &nbsp;|&nbsp; **Date:** {order['created_at']}")
