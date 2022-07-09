from data import question_data
from question_model import Question

question_bank = []
for item in question_data:
    question_bank.append(Question(item["text"], item["answer"]))
