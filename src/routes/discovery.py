"""Routes that make calls to the discovery engine API."""
import random
from flask import Blueprint, Response, request, jsonify
from discovery import DISCOVERY_ENV, get_discovery_client
from exceptions import ClientException
from tone_analyzer import analyze_tone

discovery_bp = Blueprint("discovery_bp", __name__)

MAX_PASSAGES = 5


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

    def analyze_tone(self):
        self._tone = analyze_tone(self._text)

    def to_dict(self):
        """Serialize the suggestion to a dictionary."""
        return {
            "document_id": self._document_id,
            "text": self._text,
            "score": self._score,
            "author": self._author,
            "tone": getattr(self, '_tone', 'Neutral')
        }


def _build_suggestions(
    sentence,
    results,
    passages,
    authors,
    with_tones=True
):
    """Build suggestions based on the a sentence and discovery query."""
    words = sentence.split(" ")
    suggestions = []
    for i, passage in enumerate(passages):
        author = authors[i]
        suggestion = Suggestion.from_passage(passage, author=author)
        suggestion.trim_to_contain(words)
        if with_tones:
            suggestion.analyze_tone()
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
    authors = data.get("authors", [])
    doctype = data.get("type", None)
    docfilter = ""
    if not sentence:
        raise ClientException("\"sentence\" not provided.")
    if doctype:
        docfilter += f'type::"{doctype}"'
    if authors:
        if docfilter:
            docfilter += ','
        author_str = ','.join([f'"{author}"' for author in authors])
        docfilter += f'author::{author_str}'
    query_res = client.query(
        DISCOVERY_ENV["ENV_ID"],
        DISCOVERY_ENV["COLLECTION_ID"],
        natural_language_query=sentence,
        passages_count=MAX_PASSAGES,
        return_fields=["passages"],
        filter=docfilter or None
    )
    passages = query_res.result["passages"]
    results = query_res.result["results"]
    authors = []
    tones = []
    for passage in passages:
        docid = passage["document_id"]
        doc_res = client.query(
            DISCOVERY_ENV["ENV_ID"],
            DISCOVERY_ENV["COLLECTION_ID"],
            return_fields=["author"],
            filter=f'id::"{docid}"'
        )
        authors.append(doc_res.result["results"][0].get("author", None))
    suggestions = _build_suggestions(
        sentence,
        results,
        passages,
        authors,
        with_tones=True
    )
    return jsonify(suggestions)

@discovery_bp.route("/discovery/authors/", methods=["GET"])
def discovery_authors():
    """Return authors in the discovery collection."""
    with open('./authors.txt') as f:
        authors = f.read().split('\n')
    return jsonify(authors)

@discovery_bp.route("/discovery/moonshot/", methods=["POST"])
def discovery_moonshot():
    """Moonshots a give document."""
    client = get_discovery_client()
    data = request.get_json()
    sentences = data.get("sentences", None)
    authors = data.get("authors", [])
    if not sentences:
        raise ClientException("\"sentence\" not provided.")
    if not authors:
        raise ClientException("\"authors\" not provided.")
    author_str = ','.join([f'"{author}"' for author in authors])
    docfilter = f'author::{author_str}'
    sentence_mapping = {}
    for sentence in sentences:
        query_res = client.query(
            DISCOVERY_ENV["ENV_ID"],
            DISCOVERY_ENV["COLLECTION_ID"],
            natural_language_query=sentence,
            passages_count=MAX_PASSAGES,
            return_fields=["passages"],
            filter=docfilter
        )
        passages = query_res.result["passages"]
        results = query_res.result["results"]
        suggestions = _build_suggestions(
            sentence,
            results,
            passages,
            [None] * len(passages)
        )
        if suggestions:
            suggestion = max(suggestions, key=lambda x: x['score'])
            if random.random() >= 0.5:
                sentence_mapping[sentence] = suggestion['text']
    return jsonify(sentence_mapping)
