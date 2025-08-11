# Michael Ispas
# Transcribe Utility

import tkinter as tk
from tkinter import filedialog

class TranscribeApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x500")
        self.root.title("Transcribe Utility")

        # Create menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # File dropdown menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.select_file)
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        # Open file button
        self.open_button = tk.Button(self.root, text="Open File", command=self.select_file)
        self.open_button.pack(pady=20)

    def select_file(self):
        filepath = filedialog.askopenfilename(
            title="Select a file",
            initialdir="/", # Start from the root directory
            filetypes=[("Video files", "*.mp4 *.webm *.mov *.mkv")]
        )
        if filepath:
            print(f"Selected file: {filepath}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TranscribeApp(root)
    root.mainloop()