import random

class Question:
    def __init__(self, text, answers, correct_answer):
        self.text = text
        self.answers = answers
        self.correct_answer = correct_answer


class GameLogic:
    def __init__(self, questions_data):
        self.questions = [
            Question(q["text"], q["answers"], q["answers"][q["correct_index"]])
            for q in questions_data
        ]
        self.current_question_index = 0
        self.scores = [100, 200, 300, 500, 1000, 2000, 4000, 8000, 16000, 32000,
                       64000, 125000, 250000, 500000, 1000000]
        self.safe_levels = [4, 9]  # индексы вопросов: 5 и 10
        self.lifelines_available = {
            '50_50': True,
            'call_friend': True,
            'audience_help': True
        }

    def get_current_question(self):
        if self.current_question_index < len(self.questions):
            return self.questions[self.current_question_index]
        return None

    def check_answer(self, selected_answer):
        correct = self.questions[self.current_question_index].correct_answer
        return selected_answer == correct

    def next_question(self):
        self.current_question_index += 1

    def is_final_question(self):
        return self.current_question_index == len(self.questions) - 1

    def use_lifeline(self, lifeline_type):
        if self.lifelines_available[lifeline_type]:
            self.lifelines_available[lifeline_type] = False
            return True
        return False

    def get_safe_score(self):
        last_safe_idx = -1
        for level in self.safe_levels:
            if self.current_question_index > level:
                last_safe_idx = level
        if last_safe_idx == -1:
            return 0
        return self.scores[last_safe_idx]