import os
import json
import math
import time
from data_helpers import load_lexicon, process_user_query
from web_crawler_engine import hyperlink_network

lexicon_file = "lexicon_data.json"
metadata_file = "content_metadata.json"
if not os.path.exists(lexicon_file) or not os.path.exists(metadata_file):
    print("Lexicon and metadata files not found. Please run the web crawler engine first.")
    exit(1)

start_time = time.time()
lexicon_data = load_lexicon()
term_index = lexicon_data["lexicon"]
document_lengths = lexicon_data["documents"]
total_docs = lexicon_data["total_docs"]
print(f"Data loading took {time.time() - start_time:.4f} seconds")

start_time = time.time()
with open(metadata_file, "r", encoding="utf-8") as meta_file:
    content_metadata = json.load(meta_file)
print(f"Metadata loading took {time.time() - start_time:.4f} seconds")

def calculate_authority_scores(damping_factor=0.85, max_iterations=100):
    """Calculates authority scores using power iteration."""
    N = len(hyperlink_network)
    authority_scores = {doc: 1 / N for doc in hyperlink_network}

    for _ in range(max_iterations):
        new_authority_scores = {}
        for doc in hyperlink_network:
            new_authority_scores[doc] = (1 - damping_factor) / N + damping_factor * sum(
                authority_scores[incoming] / len(hyperlink_network[incoming]) for incoming in hyperlink_network if
                doc in hyperlink_network[incoming]
            )
        authority_scores = new_authority_scores
    return authority_scores

def find_matching_documents(query_terms):
    """ Returns document IDs that contain all query terms. """
    if not query_terms:
        return set()
    document_sets = [set(term_index.get(term, {}).keys()) for term in query_terms]
    result = set.intersection(*document_sets) if document_sets else set()
    return result

def calculate_relevance_scores(query_terms, matching_docs, authority_scores):
    """ Calculates relevance scores and integrates authority scores. """
    document_scores = {}
    for term in query_terms:
        if term in term_index:
            document_frequency = len(term_index[term])
            inverse_doc_freq = math.log((total_docs / (document_frequency + 1)))
            for doc in matching_docs:
                term_freq = term_index[term].get(doc, 0) / document_lengths[doc]
                document_scores[doc] = document_scores.get(doc, 0) + (term_freq * inverse_doc_freq)
    for doc in document_scores:
        document_scores[doc] *= authority_scores.get(doc, 1)
    return sorted(document_scores.items(), key=lambda x: x[1], reverse=True)

def run_query_interface():
    """ Runs the query interface with user input and displays results with URLs. """
    authority_scores = calculate_authority_scores()
    while True:
        user_query = input("Enter your search query (or type 'quit' to exit): ").strip()
        if user_query.lower() == 'quit':
            print("Exiting query processor.")
            break
        start_time = time.time()
        processed_terms = process_user_query(user_query)
        matching_docs = find_matching_documents(processed_terms)
        if not matching_docs:
            print("No matching documents found.")
            continue
        ranked_results = calculate_relevance_scores(processed_terms, matching_docs, authority_scores)
        print("\nTop 5 results:")
        for i, (doc, score) in enumerate(ranked_results[:5]):
            url = content_metadata.get(doc, "URL not found")
            print(f"{i + 1}. URL: {url} | Relevance: {score:.4f}")
        print(f"Total query processing time: {time.time() - start_time:.4f} seconds")

if __name__ == "__main__":
    run_query_interface() 