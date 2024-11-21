import tkinter as tk
from tkinter import ttk, messagebox

class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("400x550")
        self.root.resizable(False, False)

        # Тайминги (в секундах)
        self.work_time = 25 * 60
        self.short_break = 5 * 60
        self.long_break = 15 * 60
        self.current_time = self.work_time
        self.timer_running = False
        self.session_count = 0

        # Цели и настройки
        self.daily_goal = 8  # Количество интервалов по умолчанию
        self.intervals_completed = 0
        self.intervals_before_long_break = 4  # Интервалы до длинного перерыва

        # Заголовок
        self.timer_label = ttk.Label(root, text="Pomodoro Timer", font=("Helvetica", 14))
        self.timer_label.pack(pady=10)

        # Таймер
        self.time_display = ttk.Label(root, text=self.format_time(self.current_time), font=("Helvetica", 48, "bold"))
        self.time_display.pack(pady=20)

        # Кнопки управления
        self.buttons_frame = ttk.Frame(root)
        self.buttons_frame.pack(pady=20)

        self.start_button = ttk.Button(self.buttons_frame, text="Start", command=self.start_timer)
        self.start_button.grid(row=0, column=0, padx=10)

        self.pause_button = ttk.Button(self.buttons_frame, text="Pause", command=self.pause_timer)
        self.pause_button.grid(row=0, column=1, padx=10)

        self.reset_button = ttk.Button(self.buttons_frame, text="Reset", command=self.reset_timer)
        self.reset_button.grid(row=0, column=2, padx=10)

        # Поля ввода для настройки времени
        self.settings_label = ttk.Label(root, text="Set Times (minutes):", font=("Helvetica", 12))
        self.settings_label.pack(pady=10)

        self.settings_frame = ttk.Frame(root)
        self.settings_frame.pack()

        ttk.Label(self.settings_frame, text="Work:", font=("Helvetica", 10)).grid(row=0, column=0, padx=5)
        self.work_time_entry = ttk.Entry(self.settings_frame, width=5, justify="center")
        self.work_time_entry.insert(0, "25")
        self.work_time_entry.grid(row=0, column=1, padx=5)

        ttk.Label(self.settings_frame, text="Short Break:", font=("Helvetica", 10)).grid(row=1, column=0, padx=5)
        self.short_break_entry = ttk.Entry(self.settings_frame, width=5, justify="center")
        self.short_break_entry.insert(0, "5")
        self.short_break_entry.grid(row=1, column=1, padx=5)

        ttk.Label(self.settings_frame, text="Long Break:", font=("Helvetica", 10)).grid(row=2, column=0, padx=5)
        self.long_break_entry = ttk.Entry(self.settings_frame, width=5, justify="center")
        self.long_break_entry.insert(0, "15")
        self.long_break_entry.grid(row=2, column=1, padx=5)

        # Настройка интервалов до длинного перерыва
        ttk.Label(self.settings_frame, text="Intervals Before Long Break:", font=("Helvetica", 10)).grid(row=3, column=0, padx=5)
        self.long_break_interval_entry = ttk.Entry(self.settings_frame, width=5, justify="center")
        self.long_break_interval_entry.insert(0, "4")
        self.long_break_interval_entry.grid(row=3, column=1, padx=5)

        # Кнопка Apply
        self.apply_button = ttk.Button(root, text="Apply", command=self.apply_settings)
        self.apply_button.pack(pady=10)

        # Цели
        self.goal_frame = ttk.Frame(root)
        self.goal_frame.pack(pady=10)

        ttk.Label(self.goal_frame, text="Set Daily Goal (Intervals):", font=("Helvetica", 12)).grid(row=0, column=0, padx=5)
        self.goal_entry = ttk.Entry(self.goal_frame, width=5, justify="center")
        self.goal_entry.insert(0, "8")
        self.goal_entry.grid(row=0, column=1, padx=5)

        self.goal_apply_button = ttk.Button(self.goal_frame, text="Set Goal", command=self.set_goal)
        self.goal_apply_button.grid(row=0, column=2, padx=10)

        self.progress_label = ttk.Label(root, text=self.get_progress_text(), font=("Helvetica", 12))
        self.progress_label.pack(pady=10)

    def format_time(self, seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}"

    def update_timer(self):
        if self.timer_running:
            if self.current_time > 0:
                self.current_time -= 1
                self.time_display.config(text=self.format_time(self.current_time))
                self.root.after(1000, self.update_timer)
            else:
                self.timer_running = False
                self.session_count += 1
                self.time_display.config(text="00:00")
                self.intervals_completed += 1
                self.update_progress()
                self.notify()
                self.start_next_session()

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()

    def pause_timer(self):
        self.timer_running = False

    def reset_timer(self):
        self.timer_running = False
        self.current_time = self.work_time
        self.timer_label.config(text="Pomodoro Timer")
        self.time_display.config(text=self.format_time(self.current_time))

    def start_next_session(self):
        if self.session_count % self.intervals_before_long_break == 0:
            self.current_time = self.long_break
            self.timer_label.config(text="Long Break")
        elif self.session_count % 2 == 0:
            self.current_time = self.short_break
            self.timer_label.config(text="Short Break")
        else:
            self.current_time = self.work_time
            self.timer_label.config(text="Work Time")
        self.time_display.config(text=self.format_time(self.current_time))

    def notify(self):
        if self.session_count % self.intervals_before_long_break == 0:
            messagebox.showinfo("Pomodoro Timer", "Time for a long break!")
        elif self.session_count % 2 == 0:
            messagebox.showinfo("Pomodoro Timer", "Time for a short break!")
        else:
            messagebox.showinfo("Pomodoro Timer", "Back to work!")

    def apply_settings(self):
        try:
            work_minutes = int(self.work_time_entry.get())
            short_break_minutes = int(self.short_break_entry.get())
            long_break_minutes = int(self.long_break_entry.get())
            intervals_before_long_break = int(self.long_break_interval_entry.get())

            if work_minutes <= 0 or short_break_minutes <= 0 or long_break_minutes <= 0 or intervals_before_long_break <= 0:
                raise ValueError("Values must be positive numbers.")

            # Обновляем значения таймеров
            self.work_time = work_minutes * 60
            self.short_break = short_break_minutes * 60
            self.long_break = long_break_minutes * 60
            self.intervals_before_long_break = intervals_before_long_break

            # Сбрасываем таймер на новое рабочее время
            self.reset_timer()

            # Уведомление об успешном применении
            messagebox.showinfo("Pomodoro Timer", "Settings applied successfully!")

        except ValueError:
            # Уведомление о неправильных данных
            messagebox.showerror("Pomodoro Timer", "Please enter valid positive numbers.")

    def set_goal(self):
        try:
            goal = int(self.goal_entry.get())
            if goal <= 0:
                raise ValueError("Goal must be a positive number.")
            self.daily_goal = goal
            self.intervals_completed = 0  # Сбрасываем прогресс при изменении цели
            self.update_progress()
            messagebox.showinfo("Pomodoro Timer", "Goal updated successfully!")
        except ValueError:
            messagebox.showerror("Pomodoro Timer", "Please enter a valid positive number.")

    def get_progress_text(self):
        return f"Progress: {self.intervals_completed}/{self.daily_goal} intervals completed"

    def update_progress(self):
        self.progress_label.config(text=self.get_progress_text())

# Создание окна приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()
