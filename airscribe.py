import time

"""
input: input file, patient_id
ouput: make output file
"""
def analyze(block_of_text):
	# hard code patient_id heh
	patient_id = 12345

	# random notes: can only ask each question once, must ask exactly word for word
	question_db = get_question_db()
	spoken_questions = get_spoken_questions(question_db)

	sentences = breakdown(block_of_text)
	qanda = get_qanda(sentences, spoken_questions)

	doc_text = ""
	doc_text += generate_document_header(patient_id)
	doc_text +=  "\n=== Information ===\n"
	standard_text, standard_dict = generate_standard(qanda, question_db)
	doc_text += standard_text
	doc_text += "\n=== Feedback for Patient ===\n"
	doc_text += generate_feedback(standard_dict)
	doc_text += "\n=== Full Interview Q&A ===\n"
	doc_text += generate_dialogue(qanda)
	doc_text += "\n\nGenerated by Airscribe"

	date = "160214"
	date = time.strftime("%y%m%d")
	print_to_document(doc_text, "pid{0}_discharge_{1}.txt".format(patient_id, date))

	# alternatively, return block of text
	return doc_text

"""
input: text file
output: list of sentences
"""
def breakdown(block_of_text):
	# note IBM watson has periods but no other punctuation
	sentences = block_of_text.strip().split(".")
	processed = []
	for s in sentences:
		s = s.strip()
		if len(s) > 0:
			processed.append(s)
	return processed

"""
input: list of sentences
output: dictionary of responses
"""
def get_qanda(sentences, spoken_questions):
	qanda = {}
	curr_question = None
	response = "" # usually an answer
	for sentence in sentences:
		# new question
		isQuestion = False
		for spq in spoken_questions:
			if edit_distance(sentence.lower(), spq) == 0: 
				isQuestion = True
				# deal with prev question
				if curr_question:
					qanda[curr_question] = response
				curr_question = spq[0].upper() + spq[1:]
				response = ""
		# sentence is not a question
		if not isQuestion:
			response += sentence + ". "
	# last question
	if curr_question:
		qanda[curr_question] = response
	return qanda

"""
input: dictionary of responses
output: standard, formatted interview info
"""
def generate_standard(qanda, question_db):
	# if we want the questions in a certain order, iterate through question_db in order
	text = ""
	standard = {}
	spoken_questions = get_spoken_questions(question_db)
	for question in qanda:
		# get the index from list of spoken_words
		qid = spoken_questions.index(question.lower())
		standard_form = question_db[qid]['standard_form']
		answer = qanda[question]
		answer = standardize_answer(answer, question_db[qid]['answers'])
		text += "{0}:\t{1}\n".format(standard_form, answer)
		standard[standard_form] = answer # or qid?
	return text, standard

"""
input: verbose answer, list of standard answers
output: one of the standard answers, or special custom answer
currently VERY simple; could use more thoughtful algorithm...
"""
def standardize_answer(answer, answer_choices):
	# if a key word (answer choice) is anywhere in their answer, capitalize and return it
	# otherwise just return the answer? or a special message?

	# also need to consider equivalent words like "yes" = "yeah"
	for choice in answer_choices:
		if choice.lower() in answer.lower():
			return choice.title()
	return answer

"""
input: dictionary of responses
output: summary of feedback
"""
def generate_feedback(standard):
	return "Feature not yet available!\n"

"""
input: dictionary of responses
ouput: dialogue format
"""
def generate_dialogue(qanda):
	text = ""
	for question in qanda:
		text += "Q: {}?\n".format(question)
		text += "A: {}\n".format(qanda[question])
	return text

"""
input: patient_id
output: patient details???
===
PATIENT ID:
PATIENT NAME:
"""
def generate_document_header(patient_id):
	patient_name = "Parkinson, Pansy"
	date = time.strftime("%b %d, %Y")
	interviewer_name = "Zhu, Eugenie"
	text = "Hospital Discharge Interview\nPATIENT ID: {0}\nPATIENT NAME: {1}\n".format(patient_id, patient_name) 
	text += "DATE: {0}\nINTERVIEWER: {1}\n".format(date, interviewer_name)
	return text

"""
input: dictionary of responses, optional summary?
output: print formatted text file
"""
def print_to_document(text, filename):
	with open(filename, 'w') as f:
		f.write(text)
	with open(filename, 'w') as f:
		f.write(text)

def get_question_db():
	# kinda sketch representation of Question struct
	# Question = {'qid' = int, spoken_form' = "how are you", 'standard_form'="Feelings", 'answers'=["good", "bad"]}
	question_db = []
	question_db.append({
		'qid' : 0,
		'spoken_form' : "how are you", 
		'standard_form' : "Feelings", 
		'answers' : ["good", "bad"]})
	question_db.append({
		'qid' : 1,
		'spoken_form' : "where do you live", 
		'standard_form' : "Hometown", 
		'answers' : ["fremont", "san jose", "san francisco", "houston"]})
	question_db.append({
		'qid' : 2,
		'spoken_form' : "do you live by yourself", 
		'standard_form' : "Lives alone", 
		'answers' : ["yes", "no"]})

	#print question_db
	return question_db

def get_spoken_questions(question_db):
	# just a list of all spoken form questions
	spoken_questions = []
	for question in question_db:
		spoken_questions.append(question['spoken_form'])
	return spoken_questions

def edit_distance(s1, s2):
    m=len(s1)+1
    n=len(s2)+1

    tbl = {}
    for i in range(m): tbl[i,0]=i
    for j in range(n): tbl[0,j]=j
    for i in range(1, m):
        for j in range(1, n):
            cost = 0 if s1[i-1] == s2[j-1] else 1
            tbl[i,j] = min(tbl[i, j-1]+1, tbl[i-1, j]+1, tbl[i-1, j-1]+cost)

    return tbl[i,j]

# for testing; comment out if needed
if __name__ == "__main__":
	# sample workflow
	patient_id = 12345
	with open("input.txt", 'r') as f:
		block_of_text = f.readlines()[0]
	analyze(block_of_text)

