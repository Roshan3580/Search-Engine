# Web Content Analysis and Retrieval System

## About This Project

I developed this Web Content Analysis and Retrieval System as a personal project to explore advanced text processing techniques and information retrieval algorithms. The system demonstrates how modern search engines work under the hood, combining multiple ranking algorithms to provide relevant results.

## Why I Built This

I've always been fascinated by how search engines like Google can find relevant information from billions of web pages in milliseconds. This project was my way of understanding and implementing the core concepts behind information retrieval systems. I wanted to create something that could:

- Process and analyze web content efficiently
- Implement sophisticated ranking algorithms
- Handle large datasets with optimized data structures
- Provide fast and accurate search results

## How It Works

### 1. Content Processing (`web_crawler_engine.py`)
The system starts by processing JSON files containing web content. For each document, it:
- Extracts text content from HTML using BeautifulSoup
- Performs text normalization and tokenization
- Applies Porter stemming to reduce words to their root form
- Builds an inverted index (lexicon) for fast term lookup
- Creates a link graph for authority scoring
- Removes duplicate content using SHA-256 hashing

### 2. Query Processing (`query_processor.py`)
When you enter a search query, the system:
- Tokenizes and normalizes your query terms
- Finds documents containing all query terms (Boolean AND search)
- Calculates relevance scores using TF-IDF algorithm
- Integrates authority scores using PageRank algorithm
- Ranks results by combined relevance and authority
- Returns top 5 most relevant results with URLs

### 3. Ranking Algorithms
The system uses two main ranking approaches:
- **TF-IDF (Term Frequency-Inverse Document Frequency)**: Measures how important a term is in a document relative to the entire collection
- **Authority Scoring (PageRank)**: Considers the link structure between documents to determine their importance

## Key Features

- **Efficient Indexing**: Uses inverted index data structure for O(1) term lookup
- **Duplicate Detection**: Automatically identifies and skips duplicate content
- **Link Analysis**: Extracts and analyzes hyperlinks between documents
- **Fast Retrieval**: Optimized algorithms for quick search results
- **Scalable Architecture**: Modular design allows for easy extensions

## Technical Implementation

The system is built using Python with these key libraries:
- **NLTK**: For advanced text processing and tokenization
- **BeautifulSoup**: For HTML parsing and content extraction
- **Collections**: For efficient data structures
- **JSON**: For data serialization and storage

## What I Learned

Building this system taught me:
- How search engines process and index content
- The importance of efficient data structures in information retrieval
- How ranking algorithms work together to provide relevant results
- The challenges of handling large-scale text processing
- Best practices for building modular, maintainable code

## Future Enhancements

Some ideas I have for improving the system:
- Add support for phrase queries and wildcard searches
- Implement query expansion using synonyms
- Add support for different file formats (PDF, DOCX)
- Create a web interface for easier interaction
- Add user feedback mechanisms for result relevance

This project represents my journey into understanding information retrieval systems and demonstrates the power of combining multiple algorithms to solve complex problems in text analysis and search. 