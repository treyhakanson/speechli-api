
import json
import os
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from constants import KEYWORDS_ANALYZER_VERSION, KEYWORDS_IAM_URL
from watson_developer_cloud.natural_language_understanding_v1 import Features, KeywordsOptions


KEYWORDS_ANALYZER_ENV = {
    "API_KEY": os.environ.get("IAM_API_KEY_KEYWORDS", None)
}



natural_language_understanding = NaturalLanguageUnderstandingV1(
    version= KEYWORDS_ANALYZER_VERSION,
    iam_apikey= KEYWORDS_ANALYZER_ENV["API_KEY"],
    url= KEYWORDS_IAM_URL
)


def keywords(txt):
    response = natural_language_understanding.analyze(
    text = txt,
    features = Features(keywords=KeywordsOptions(limit = 5))).get_result()
    keywords = []
    for key, val in response.items():
        if (key == 'keywords'):
            for item in val:
                item.pop('count', None)
                keywords.append(item)
    return keywords

