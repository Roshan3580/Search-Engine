import json
import math
from utils import load_index, process_query

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

    return sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)


def search():
    """ Runs the search engine and displays results with URLs. """
    test_queries = [
        "Iftekhar Ahmed",
        "machine learning",
        "ACM",
        "master of software engineering"
    ]

    for query in test_queries:
        print(f"\nQuery: {query}")

        query_terms = process_query(query)
        relevant_docs = boolean_and_search(query_terms)

        if not relevant_docs:
            print("No results found.")
            continue

        ranked_results = compute_tf_idf(query_terms, relevant_docs)

        print("Top 5 results:")
        for i, (doc, score) in enumerate(ranked_results[:5]):
            url = doc_metadata.get(doc, "URL not found")
            print(f"{i + 1}. URL: {url} | Score: {score:.4f}")


if __name__ == "__main__":
    search()
