import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from search.search import check_username, filter_results
from platforms import SOCIAL_PLATFORMS
from validation.validation import is_valid_username
import threading
import json

class UsernameHunterGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("UsernameHunter - GUI (Tkinter)")
        self.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        frm = ttk.Frame(self)
        frm.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(frm, text="Usernames (one per line):").pack(anchor=tk.W)
        self.usernames_text = scrolledtext.ScrolledText(frm, height=6)
        self.usernames_text.pack(fill=tk.X)

        ttk.Label(frm, text="Platforms:").pack(anchor=tk.W, pady=(10,0))
        self.platforms_var = tk.StringVar(value=list(SOCIAL_PLATFORMS.keys()))
        self.platforms_list = tk.Listbox(frm, listvariable=self.platforms_var, selectmode=tk.MULTIPLE, height=8)
        self.platforms_list.pack(fill=tk.X)

        self.check_btn = ttk.Button(frm, text="Check Username", command=self.start_check)
        self.check_btn.pack(pady=10)

        self.result_text = scrolledtext.ScrolledText(frm, height=18)
        self.result_text.pack(fill=tk.BOTH, expand=True)

        self.export_btn = ttk.Button(frm, text="Export JSON", command=self.export_json)
        self.export_btn.pack(pady=5)
        self.results_all = {}

    def start_check(self):
        self.result_text.delete(1.0, tk.END)
        usernames = [u.strip() for u in self.usernames_text.get(1.0, tk.END).splitlines() if u.strip()]
        selected = [self.platforms_list.get(i) for i in self.platforms_list.curselection()]
        if not usernames:
            messagebox.showwarning("Input Error", "Please enter at least one username.")
            return
        self.check_btn.config(state=tk.DISABLED)
        threading.Thread(target=self.check_usernames, args=(usernames, selected), daemon=True).start()

    def check_usernames(self, usernames, selected):
        self.results_all = {}
        for username in usernames:
            valid, reason = is_valid_username(username)
            if not valid:
                self.result_text.insert(tk.END, f"[WARNING] {username}: {reason}\n")
                continue
            results = check_username(username, platforms={k: v for k, v in SOCIAL_PLATFORMS.items() if not selected or k in selected})
            filtered = filter_results(results)
            self.results_all[username] = filtered
            self.result_text.insert(tk.END, f"\nHasil untuk: {username}\n")
            for platform, info in filtered.items():
                status = "Terdaftar" if info['exists'] else ("Tidak Terdaftar" if info['exists'] is False else "Tidak Diketahui")
                self.result_text.insert(tk.END, f"[{platform}] {status}\n  URL: {info['url']}\n")
                if 'error' in info:
                    self.result_text.insert(tk.END, f"  Error: {info['error']}\n")
        self.check_btn.config(state=tk.NORMAL)

    def export_json(self):
        if not self.results_all:
            messagebox.showinfo("Export", "No results to export.")
            return
        file = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file:
            with open(file, "w", encoding="utf-8") as f:
                json.dump(self.results_all, f, indent=2)
            messagebox.showinfo("Export", f"Results exported to {file}")

if __name__ == "__main__":
    app = UsernameHunterGUI()
    app.mainloop()
