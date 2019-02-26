"""Routes that make calls to the tone analyzer engine API."""
from flask import Blueprint, Response, request, jsonify
from tone_analyzer import TONE_ANALYZER_ENV, get_tone_analyzer_client
from exceptions import ClientException

tone_analyzer_bp = Blueprint("tone_analyzer_bp", __name__)

@tone_analyzer_bp.route("/tone/", methods=["POST"])
def analyze():
    client = get_tone_analyzer_client()
    data = request.get_json()
    sentence = data.get("sentence", None)
    if not sentence:
        raise ClientException("\"sentence\" not provided.")
    tone_analysis = client.tone(
    {'text': sentence},
    'application/json'
    ).get_result()
    return jsonify(tone_analysis)
