**README.txt**

# Search Engine Project

## Overview
This project implements a simple search engine using an inverted index, tokenization, stemming, and TF-IDF ranking. The system allows users to index documents and perform search queries efficiently.

## Requirements
Before running the code, ensure you have the necessary dependencies installed. You can install them using:
```
pip install nltk
```

## How to Create the Index
1. Prepare a directory with text files containing the documents to be indexed.
2. Run the indexer script:
   ```
   python indexer.py <directory_path>
   ```
   This will process the documents and generate `inverted_index.json`.

## How to Start the Search Interface
1. Ensure that `inverted_index.json` has been created.
2. Run the search script:
   ```
   python search.py
   ```
   This will launch an interactive prompt where you can enter queries.

## How to Perform a Simple Query
1. After starting `search.py`, enter a query term or phrase.
2. The system will tokenize, stem, and search for relevant documents based on the indexed data.
3. The results will be displayed in order of relevance.

## Notes
- The search engine uses NLTK for tokenization and stemming.
- Ensure all text files used for indexing are in UTF-8 format.
- The `config.py` file can be modified to adjust parameters like stopword removal or ranking functions.

