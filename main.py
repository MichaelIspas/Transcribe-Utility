# Michael Ispas
# Transcribe Utility
# Resources:
# Whisper Docs - https://github.com/openai/whisper
# Whisper Fork - https://github.com/Purfview/# whisper-standalone-win
# Tkinter GUI - https://docs.python.org/3/library/tkinter.html

import tkinter as tk
from tkinter import filedialog

class TranscribeApp:
    def __init__(self, root):
        self.root = tk.Tk()
        self.root.geometry("800x500")
        self.root.title("Transcribe Utility")

        # Open File Button
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