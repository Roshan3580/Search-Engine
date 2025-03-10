import os
import json
import re
import collections
from bs4 import BeautifulSoup
import warnings
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from collections import defaultdict, Counter
import nltk
import ssl
import hashlib

warnings.filterwarnings("ignore")

ssl._create_default_https_context = ssl._create_unverified_context

nltk.download('punkt_tab')

document_hashes = {}

stemmer = PorterStemmer()
inverted_index = defaultdict(lambda: defaultdict(int))
document_metadata = {}
documents = {}
link_graph = defaultdict(set)
bigram_index = defaultdict(lambda: defaultdict(int))
trigram_index = defaultdict(lambda: defaultdict(int))
positional_index = defaultdict(lambda: defaultdict(list))
anchor_index = defaultdict(lambda: defaultdict(int))


def compute_hash(text):
    """Computes SHA-256 hash for deduplication."""
    return hashlib.sha256(text.encode()).hexdigest()


def extract_text_and_metadata(json_content, filename):
    """Extracts text, metadata, and links from a document."""
    text = ""
    url = json_content.get("url", "UNKNOWN")

    if "content" in json_content:
        soup = BeautifulSoup(json_content["content"], "html.parser")

        important_text = " ".join([tag.get_text() for tag in soup.find_all(["title", "h1", "h2", "h3", "b", "strong"])])
        body_text = soup.get_text()

        text += important_text + " " + body_text
        extract_links(soup, filename)

    doc_hash = compute_hash(text)
    if doc_hash in document_hashes:
        return None

    document_hashes[doc_hash] = filename
    document_metadata[filename] = url

    return text.strip()


def extract_links(soup, filename):
    """Extracts links and updates link graph."""
    for link in soup.find_all("a", href=True):
        link_graph[filename].add(link["href"])


def generate_ngrams(tokens, n):
    return [" ".join(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]

if __name__ == "__main__":
    dataset_dir = input("Enter the dataset directory: ").strip()

    if not os.path.exists(dataset_dir):
        print(f"Directory '{dataset_dir}' does not exist.")
        exit(1)

    for root, _, files in os.walk(dataset_dir):
        for filename in files:
            if filename.endswith(".json"):
                file_path = os.path.join(root, filename)

                with open(file_path, "r", encoding="utf-8") as file:
                    json_content = json.load(file)
                    text = extract_text_and_metadata(json_content, filename)

                    if text is None:
                        continue

                    tokens = word_tokenize(text.lower())
                    filtered_tokens = [stemmer.stem(token) for token in tokens if re.match(r"^[a-zA-Z0-9]+$", token)]

                    term_frequencies = collections.Counter(filtered_tokens)

                    documents[filename] = len(filtered_tokens)
                    for term, freq in term_frequencies.items():
                        inverted_index[term][filename] = freq

                    bigrams = generate_ngrams(filtered_tokens, 2)
                    trigrams = generate_ngrams(filtered_tokens, 3)

                    for ngram in bigrams:
                        bigram_index[ngram][filename] += 1
                    for ngram in trigrams:
                        trigram_index[ngram][filename] += 1

                    for i, token in enumerate(filtered_tokens):
                        inverted_index[token][filename] += 1
                        positional_index[token][filename].append(i)

    with open("inverted_index.json", "w", encoding="utf-8") as index_file:
        json.dump({"index": inverted_index, "documents": documents}, index_file, indent=4)

    with open("doc_metadata.json", "w", encoding="utf-8") as meta_file:
        json.dump(document_metadata, meta_file, indent=4)

    print("\nSummary Report:")
    print(f"Indexed {len(documents)} documents.")
    print(f"Total unique tokens: {len(inverted_index)}")
    print(f"Index size: {os.path.getsize('inverted_index.json') / 1024:.2f} KB")
