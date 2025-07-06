import re
import json
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

word_normalizer = PorterStemmer()


def load_lexicon(lexicon_file="lexicon_data.json"):
    """Loads the lexicon from a JSON file."""
    with open(lexicon_file, "r", encoding="utf-8") as file:
        return json.load(file)


def process_user_query(user_input):
    """ Tokenizes, normalizes, and returns a list of processed query terms. """
    tokens = word_tokenize(user_input.lower())
    return [word_normalizer.stem(token) for token in tokens if re.match(r'^[a-zA-Z0-9]+$', token)] 