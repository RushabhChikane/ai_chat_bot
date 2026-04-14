import chromadb
from sentence_transformers import SentenceTransformer
from config import CHROMA_DB_PATH, EMBEDDING_MODEL
from db.database import get_db

model = SentenceTransformer(EMBEDDING_MODEL)
client = chromadb.PersistentClient(path=CHROMA_DB_PATH)


def get_collection():
    """Get or create the product embeddings collection."""
    return client.get_or_create_collection(name="products", metadata={"hnsw:space": "cosine"})


def embed_products():
    """Convert all product text into vectors and store in ChromaDB."""
    conn = get_db()
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()

    collection = get_collection()
    if collection.count() == len(products):
        return  # Already embedded

    docs, metas, ids = [], [], []
    for p in products:
        p = dict(p)
        docs.append(f"{p['name']} - {p['category']} - {p['description']}")
        metas.append({
            "product_id": p["id"], "name": p["name"],
            "category": p["category"], "price": p["price"],
            "stock": p["stock"], "rating": p["rating"],
        })
        ids.append(str(p["id"]))

    embeddings = model.encode(docs).tolist()
    collection.upsert(documents=docs, embeddings=embeddings, metadatas=metas, ids=ids)


def search_products(query, n_results=5):
    """Semantic search: find products matching a natural language query."""
    collection = get_collection()
    query_embedding = model.encode(query).tolist()
    return collection.query(query_embeddings=[query_embedding], n_results=n_results)


def refresh_embedding(product_id):
    """Re-embed a single product after stock changes."""
    conn = get_db()
    p = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    conn.close()
    if not p:
        return
    p = dict(p)
    doc = f"{p['name']} - {p['category']} - {p['description']}"
    embedding = model.encode(doc).tolist()
    get_collection().upsert(
        documents=[doc], embeddings=[embedding],
        metadatas=[{"product_id": p["id"], "name": p["name"], "category": p["category"],
                    "price": p["price"], "stock": p["stock"], "rating": p["rating"]}],
        ids=[str(p["id"])],
    )
