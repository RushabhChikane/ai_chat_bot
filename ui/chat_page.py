import streamlit as st
from ai.chat_engine import chat


def render():
    st.title("🤖 AI Shopping Assistant")
    st.markdown("Ask me to search products, check stock, or place orders!")
    st.markdown("---")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("e.g. 'Show me laptops under 50000'"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat(prompt, st.session_state.messages[:-1])
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

    # Suggestions in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Try asking:")
    for s in ["Show me phones under 70000", "What books do you have?",
              "Buy 2 iPhone 15", "What's the status of order #1?"]:
        st.sidebar.markdown(f"- *{s}*")
