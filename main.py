import tkinter as tk
import random
import time
import customtkinter as ctk

class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("800x600")
        ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

        self.texts = [
            "The quick brown fox jumps over the lazy dog.",
            "Python is a high-level programming language.",
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "Programming is fun and challenging."
        ]
        self.current_text = tk.StringVar()
        self.user_input = tk.StringVar()
        self.start_time = None
        self.create_widgets()
        self.set_random_text()

    def create_widgets(self):
        self.header_frame = ctk.CTkFrame(self.root)
        self.header_frame.pack(pady=20)

        self.header_label = ctk.CTkLabel(self.header_frame, text="Typing Speed Test", font=ctk.CTkFont(size=24, weight="bold"))
        self.header_label.pack(pady=10)

        self.instructions = ctk.CTkLabel(self.header_frame, text="Type the text below as fast as you can:", font=ctk.CTkFont(size=14))
        self.instructions.pack(pady=10)

        self.text_display = ctk.CTkLabel(self.root, textvariable=self.current_text, font=ctk.CTkFont(size=14), wraplength=700, justify="center")
        self.text_display.pack(pady=20)

        self.entry = ctk.CTkEntry(self.root, textvariable=self.user_input, font=ctk.CTkFont(size=14), width=600)
        self.entry.pack(pady=10)
        self.entry.bind("<KeyRelease>", self.highlight_errors)

        self.start_button = ctk.CTkButton(self.root, text="Start", font=ctk.CTkFont(size=14), command=self.start_test)
        self.start_button.pack(pady=10)

        self.results_frame = ctk.CTkFrame(self.root)
        self.results_frame.pack(pady=20)

        self.results_label = ctk.CTkLabel(self.results_frame, text="", font=ctk.CTkFont(size=14))
        self.results_label.pack(side="left", padx=10)

        self.error_display = ctk.CTkLabel(self.results_frame, text="", font=ctk.CTkFont(size=14), text_color="red")
        self.error_display.pack(side="left", padx=10)

        self.progress_bar = ctk.CTkProgressBar(self.root, width=600)
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)

    def set_random_text(self):
        self.current_text.set(random.choice(self.texts))

    def start_test(self):
        self.start_time = time.time()
        self.entry.focus()
        self.start_button.configure(text="Check", command=self.check_result)
        self.user_input.set("")
        self.results_label.configure(text="")
        self.error_display.configure(text="")
        self.progress_bar.set(0)

    def highlight_errors(self, event):
        user_text = self.user_input.get()
        target_text = self.current_text.get()
        errors = [i for i, (x, y) in enumerate(zip(user_text, target_text)) if x != y]
        error_text = [" "]*len(target_text)
        for i in errors:
            error_text[i] = target_text[i]
        self.error_display.configure(text="Errors: " + "".join(error_text))

        progress = len(user_text) / len(target_text)
        self.progress_bar.set(progress)

    def check_result(self):
        end_time = time.time()
        user_text = self.user_input.get()
        time_taken = end_time - self.start_time
        correct_chars = sum(1 for x, y in zip(self.current_text.get(), user_text) if x == y)
        accuracy = (correct_chars / len(self.current_text.get())) * 100
        words_per_minute = len(user_text.split()) / (time_taken / 60)
        total_errors = sum(1 for x, y in zip(self.current_text.get(), user_text) if x != y)
        result_str = f"Time: {time_taken:.2f}s\nAccuracy: {accuracy:.2f}%\nWPM: {words_per_minute:.2f}\nErrors: {total_errors}"
        self.results_label.configure(text=result_str)
        self.start_button.configure(text="Start", command=self.start_test)

if __name__ == "__main__":
    root = ctk.CTk()
    app = TypingSpeedTest(root)
    root.mainloop()
