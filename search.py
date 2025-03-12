import os
import json
import math
import time
from utils import load_index, process_query
from indexer import link_graph

index_file = "inverted_index.json"
metadata_file = "doc_metadata.json"
if not os.path.exists(index_file) or not os.path.exists(metadata_file):
    print("Index and metadata files not found. Please run the indexer first.")
    exit(1)

start_time = time.time()
data = load_index()
inverted_index = data["index"]
documents = data["documents"]
document_count = data["doc_count"]
print(f"Data loading took {time.time() - start_time:.4f} seconds")

start_time = time.time()
with open(metadata_file, "r", encoding="utf-8") as meta_file:
    doc_metadata = json.load(meta_file)
print(f"Metadata loading took {time.time() - start_time:.4f} seconds")

def compute_pagerank(damping=0.85, max_iter=100):
    """Computes PageRank using power iteration."""
    start_time = time.time()
    N = len(link_graph)
    pagerank = {doc: 1 / N for doc in link_graph}

    for _ in range(max_iter):
        new_pagerank = {}
        for doc in link_graph:
            new_pagerank[doc] = (1 - damping) / N + damping * sum(
                pagerank[incoming] / len(link_graph[incoming]) for incoming in link_graph if
                doc in link_graph[incoming]
            )
        pagerank = new_pagerank

    print(f"PageRank computation took {time.time() - start_time:.4f} seconds")
    return pagerank

def boolean_and_search(query_terms):
    """ Returns document IDs that contain all query terms. """
    if not query_terms:
        return set()
    start_time = time.time()
    postings = [set(inverted_index.get(term, {}).keys()) for term in query_terms]
    result = set.intersection(*postings) if postings else set()
    print(f"Boolean AND search took {time.time() - start_time:.4f} seconds")
    return result

def compute_tf_idf(query_terms, relevant_docs, pagerank_scores):
    """ Computes TF-IDF scores and integrates PageRank. """
    start_time = time.time()
    doc_scores = {}
    for term in query_terms:
        if term in inverted_index:
            df = len(inverted_index[term])
            idf = math.log((document_count / (df + 1)))
            for doc in relevant_docs:
                tf = inverted_index[term].get(doc, 0) / documents[doc]
                doc_scores[doc] = doc_scores.get(doc, 0) + (tf * idf)
    for doc in doc_scores:
        doc_scores[doc] *= pagerank_scores.get(doc, 1)
    print(f"TF-IDF computation took {time.time() - start_time:.4f} seconds")
    return sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)

def search():
    """ Runs the search engine with user input and displays results with URLs. """
    pagerank_scores = compute_pagerank()
    while True:
        query = input("Enter your search query (or type 'exit' to quit): ").strip()
        if query.lower() == 'exit':
            print("Exiting search engine.")
            break
        start_time = time.time()
        query_terms = process_query(query)
        relevant_docs = boolean_and_search(query_terms)
        if not relevant_docs:
            print("No results found.")
            continue
        ranked_results = compute_tf_idf(query_terms, relevant_docs, pagerank_scores)
        print("\nTop 5 results:")
        for i, (doc, score) in enumerate(ranked_results[:5]):
            url = doc_metadata.get(doc, "URL not found")
            print(f"{i + 1}. URL: {url} | Score: {score:.4f}")
        print(f"Total query processing time: {time.time() - start_time:.4f} seconds")

if __name__ == "__main__":
    search()
