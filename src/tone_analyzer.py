import os
from constants import TONE_ANALYZER_VERSION, TONE_IAM_URL
from watson_developer_cloud import ToneAnalyzerV3

TONE_ANALYZER_ENV = {
    "API_KEY": os.environ.get("IAM_API_KEY_TONE", None)
}

def get_tone_analyzer_client():
    """Get a IBM tone analyzer engine client."""
    tone_analyzer = ToneAnalyzerV3(
        version= TONE_ANALYZER_VERSION,
        iam_apikey= TONE_ANALYZER_ENV["API_KEY"],
        url= TONE_IAM_URL
    )
    return tone_analyzer


def analyze_tone(text):
    client = get_tone_analyzer_client()
    tone_analysis = client.tone(
        {
            "text": text
        },
        "application/json"
    ).get_result()
    print(tone_analysis)
    tone = ', '.join([tone['tone_name'] for tone in tone_analysis['document_tone']['tones']] or ['Neutral'])
    return tone
