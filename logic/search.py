from backend.repository import search_items

def find_items(keyword):
    results = search_items(keyword)
    if not results:
        return [f"No items found for '{keyword}'."]
    return [f"{i.id}: {i.title} ({i.category}) - {i.quantity} available" for i in results]
