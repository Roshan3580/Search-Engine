# web_crawler_engine.py

import os
import json
import re
import collections
from bs4 import BeautifulSoup
import warnings
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from collections import defaultdict
import nltk
import ssl
import hashlib

# Suppress warnings
warnings.filterwarnings("ignore")
ssl._create_default_https_context = ssl._create_unverified_context
nltk.download('punkt')

content_fingerprints = {}  # Stores hash -> filename

# Get dataset directory
data_source_path = input("Enter the dataset directory: ").strip()
output_lexicon_file = "lexicon_data.json"
content_info_file = "content_metadata.json"

# Initialize structures
word_normalizer = PorterStemmer()
lexicon_structure = defaultdict(lambda: defaultdict(int))  # term -> {doc_id -> term_freq}
content_info = {}  # Maps filenames to their URLs
total_documents = 0
document_lengths = {}
hyperlink_network = defaultdict(set)

def generate_content_hash(text_content):
    """Generates SHA-256 hash for content deduplication."""
    return hashlib.sha256(text_content.encode()).hexdigest()

# Function to extract text and metadata from JSON
def parse_content_and_info(json_data, filename):
    extracted_text = ""
    page_url = json_data.get("url", "UNKNOWN")

    # Parse HTML content from 'content' key
    if "content" in json_data:
        html_parser = BeautifulSoup(json_data["content"], "html.parser")

        # Extract important text
        priority_text = " ".join([tag.get_text() for tag in html_parser.find_all(["title", "h1", "h2", "h3", "b", "strong"])])
        main_content = html_parser.get_text()
        extracted_text += priority_text + " " + main_content
        collect_hyperlinks(html_parser, filename)

    content_hash = generate_content_hash(extracted_text)
    if content_hash in content_fingerprints:
        print(f"Duplicate content detected: {filename} matches {content_fingerprints[content_hash]}")
        return None  # Skip indexing duplicate

    content_fingerprints[content_hash] = filename
    content_info[filename] = page_url  # Store the URL
    return extracted_text.strip()

def collect_hyperlinks(html_parser, filename):
    """Collects hyperlinks and updates link network."""
    for link in html_parser.find_all("a", href=True):
        hyperlink_network[filename].add(link["href"])

# Convert defaultdict to dict
def transform_defaultdict_to_dict(data_structure):
    return {k: transform_defaultdict_to_dict(v) for k, v in data_structure.items()} if isinstance(data_structure, defaultdict) else data_structure

def create_lexicon():
    """Function to process dataset and create lexicon."""
    global total_documents, lexicon_structure, document_lengths, hyperlink_network

    # Check if dataset directory exists
    if not os.path.exists(data_source_path):
        print(f"Directory '{data_source_path}' does not exist.")
        exit(1)

    # Process JSON files
    for root, _, files in os.walk(data_source_path):
        for filename in files:
            if filename.endswith(".json"):
                file_path = os.path.join(root, filename)
                with open(file_path, "r", encoding="utf-8") as file:
                    json_data = json.load(file)
                    extracted_text = parse_content_and_info(json_data, filename)

                    if extracted_text is None:
                        continue  # Skip duplicates

                    total_documents += 1

                    # Tokenization & Stemming
                    word_tokens = word_tokenize(extracted_text.lower())
                    processed_tokens = [word_normalizer.stem(token) for token in word_tokens if re.match(r"^[a-zA-Z0-9]+$", token)]

                    # Compute term frequencies
                    term_frequencies = collections.Counter(processed_tokens)

                    # Store document details
                    document_lengths[filename] = len(processed_tokens)
                    for term, freq in term_frequencies.items():
                        lexicon_structure[term][filename] = freq

    # Save lexicon and metadata
    with open(output_lexicon_file, "w", encoding="utf-8") as lexicon_file:
        json.dump(
            {"lexicon": transform_defaultdict_to_dict(lexicon_structure), "documents": document_lengths, "total_docs": total_documents},
            lexicon_file, indent=4)

    with open(content_info_file, "w", encoding="utf-8") as meta_file:
        json.dump(content_info, meta_file, indent=4)

    print("\nProcessing Summary:")
    print(f"Processed {total_documents} documents.")
    print(f"Total unique terms: {len(lexicon_structure)}")
    print(f"Lexicon size: {os.path.getsize(output_lexicon_file) / 1024:.2f} KB")


if __name__ == "__main__":
    create_lexicon() 