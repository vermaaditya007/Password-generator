"""Tkinter GUI for the password generator."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from .generator import PasswordOptions, generate_password


class PasswordGeneratorApp(ttk.Frame):
    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root, padding=16)
        self.root = root
        self.root.title("Random Password Generator")
        self.root.minsize(460, 360)

        self.length_var = tk.IntVar(value=16)
        self.lowercase_var = tk.BooleanVar(value=True)
        self.uppercase_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        self.require_each_var = tk.BooleanVar(value=True)
        self.exclude_var = tk.StringVar(value="")
        self.password_var = tk.StringVar(value="")

        self.grid(sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self._build_widgets()
        self.generate()

    def _build_widgets(self) -> None:
        title = ttk.Label(self, text="Random Password Generator", font=("Segoe UI", 16, "bold"))
        title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 14))

        ttk.Label(self, text="Length").grid(row=1, column=0, sticky="w")
        length_spin = ttk.Spinbox(self, from_=4, to=128, textvariable=self.length_var, width=8)
        length_spin.grid(row=1, column=1, sticky="w", pady=4)

        checks = [
            ("Lowercase letters", self.lowercase_var),
            ("Uppercase letters", self.uppercase_var),
            ("Digits", self.digits_var),
            ("Symbols", self.symbols_var),
            ("Require each selected type", self.require_each_var),
        ]

        for row, (label, variable) in enumerate(checks, start=2):
            ttk.Checkbutton(self, text=label, variable=variable).grid(
                row=row, column=0, columnspan=2, sticky="w", pady=2
            )

        ttk.Label(self, text="Exclude characters").grid(row=7, column=0, sticky="w", pady=(12, 0))
        exclude_entry = ttk.Entry(self, textvariable=self.exclude_var)
        exclude_entry.grid(row=7, column=1, sticky="ew", pady=(12, 0))

        result_entry = ttk.Entry(
            self,
            textvariable=self.password_var,
            font=("Consolas", 12),
            state="readonly",
        )
        result_entry.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(18, 8))

        button_frame = ttk.Frame(self)
        button_frame.grid(row=9, column=0, columnspan=2, sticky="ew")
        button_frame.columnconfigure((0, 1), weight=1)

        ttk.Button(button_frame, text="Generate", command=self.generate).grid(
            row=0, column=0, sticky="ew", padx=(0, 6)
        )
        ttk.Button(button_frame, text="Copy", command=self.copy_to_clipboard).grid(
            row=0, column=1, sticky="ew", padx=(6, 0)
        )

        hint = ttk.Label(
            self,
            text="Tip: exclude similar-looking characters like O0Il1 if you need easy typing.",
            foreground="#555555",
            wraplength=420,
        )
        hint.grid(row=10, column=0, columnspan=2, sticky="w", pady=(14, 0))

    def generate(self) -> None:
        options = PasswordOptions(
            length=self.length_var.get(),
            use_lowercase=self.lowercase_var.get(),
            use_uppercase=self.uppercase_var.get(),
            use_digits=self.digits_var.get(),
            use_symbols=self.symbols_var.get(),
            exclude=self.exclude_var.get(),
            require_each_selected_type=self.require_each_var.get(),
        )

        try:
            self.password_var.set(generate_password(options))
        except ValueError as error:
            messagebox.showerror("Invalid settings", str(error), parent=self.root)

    def copy_to_clipboard(self) -> None:
        password = self.password_var.get()
        if not password:
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        self.root.update()
        messagebox.showinfo("Copied", "Password copied to clipboard.", parent=self.root)


def main() -> None:
    root = tk.Tk()
    PasswordGeneratorApp(root)
    root.mainloop()
