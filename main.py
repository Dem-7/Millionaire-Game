import tkinter as tk
from tkinter import messagebox
from game_logic import GameLogic
import json
import random

class MillionaireGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Кто хочет стать миллионером?")
        self.root.geometry("1000x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        # Загрузка вопросов
        with open("questions.json", "r", encoding="utf-8") as f:
            questions_data = json.load(f)
        self.game = GameLogic(questions_data)

        self.setup_main_menu()

    def setup_main_menu(self):
        self.clear_window()
        tk.Label(self.root, text="Кто хочет стать миллионером?", font=("Arial", 24), bg="#f0f0f0").pack(pady=50)
        tk.Button(self.root, text="Играть", width=20, command=self.start_game).pack(pady=10)
        tk.Button(self.root, text="Выход", width=20, command=self.root.quit).pack(pady=10)

    def start_game(self):
        self.clear_window()

        # Разделение на две части: шкала и игровое поле
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Шкала выигрышей
        self.score_frame = tk.Frame(main_frame, bg="black", width=200)
        self.score_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.score_labels = []
        scores = ["1 000 000", "500 000", "250 000", "125 000", "64 000", "32 000", "16 000",
                  "8 000", "4 000", "2 000", "1 000", "500", "300", "200", "100"]

        for i, score in enumerate(scores):
            lbl = tk.Label(self.score_frame, text=f"{score} $", fg="white", bg="black",
                           font=("Arial", 12), anchor="e", padx=10, pady=5)
            lbl.pack()
            self.score_labels.append(lbl)

        # Игровое поле
        game_frame = tk.Frame(main_frame, bg="#f0f0f0")
        game_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)

        self.question_label = tk.Label(game_frame, text="", wraplength=600, justify="center",
                                       font=("Arial", 16), bg="#f0f0f0")
        self.question_label.pack(pady=20)

        self.answers_frame = tk.Frame(game_frame, bg="#f0f0f0")
        self.answers_frame.pack(pady=10)

        self.answer_buttons = []
        for i in range(4):
            btn = tk.Button(self.answers_frame, text="", width=30, height=2,
                            command=lambda idx=i: self.select_answer(idx))
            btn.grid(row=i // 2, column=i % 2, padx=10, pady=10)
            self.answer_buttons.append(btn)

        self.lifelines_frame = tk.Frame(game_frame, bg="#f0f0f0")
        self.lifelines_frame.pack(pady=10)

        self.fifty_fifty_btn = tk.Button(self.lifelines_frame, text="50/50", width=12,
                                         command=self.use_50_50)
        self.fifty_fifty_btn.grid(row=0, column=0, padx=5)

        self.call_friend_btn = tk.Button(self.lifelines_frame, text="Звонок другу", width=12,
                                         command=self.use_call_friend)
        self.call_friend_btn.grid(row=0, column=1, padx=5)

        self.audience_help_btn = tk.Button(self.lifelines_frame, text="Помощь зала", width=12,
                                           command=self.use_audience_help)
        self.audience_help_btn.grid(row=0, column=2, padx=5)

        # Текст с несгораемыми суммами
        self.safe_levels_text = "Несгораемые суммы: $1 000, $32 000"
        self.safe_level_label = tk.Label(game_frame, text=self.safe_levels_text,
                                         font=("Arial", 14), fg="green", bg="#f0f0f0")
        self.safe_level_label.pack(pady=10)

        self.update_question()

    def update_question(self):
        question = self.game.get_current_question()
        if not question:
            self.show_win_screen()
            return

        self.question_label.config(text=f"Вопрос {self.game.current_question_index + 1}: {question.text}")

        answers = question.answers
        for i, btn in enumerate(self.answer_buttons):
            btn.config(text=answers[i], state=tk.NORMAL, bg="SystemButtonFace")

        self.highlight_current_score()

    def highlight_current_score(self):
        scores_order = [14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        index = scores_order[self.game.current_question_index]

        for i, label in enumerate(self.score_labels):
            if i == index:
                label.config(bg="green", fg="white")
            elif len(self.score_labels) - i - 1 in self.game.safe_levels:
                label.config(bg="yellow", fg="black")
            else:
                label.config(bg="black", fg="white")

    def select_answer(self, index):
        selected_answer = self.answer_buttons[index].cget("text")
        is_correct = self.game.check_answer(selected_answer)

        for btn in self.answer_buttons:
            btn.config(state=tk.DISABLED)

        if is_correct:
            if self.game.is_final_question():
                self.show_win_screen()
            else:
                self.show_next_button()
        else:
            self.show_lose_screen()

    def show_next_button(self):
        next_btn = tk.Button(self.root, text="Следующий вопрос", width=20, command=self.next_question)
        next_btn.place(relx=0.5, rely=0.9, anchor="center")

    def next_question(self):
        self.game.next_question()
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button) and widget.cget("text") == "Следующий вопрос":
                widget.destroy()
        self.update_question()

    def show_win_screen(self):
        self.clear_window()
        tk.Label(self.root, text="🎉 Поздравляем! Вы стали миллионером!", font=("Arial", 20),
                 fg="green", bg="#f0f0f0").pack(pady=50)
        tk.Button(self.root, text="Играть снова", width=20, command=self.setup_main_menu).pack(pady=10)
        tk.Button(self.root, text="Выход", width=20, command=self.root.quit).pack(pady=10)

    def show_lose_screen(self):
        safe_score = self.game.get_safe_score()
        self.clear_window()
        tk.Label(self.root, text=f"❌ Неправильный ответ!\nВы получаете: ${safe_score}", font=("Arial", 20),
                 fg="red", bg="#f0f0f0").pack(pady=50)
        tk.Button(self.root, text="Играть снова", width=20, command=self.setup_main_menu).pack(pady=10)
        tk.Button(self.root, text="Выход", width=20, command=self.root.quit).pack(pady=10)

    def use_50_50(self):
        if not self.game.use_lifeline("50_50"):
            return

        correct_answer = self.game.get_current_question().correct_answer
        answer_texts = [btn.cget("text") for btn in self.answer_buttons]

        incorrect_answers = [a for a in answer_texts if a != correct_answer]
        to_remove = random.sample(incorrect_answers, 2)

        for btn in self.answer_buttons:
            text = btn.cget("text")
            if text in to_remove:
                btn.config(text="", state=tk.DISABLED)
        self.fifty_fifty_btn.config(state=tk.DISABLED)

    def use_call_friend(self):
        if not self.game.use_lifeline("call_friend"):
            return

        answer_texts = [btn.cget("text") for btn in self.answer_buttons]
        correct = self.game.get_current_question().correct_answer

        if random.random() < 0.8:
            suggestion = correct
        else:
            suggestion = random.choice([a for a in answer_texts if a != correct])

        messagebox.showinfo("Звонок другу", f"Друг думает, что правильный ответ: {suggestion}")
        self.call_friend_btn.config(state=tk.DISABLED)

    def use_audience_help(self):
        if not self.game.use_lifeline("audience_help"):
            return

        answer_texts = [btn.cget("text") for btn in self.answer_buttons]
        correct = self.game.get_current_question().correct_answer
        percentages = {}

        for ans in answer_texts:
            if ans == correct:
                percentages[ans] = random.randint(50, 80)
            else:
                percentages[ans] = random.randint(5, 20)

        help_text = "\n".join([f"{a}: {p}%" for a, p in percentages.items()])
        messagebox.showinfo("Помощь зала", f"Голосование зала:\n{help_text}")
        self.audience_help_btn.config(state=tk.DISABLED)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = MillionaireGame(root)
    root.mainloop()