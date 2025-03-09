import re
import json
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()


def load_index(index_file="inverted_index.json"):
    """Loads the inverted index from a JSON file."""
    with open(index_file, "r", encoding="utf-8") as file:
        return json.load(file)


def process_query(query):
    """ Tokenizes, stems, and returns a list of processed query terms. """
    tokens = word_tokenize(query.lower())
    return [stemmer.stem(token) for token in tokens if re.match(r'^[a-zA-Z0-9]+$', token)]
