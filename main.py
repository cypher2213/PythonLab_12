import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
import random
import os
from datetime import datetime

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Тестування знань")
        self.data = None
        self.current_question = 0
        self.score = 0
        self.questions = []
        self.username = ""
        
        self.build_main_interface()

    # ---------- ГОЛОВНИЙ ІНТЕРФЕЙС ----------
    def build_main_interface(self):
        tk.Label(self.root, text="Ім'я користувача:").pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()

        tk.Button(self.root, text="Завантажити файл з питаннями",
                  command=self.load_file).pack(pady=5)

        tk.Label(self.root, text="Кількість питань:").pack()
        self.q_count = tk.Entry(self.root)
        self.q_count.pack()

        tk.Button(self.root, text="Почати тестування",
                  command=self.start_test).pack(pady=10)

    # ---------- ЗАВАНТАЖЕННЯ ФАЙЛУ ----------
    def load_file(self):
        try:
            filepath = filedialog.askopenfilename(filetypes=[("CSV файли", "*.csv")])
            if not filepath:
                return
            
            df = pd.read_csv(filepath)

            required_cols = ["question", "option1", "option2", "option3", "correct"]
            for col in required_cols:
                if col not in df.columns:
                    raise KeyError(f"Немає стовпця '{col}'")

            df.dropna(inplace=True)
            self.data = df
            messagebox.showinfo("OK", "Файл успішно завантажено!")

        except FileNotFoundError:
            messagebox.showerror("Помилка", "Файл не знайдено.")
        except KeyError as e:
            messagebox.showerror("Помилка структури", str(e))
        except Exception as e:
            messagebox.showerror("Невідома помилка", str(e))

    # ---------- ПОЧАТОК ТЕСТУ ----------
    def start_test(self):
        try:
            if self.data is None:
                raise ValueError("Спочатку завантажте файл!")

            self.username = self.name_entry.get()
            if not self.username.strip():
                raise ValueError("Введіть ім'я!")

            count = int(self.q_count.get())
            if count <= 0 or count > len(self.data):
                raise ValueError("Некоректна кількість питань.")

            self.questions = self.data.sample(count).to_dict("records")
            self.current_question = 0
            self.score = 0
            self.show_question()

        except ValueError as e:
            messagebox.showerror("Помилка вводу", str(e))

    # ---------- ПОКАЗ ПИТАННЯ ----------
    def show_question(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        q = self.questions[self.current_question]
        tk.Label(self.root, text=q["question"], wraplength=400,
                 font=("Arial", 14)).pack(pady=10)

        self.answer_var = tk.StringVar()

        for opt in ["option1", "option2", "option3"]:
            tk.Radiobutton(self.root, text=q[opt], variable=self.answer_var,
                           value=q[opt]).pack(anchor="w")

        tk.Button(self.root, text="Далі", command=self.next_question).pack(pady=10)

    # ---------- ПЕРЕХІД ДО НАСТУПНОГО ----------
    def next_question(self):
        if self.answer_var.get() == "":
            messagebox.showwarning("Увага", "Оберіть відповідь!")
            return

        if self.answer_var.get() == self.questions[self.current_question]["correct"]:
            self.score += 1

        self.current_question += 1

        if self.current_question >= len(self.questions):
            self.finish_test()
        else:
            self.show_question()

    # ---------- ЗАВЕРШЕННЯ ТЕСТУ ----------
    def finish_test(self):
        result = f"Користувач: {self.username}\n" \
                 f"Правильних відповідей: {self.score}/{len(self.questions)}\n" \
                 f"Успішність: {self.score / len(self.questions) * 100:.1f}%"

        messagebox.showinfo("Результат", result)
        self.save_result(result)

    # ---------- ЗБЕРЕЖЕННЯ РЕЗУЛЬТАТУ ----------
    def save_result(self, text):
        filename = f"result_{self.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)

        messagebox.showinfo("Збережено", f"Результат записано у файл:\n{filename}")


# ---------- ЗАПУСК ПРОГРАМИ ----------
root = tk.Tk()
app = QuizApp(root)
root.mainloop()
