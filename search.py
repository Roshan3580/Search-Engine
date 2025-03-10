import json
import math
import time  # Import time module for runtime tracking
from utils import load_index, process_query
import numpy as np
import indexer

def compute_pagerank(damping=0.85, max_iter=100):
    """Computes PageRank using power iteration."""
    N = len(indexer.link_graph)
    pagerank = {doc: 1 / N for doc in indexer.link_graph}

    for _ in range(max_iter):
        new_pagerank = {}
        for doc in indexer.link_graph:
            new_pagerank[doc] = (1 - damping) / N + damping * sum(
                pagerank[incoming] / len(indexer.link_graph[incoming]) for incoming in indexer.link_graph if doc in indexer.link_graph[incoming]
            )
        pagerank = new_pagerank
    return pagerank


# Load data
data = load_index()
inverted_index = data["index"]
documents = data["documents"]
document_count = data["doc_count"]

# Load document metadata (filenames to URLs)
with open("doc_metadata.json", "r", encoding="utf-8") as meta_file:
    doc_metadata = json.load(meta_file)


def boolean_and_search(query_terms):
    """ Returns document IDs that contain all query terms. """
    if not query_terms:
        return set()

    postings = [set(inverted_index.get(term, {}).keys()) for term in query_terms]
    return set.intersection(*postings) if postings else set()

def compute_tf_idf(query_terms, relevant_docs):
    """ Computes TF-IDF scores and ranks documents. """
    doc_scores = {}

    for term in query_terms:
        if term in inverted_index:
            df = len(inverted_index[term])
            idf = math.log((document_count / (df + 1)))

            for doc in relevant_docs:
                tf = inverted_index[term].get(doc, 0) / documents[doc]
                doc_scores[doc] = doc_scores.get(doc, 0) + (tf * idf)

    # Apply PageRank adjustment
    pagerank_scores = compute_pagerank()
    for doc in doc_scores:
        doc_scores[doc] *= pagerank_scores.get(doc, 1)

    return sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)


def search():
    """ Runs the search engine with user input and displays results with URLs. """
    while True:
        query = input("Enter your search query (or type 'exit' to quit): ").strip()
        if query.lower() == 'exit':
            print("Exiting search engine.")
            break

        # Start measuring time for query processing
        start_time = time.time()

        # Tokenization and preprocessing
        query_terms = process_query(query)
        print(f"Query preprocessing (tokenization, etc.) took {time.time() - start_time:.4f} seconds")

        # Perform boolean AND search
        start_time = time.time()
        relevant_docs = boolean_and_search(query_terms)
        print(f"Boolean AND search took {time.time() - start_time:.4f} seconds")

        if not relevant_docs:
            print("No results found.")
            continue

        # Compute TF-IDF scores
        start_time = time.time()
        ranked_results = compute_tf_idf(query_terms, relevant_docs)
        print(f"TF-IDF computation and ranking took {time.time() - start_time:.4f} seconds")

        print("Top 5 results:")
        for i, (doc, score) in enumerate(ranked_results[:5]):
            url = doc_metadata.get(doc, "URL not found")
            print(f"{i + 1}. URL: {url} | Score: {score:.4f}")

        # Total time for the entire query processing
        print(f"Total query processing time: {time.time() - start_time:.4f} seconds")


def search_ngrams(query_terms):
    """Search using n-grams."""
    bigram_matches = {doc for term in query_terms for doc in indexer.bigram_index.get(term, {})}
    trigram_matches = {doc for term in query_terms for doc in indexer.trigram_index.get(term, {})}
    query = ["data science"]
    matches = search_ngrams(query)
    return bigram_matches | trigram_matches

def search_with_positions(query_terms):
    """Find documents where terms appear close together."""
    candidate_docs = set(indexer.positional_index.get(query_terms[0], {}).keys())

    for term in query_terms[1:]:
        candidate_docs &= set(indexer.positional_index.get(term, {}).keys())

    ranked_docs = []
    for doc in candidate_docs:
        positions = [indexer.positional_index[term][doc] for term in query_terms]
        min_distance = min(abs(a - b) for a, b in zip(*positions))
        ranked_docs.append((doc, 1 / (1 + min_distance)))

    return sorted(ranked_docs, key=lambda x: x[1], reverse=True)

if __name__ == "__main__":
    search()
