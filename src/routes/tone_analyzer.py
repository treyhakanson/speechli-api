"""Routes that make calls to the tone analyzer engine API."""
from flask import Blueprint, Response, request, jsonify
from tone_analyzer import TONE_ANALYZER_ENV, analyze_tone
from exceptions import ClientException

tone_analyzer_bp = Blueprint("tone_analyzer_bp", __name__)

@tone_analyzer_bp.route("/tone/", methods=["POST"])
def analyze():
    data = request.get_json()
    sentence = data.get("sentence", None)
    if not sentence:
        raise ClientException("\"sentence\" not provided.")
    tones = analyze_tone(sentence)
    return jsonify({"tones": tones})
