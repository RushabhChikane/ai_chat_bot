from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from config import GROQ_API_KEY, GROQ_MODEL
from db.database import get_db
from services.product_service import get_product_by_name
from services.order_service import place_order, get_order_by_id
from ai.embeddings import search_products, refresh_embedding


# ── Tools ───────────────────────────────────────────────────

@tool
def search_products_tool(query: str) -> str:
    """Search for products by name, category, or description.
    Use this when the user wants to find or browse products.
    """
    results = search_products(query, n_results=5)
    if not results["ids"][0]:
        return "No products found."

    conn = get_db()
    output = "Found products:\n\n"
    for i in range(len(results["ids"][0])):
        meta = results["metadatas"][0][i]
        live = conn.execute("SELECT stock, price FROM products WHERE id = ?", (meta["product_id"],)).fetchone()
        stock = live["stock"] if live else meta["stock"]
        price = live["price"] if live else meta["price"]
        status = f"In Stock ({stock})" if stock > 0 else "OUT OF STOCK"
        output += (f"{i+1}. {meta['name']} (ID: {meta['product_id']})\n"
                   f"   Rs.{price:,.0f} | Rating: {meta['rating']}/5 | {status}\n\n")
    conn.close()
    return output


@tool
def check_order_tool(product_name: str, quantity: str) -> str:
    """Preview an order BEFORE placing it. Always call this first when user wants to buy.
    This does NOT place the order.
    """
    qty = int(quantity)
    product = get_product_by_name(product_name)
    if not product:
        return f"Product '{product_name}' not found. Search for products first."
    if product["stock"] <= 0:
        return f"{product['name']} is OUT OF STOCK."
    if product["stock"] < qty:
        return (f"Not enough stock for {product['name']}. "
                f"Requested: {qty}, Available: {product['stock']}. "
                f"Ask the user if they want {product['stock']} instead. Do NOT auto-order.")
    total = product["price"] * qty
    return (f"ORDER PREVIEW:\n"
            f"  Product: {product['name']}\n"
            f"  Quantity: {qty}\n"
            f"  Price: Rs.{product['price']:,.0f} each\n"
            f"  Total: Rs.{total:,.0f}\n"
            f"  Stock: {product['stock']} available\n"
            f"Show these details and ask: 'Shall I confirm this order?'")


@tool
def confirm_order_tool(product_name: str, quantity: str) -> str:
    """Place the order. ONLY call after user confirms with yes/ok/confirm."""
    qty = int(quantity)
    result = place_order(product_name, qty)
    if "error" in result:
        return f"Order failed: {result['error']}"
    product = get_product_by_name(product_name)
    if product:
        refresh_embedding(product["id"])
    return (f"ORDER CONFIRMED:\n"
            f"  Order ID: #{result['order_id']}\n"
            f"  Product: {result['product_name']}\n"
            f"  Quantity: {result['quantity']}\n"
            f"  Total: Rs.{result['total_price']:,.0f}\n"
            f"  Stock remaining: {result['stock_remaining']}")


@tool
def get_order_status_tool(order_id: str) -> str:
    """Check status of an order by its ID number."""
    clean_id = "".join(c for c in str(order_id) if c.isdigit())
    order = get_order_by_id(int(clean_id))
    if not order:
        return f"No order found with ID #{clean_id}."
    return (f"Order #{order['id']}:\n"
            f"  Product: {order['product_name']}\n"
            f"  Quantity: {order['quantity']}\n"
            f"  Total: Rs.{order['total_price']:,.0f}\n"
            f"  Status: {order['status']}\n"
            f"  Date: {order['created_at']}")


# ── Agent ───────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a shopping assistant for an online store.

ORDER RULES:
1. When user wants to buy, call check_order_tool FIRST to preview.
2. Show the preview details and ask user to confirm.
3. Only call confirm_order_tool AFTER user says yes/ok/confirm.
4. If stock is insufficient, tell the user. NEVER auto-order a different quantity.
5. Report the exact Order ID from the tool response.

OTHER RULES:
6. Search products before recommending. Don't make up info.
7. Show product IDs in results. Prices in Rs.
8. Be concise.
"""

TOOLS = [search_products_tool, check_order_tool, confirm_order_tool, get_order_status_tool]
TOOL_MAP = {t.name: t for t in TOOLS}

llm = ChatGroq(model=GROQ_MODEL, api_key=GROQ_API_KEY, temperature=0.1)
llm_with_tools = llm.bind_tools(TOOLS)


def chat(message: str, history: list) -> str:
    """Send a message to the AI agent and get a response."""
    # Build message list
    messages = [SystemMessage(content=SYSTEM_PROMPT)]
    for msg in history[-10:]:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))
    messages.append(HumanMessage(content=message))

    try:
        return _run_agent(messages)
    except Exception as e:
        err = str(e)
        # If tool calling fails, retry without tools (plain LLM response)
        if "Failed to call a function" in err or "tool_use_failed" in err:
            try:
                response = llm.invoke(messages)
                return response.content if isinstance(response.content, str) else str(response.content)
            except Exception:
                pass
        if "429" in err or "rate" in err.lower():
            return "Rate limited. Please wait a few seconds and try again."
        if "503" in err or "UNAVAILABLE" in err:
            return "AI model is temporarily busy. Please try again."
        return f"Something went wrong: {err[:150]}"


def _run_agent(messages):
    """Agent loop: LLM decides tool → execute → LLM reads result → repeat."""
    for _ in range(5):
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        if not response.tool_calls:
            content = response.content
            if isinstance(content, list):
                parts = [b["text"] for b in content if isinstance(b, dict) and b.get("type") == "text"]
                return "\n".join(parts) if parts else str(content)
            return content

        for tc in response.tool_calls:
            tool_fn = TOOL_MAP.get(tc["name"])
            result = tool_fn.invoke(tc["args"]) if tool_fn else f"Unknown tool: {tc['name']}"
            messages.append(ToolMessage(content=result, tool_call_id=tc["id"]))

    return "Sorry, I couldn't process that. Please try again."
