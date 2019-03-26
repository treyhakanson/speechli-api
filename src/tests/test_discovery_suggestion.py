from routes.discovery import Suggestion

def test_init_and_serialize():
	document_id = 'test_document_id'
	text = 'test text'
	score = 1
	author = 'test author'
	suggestion = Suggestion(document_id, text, score, author)
	suggestion_dict = suggestion.to_dict()

	assert(document_id == suggestion_dict['document_id'])
	assert(text == suggestion_dict['text'])
	assert(author == suggestion_dict['author'])
	assert(score == suggestion_dict['score'])
	assert('Neutral' == suggestion_dict['tone'])

def test_from_passage_and_serialize():
	passage = {
		'document_id': 'test_document_id',
		'passage_text': 'First line.\nSecond line',
		'passage_score': 1
	}
	author = 'test author'
	suggestion = Suggestion.from_passage(passage, author)
	suggestion_dict = suggestion.to_dict()

	assert(passage['document_id'] == suggestion_dict['document_id'])
	assert('First line. Second line' == suggestion_dict['text'])
	assert(author == suggestion_dict['author'])
	assert(passage['passage_score'] == suggestion_dict['score'])
	assert('Neutral' == suggestion_dict['tone'])

def test_trim_to_contain():
	passage = {
		'document_id': 'test_document_id',
		'passage_text': 'First line.\nSecond line',
		'passage_score': 1
	}
	author = 'test author'
	suggestion = Suggestion.from_passage(passage, author)
	suggestion.trim_to_contain('First')

	assert('First line' == suggestion.to_dict()['text'])