import random


class Question:
    def __init__(self, question):
        self.question = question.title
        self.correct_answer = question.correct_answer
        self.answers = question.answers 

    def present_question(self):
        print(f"\n{self.question}")
        print("Muligheder:")
        options = [self.correct_answer] +  [answer for answer in self.answers if answer != self.correct_answer]
        # Shuffle the options to randomize their order
        random.shuffle(options)
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        return options, options.index(self.correct_answer)

    def check_answer(self, user_answer):
        return user_answer == self.correct_answer


# generate AI questions
from AI import generate_ai_questions
questions = generate_ai_questions(10)

for ai_question in questions:
    q = Question(ai_question)
    q.present_question()