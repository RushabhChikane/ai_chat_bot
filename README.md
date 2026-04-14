# AI Shopping Assistant

An AI-powered e-commerce chatbot that lets users browse products, search using natural language, and place orders through conversation.

## Features

- **Product Catalog** — Browse 20 products across 5 categories with filters
- **AI Chatbot** — Search products, check stock, and place orders via natural conversation
- **Semantic Search** — Uses vector embeddings so "something for music" finds headphones and speakers
- **Order Management** — Place orders through chat with confirmation, real-time stock updates
- **Order History** — View all past orders with details

## Tech Stack

| Technology | Purpose |
|---|---|
| Streamlit | Frontend UI |
| LangChain | AI agent with tool calling |
| Groq (Llama 3.3) | LLM for natural language understanding |
| ChromaDB | Vector database for semantic search |
| sentence-transformers | Text to vector embeddings |
| SQLite | Product and order database |

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file with your Groq API key (free at console.groq.com)
cp .env.example .env
# Edit .env and add your key

# Run the app
streamlit run run.py
```

## Project Structure

```
├── config.py                  # Settings and paths
├── run.py                     # App entry point
│
├── db/                        # Data layer
│   ├── database.py            # SQLite connection and tables
│   ├── models.py              # Product and Order dataclasses
│   └── seed_data.py           # Sample product data
│
├── services/                  # Business logic
│   ├── product_service.py     # Product queries
│   └── order_service.py       # Order placement and stock management
│
├── ai/                        # AI layer
│   ├── embeddings.py          # ChromaDB vector search
│   └── chat_engine.py         # LangChain agent with tools
│
└── ui/                        # Frontend pages
    ├── products_page.py       # Product catalog
    ├── chat_page.py           # AI chat interface
    └── orders_page.py         # Order history
```

## How It Works

1. **Product data** is stored in SQLite and embedded as vectors in ChromaDB using sentence-transformers
2. When a user chats, the **LangChain agent** decides which tool to call (search, check order, confirm order, order status)
3. **Semantic search** matches user queries to products by meaning, not just keywords
4. Orders go through a **preview → confirm** flow — the bot shows details and asks for confirmation before placing

## Chat Examples

- `Show me phones under 70000`
- `What books do you have?`
- `Buy 2 iPhone 15` → shows preview → `yes` → places order
- `What's the status of order #1?`
