import tkinter as tk
from tkinter import ttk, messagebox
from math import sqrt

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Modern Python Calculator")
        self.configure(bg="#121212")
        self.geometry("400x580")
        self.minsize(360, 520)
        self.expression = ""
        self.history = []

        self._build_interface()

    def _build_interface(self):
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Segoe UI", 14), foreground="#ffffff", background="#1f1f1f")
        self.style.map("TButton",
                       foreground=[("active", "#ffffff")],
                       background=[("active", "#333333")])

        display_frame = tk.Frame(self, bg="#121212")
        display_frame.pack(fill="x", padx=16, pady=(16, 10))

        self.display_var = tk.StringVar(value="0")
        display_label = tk.Label(display_frame, textvariable=self.display_var, anchor="e", bg="#121212", fg="#ffffff",
                                 font=("Segoe UI Variable", 34), padx=14)
        display_label.pack(fill="x")

        history_frame = tk.Frame(self, bg="#171717")
        history_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        history_label = tk.Label(history_frame, text="History", bg="#171717", fg="#bbbbbb", font=("Segoe UI", 10, "bold"))
        history_label.pack(anchor="w", padx=8, pady=(8, 4))

        self.history_box = tk.Listbox(history_frame, bg="#1a1a1a", fg="#ffffff", highlightthickness=0, bd=0,
                                      font=("Segoe UI", 10), selectbackground="#444444")
        self.history_box.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        button_frame = tk.Frame(self, bg="#121212")
        button_frame.pack(fill="x", padx=16, pady=(0, 16))

        buttons = [
            ["C", "⌫", "%", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "^", "√"],
            ["=", "HISTORY", "", ""]
        ]

        for row_index, row_values in enumerate(buttons):
            row_frame = tk.Frame(button_frame, bg="#121212")
            row_frame.pack(fill="x", pady=6)
            for col_index, label in enumerate(row_values):
                if not label:
                    spacer = tk.Frame(row_frame, width=80, bg="#121212")
                    spacer.pack(side="left", padx=4)
                    continue
                action = self._button_action(label)
                button = ttk.Button(row_frame, text=label, command=action, width=8)
                button.pack(side="left", expand=True, fill="x", padx=4)
                if label == "=":
                    button.configure(style="Accent.TButton")

    def _button_action(self, label):
        if label == "C":
            return self.clear
        if label == "⌫":
            return self.backspace
        if label == "=":
            return self.calculate
        if label == "√":
            return lambda: self.append_text("sqrt(")
        if label == "HISTORY":
            return self.show_history
        if label == "^":
            return lambda: self.append_text("**")
        return lambda: self.append_text(label)

    def append_text(self, value):
        if self.display_var.get() == "0" and value not in (".", "sqrt("):
            self.expression = value
        else:
            self.expression += value
        self.display_var.set(self.expression)

    def clear(self):
        self.expression = ""
        self.display_var.set("0")

    def backspace(self):
        self.expression = self.expression[:-1]
        if not self.expression:
            self.display_var.set("0")
        else:
            self.display_var.set(self.expression)

    def calculate(self):
        if not self.expression:
            return
        try:
            result = eval(self.expression, {"__builtins__": None}, {"sqrt": sqrt})
            if result is None:
                raise ValueError("Invalid calculation")
            output = str(round(result, 10)).rstrip("0").rstrip(".") if isinstance(result, float) else str(result)
            self.add_history(self.expression, output)
            self.expression = output
            self.display_var.set(output)
        except ZeroDivisionError:
            self._show_error("Cannot divide by zero.")
        except (SyntaxError, NameError, ValueError, TypeError):
            self._show_error("Enter a valid expression.")

    def add_history(self, expression, result):
        entry = f"{expression} = {result}"
        self.history.insert(0, entry)
        self.history_box.insert(0, entry)
        if len(self.history) > 20:
            self.history.pop()
            self.history_box.delete(tk.END)

    def show_history(self):
        history_text = "\n".join(self.history) if self.history else "No history yet."
        messagebox.showinfo("Calculation History", history_text)

    def _show_error(self, message):
        messagebox.showerror("Error", message)
        self.expression = ""
        self.display_var.set("0")

if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
