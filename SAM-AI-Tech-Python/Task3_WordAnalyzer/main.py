import re
import tkinter as tk
from collections import Counter
from pathlib import Path
from tkinter import filedialog, messagebox

class TextAnalyzerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python Text Analyzer")
        self.configure(bg="#1d1f21")
        self.geometry("540x520")
        self.minsize(520, 500)

        self.file_path = None
        self.text_content = ""
        self._build_ui()

    def _build_ui(self):
        header = tk.Label(self, text="Text Analyzer", bg="#1d1f21", fg="#f5f5f5",
                          font=("Segoe UI", 20, "bold"))
        header.pack(pady=(16, 8))

        button_frame = tk.Frame(self, bg="#1d1f21")
        button_frame.pack(fill="x", padx=16, pady=8)

        open_button = tk.Button(button_frame, text="Open File", command=self.open_file,
                                bg="#282c34", fg="#ffffff", font=("Segoe UI", 11), bd=0, padx=12, pady=10)
        open_button.pack(side="left")

        analyze_button = tk.Button(button_frame, text="Analyze Text", command=self.analyze_text,
                                   bg="#3a7bd5", fg="#ffffff", font=("Segoe UI", 11), bd=0, padx=12, pady=10)
        analyze_button.pack(side="left", padx=12)

        self.status_label = tk.Label(self, text="Choose a text file to analyze.", bg="#1d1f21", fg="#b0b0b0",
                                     font=("Segoe UI", 10))
        self.status_label.pack(anchor="w", padx=18)

        self.result_box = tk.Text(self, bg="#121416", fg="#e8e6e3", font=("Segoe UI", 11), bd=0,
                                  padx=12, pady=12, wrap="word", state="disabled", height=18)
        self.result_box.pack(fill="both", expand=True, padx=16, pady=(8, 16))

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not path:
            return
        try:
            self.file_path = Path(path)
            self.text_content = self.file_path.read_text(encoding="utf-8")
            self.status_label.config(text=f"Loaded: {self.file_path.name}")
            self._show_results("File loaded successfully. Click Analyze Text to continue.")
        except FileNotFoundError:
            messagebox.showerror("File Not Found", "The selected file could not be located.")
        except Exception as exc:
            messagebox.showerror("Error", f"Could not read file: {exc}")

    def analyze_text(self):
        if not self.text_content:
            messagebox.showwarning("No File", "Please open a text file before analyzing.")
            return

        word_list = re.findall(r"\b[\w']+\b", self.text_content.lower())
        sentence_count = len(re.findall(r"[.!?]+", self.text_content))
        character_count = len(self.text_content)
        word_count = len(word_list)
        top_words = Counter(word_list).most_common(10)

        results = [
            f"File: {self.file_path.name if self.file_path else 'Untitled'}",
            f"Words: {word_count}",
            f"Characters: {character_count}",
            f"Sentences: {sentence_count}",
            "",
            "Top frequent words:",
        ]
        for word, count in top_words:
            results.append(f"  {word}: {count}")

        self._show_results("\n".join(results))

    def _show_results(self, text: str):
        self.result_box.config(state="normal")
        self.result_box.delete("1.0", tk.END)
        self.result_box.insert(tk.END, text)
        self.result_box.config(state="disabled")


if __name__ == "__main__":
    app = TextAnalyzerApp()
    app.mainloop()
