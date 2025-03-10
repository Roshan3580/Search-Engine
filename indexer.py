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

# Suppress warnings
warnings.filterwarnings("ignore")

ssl._create_default_https_context = ssl._create_unverified_context

nltk.download('punkt_tab')

# Get dataset directory
dataset_dir = input("Enter the dataset directory: ").strip()
output_index_file = "inverted_index.json"
metadata_file = "doc_metadata.json"

# Initialize structures
stemmer = PorterStemmer()
inverted_index = defaultdict(lambda: defaultdict(int))  # term -> {doc_id -> term_freq}
document_metadata = {}  # Maps filenames to their URLs
document_count = 0
documents = {}

# Function to extract text and metadata from JSON
def extract_text_and_metadata(json_content, filename):
    text = ""
    url = json_content.get("url", "UNKNOWN")

    # Parse HTML content from 'content' key
    if "content" in json_content:
        soup = BeautifulSoup(json_content["content"], "html.parser")

        # Extract important text
        important_text = " ".join([tag.get_text() for tag in soup.find_all(["title", "h1", "h2", "h3", "b", "strong"])])
        body_text = soup.get_text()

        text += important_text + " " + body_text

    document_metadata[filename] = url  # Store the URL
    return text.strip()

# Convert defaultdict to dict
def convert_defaultdict_to_dict(d):
    return {k: convert_defaultdict_to_dict(v) for k, v in d.items()} if isinstance(d, defaultdict) else d

# Check if dataset directory exists
if not os.path.exists(dataset_dir):
    print(f"Directory '{dataset_dir}' does not exist.")
    exit(1)

# Process JSON files
for root, _, files in os.walk(dataset_dir):
    for filename in files:
        if filename.endswith(".json"):
            document_count += 1
            file_path = os.path.join(root, filename)

            with open(file_path, "r", encoding="utf-8") as file:
                json_content = json.load(file)
                text = extract_text_and_metadata(json_content, filename)

                # Tokenization & Stemming
                tokens = word_tokenize(text.lower())
                filtered_tokens = [stemmer.stem(token) for token in tokens if re.match(r"^[a-zA-Z0-9]+$", token)]

                # Compute term frequencies
                term_frequencies = collections.Counter(filtered_tokens)

                # Store document details
                documents[filename] = len(filtered_tokens)
                for term, freq in term_frequencies.items():
                    inverted_index[term][filename] = freq

# Save index and metadata
with open(output_index_file, "w", encoding="utf-8") as index_file:
    json.dump(
        {"index": convert_defaultdict_to_dict(inverted_index), "documents": documents, "doc_count": document_count},
        index_file, indent=4)

with open(metadata_file, "w", encoding="utf-8") as meta_file:
    json.dump(document_metadata, meta_file, indent=4)

print("\nSummary Report:")
print(f"Indexed {document_count} documents.")
print(f"Total unique tokens: {len(inverted_index)}")
print(f"Index size: {os.path.getsize(output_index_file) / 1024:.2f} KB")
