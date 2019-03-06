"""Routes that make calls to the discovery engine API."""
from pathlib import Path
import sys
path = str(Path().absolute().parent)
sys.path.insert(0, path)


from flask import Blueprint, Response, request, jsonify
from discovery import DISCOVERY_ENV, get_discovery_client
from exceptions import ClientException


discovery_bp = Blueprint("discovery_bp", __name__)


MAX_PASSAGES = 10


class Suggestion:
    """Discovery suggestion helper class."""

    @staticmethod
    def from_passage(passage, author=None):
        """Create a suggestion from a discovery query passage."""
        return Suggestion(
            passage["document_id"],
            " ".join(passage["passage_text"].splitlines()),
            passage["passage_score"],
            author
        )

    def __init__(self, document_id, text, score, author):
        """Constructor."""
        self._document_id = document_id
        self._text = text
        self._score = score
        self._author = author

    def trim_to_contain(self, should_contain):
        """
        Trim suggestion text.

        Trims suggestion text to be the sentence containing the
        most matches to words in the should contain list.
        """
        parts = self._text.split(".")
        max_matches = float("-inf")
        sentence = None
        for part in parts:
            num_matches = sum([substr in part for substr in should_contain])
            if num_matches > max_matches:
                max_matches = num_matches
                sentence = part
        self._text = sentence
        return self

    def to_dict(self):
        """Serialize the suggestion to a dictionary."""
        return {
            "document_id": self._document_id,
            "text": self._text,
            "score": self._score,
            "author": self._author
        }


def _build_suggestions(sentence, results, passages):
    """Build suggestions based on the a sentence and discovery query."""
    words = sentence.split(" ")
    suggestions = []
    for passage in passages:
        author = next((result.get("author", None) for result in results if result["id"] == passage["document_id"]), None)
        suggestion = Suggestion.from_passage(passage, author=author)
        suggestion.trim_to_contain(words)
        suggestions.append(suggestion.to_dict())
    return suggestions


@discovery_bp.route("/discovery/environments/", methods=["GET"])
def discovery_environments():
    """Return discovery engine environments."""
    client = get_discovery_client()
    environments = client.list_environments()
    return Response(environments, mimetype='application/json')


@discovery_bp.route("/discovery/suggest/", methods=["POST"])
def discovery_suggest():
    """Return suggestions for a given sentence."""
    client = get_discovery_client()
    data = request.get_json()
    sentence = data.get("sentence", None)
    if not sentence:
        raise ClientException("\"sentence\" not provided.")
    query_res = client.query(
        DISCOVERY_ENV["ENV_ID"],
        DISCOVERY_ENV["COLLECTION_ID"],
        natural_language_query=sentence,
        passages_count=MAX_PASSAGES,
        return_fields=["passages"]
    )
    passages = query_res.result["passages"]
    results = query_res.result["results"]
    suggestions = _build_suggestions(sentence, results, passages)
    return jsonify(suggestions)

@discovery_bp.route("/discovery/authors/", methods=["GET"])
def discovery_authors():
    """Return authors in the discovery collection."""
    with open('./authors.txt') as f:
        authors = f.read().split('\n')
    return jsonify(authors)
