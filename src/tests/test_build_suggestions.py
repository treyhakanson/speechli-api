from pathlib import Path
import sys
path = str(Path().absolute().parent)
sys.path.insert(0, path)
from routes.discovery import _build_suggestions
  
def test_build_suggestions1():
    
    sentence = "Change will not come if we wait for some other person, or if we wait for some other time."
    passages = ["Change will not come if we wait for some other person, or if we wait for some other time.", ""]
    results = []
    document_id = 1
    score = 2
    text = ""
    author = ""
    #print (from_passage(sentence, results), "Working")
    #assert len(Suggestion(document_id, score, text, author).from_passage(sentence, results)) == 0         
    
def test_build_suggestions2():
    
    sentence = "Change will not come if we wait for some other person, or if we wait for some other time."
    passages = []
    results = []
    assert len(_build_suggestions(sentence, results, passages)) == 0 
