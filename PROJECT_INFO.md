**PROJECT_INFO.md**

# Web Content Analysis and Retrieval System

## Overview
This project implements a sophisticated web content analysis and retrieval system using advanced text processing, lexical analysis, and authority-based ranking algorithms. The system enables efficient indexing of web documents and provides intelligent content discovery capabilities.

## Prerequisites
Before running the system, ensure you have the necessary dependencies installed:
```
pip install nltk beautifulsoup4
```

## How to Build the Lexicon
1. Prepare a directory containing JSON files with web content data.
2. Execute the web crawler engine:
   ```
   python web_crawler_engine.py
   ```
   This will process the documents and generate `lexicon_data.json`.

## How to Launch the Query Interface
1. Ensure that `lexicon_data.json` has been created.
2. Run the query processor:
   ```
   python query_processor.py
   ```
   This will launch an interactive interface where you can enter content queries.
   The system will prompt you for the directory path to confirm the data source,
   enter the same directory path that you used for the web crawler engine.

## How to Perform Content Queries
1. After launching the query processor, enter your search terms or phrases.
2. The system will process, normalize, and search for relevant content based on the indexed data.
3. Results will be displayed in order of relevance with authority scores.

## Technical Notes
- The system uses NLTK for advanced text processing and normalization.
- All text files used for indexing should be in UTF-8 format.
- The `settings.py` file can be modified to adjust system parameters like authority calculation or result display limits. 