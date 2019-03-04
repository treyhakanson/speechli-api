def test_sum():
    assert 1 + 2 == 3
    #assert sum([1, 1, 1]) == 6, "Should be 6"
    
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


def test_build_suggestions():
    
    sentence = "Change will not come if we wait for some other person, or if we wait for some other time."
    passages = []
    results = []
    #print (_build_suggestions(sentence, results, passages), "Working")
    assert len(_build_suggestions(sentence, results, passages)) == 0         
    
