import json
import numpy as np
from utils import process_query, load_index

def search(query, index):
    """Search for a query in the inverted index and return ranked results."""
    query_terms = process_query(query)
    scores = {}

    for term in query_terms:
        if term in index:
            for doc_id, weight in index[term].items():
                if doc_id not in scores:
                    scores[doc_id] = 0
                scores[doc_id] += weight

    # Rank results
    ranked_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranked_results

if __name__ == "__main__":
    index = load_index()
    while True:
        query = input("\nEnter search query (or type 'exit' to quit): ")
        if query.lower() == "exit":
            break
        results = search(query, index)
        if results:
            print("\nTop search results:")
            for doc_id, score in results[:5]:
                print(f"Document {doc_id}: Score {score:.4f}")
        else:
            print("No relevant documents found.")
