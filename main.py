# Michael Ispas
# Transcribe Utility

import tkinter as tk
#import srt
import threading
#import time
from tkinter import filedialog, messagebox
from transcriber import Transcriber

class TranscribeApp: # Covers GUI basic features
    def __init__(self, root_window):
        """Initialize the TranscribeApp with a Tkinter root window.

            Args: root_gui (tk.Tk): The main Tkinter window instance.
        """
        self.root = root_window
        self.root.geometry("800x500")
        self.root.title("Transcribe Utility")
        self.running = False

        # Initialize Transcriber
        self.transcriber = Transcriber(model_size="small", device="cpu",
                                       compute_type="int8")

        # Create menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # File dropdown menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.select_file)
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        # GUI elements
        self.open_button = tk.Button(self.root, text="Open File",
                                     command=self.select_file)
        self.open_button.pack(pady=10)

        self.transcribe_button = tk.Button(self.root, text="Transcribe",
                command=threading.Thread(target=self.transcribe_file).start,
                state=tk.DISABLED)
        self.transcribe_button.pack(pady=10)

        self.filepath = None

    def select_file(self):
        filepath = filedialog.askopenfilename(
            title="Select a file",
            initialdir="/", # Start from the root directory
            filetypes=[("Video files", "*.mp4 *.webm *.mov *.mkv")]
        )
        if filepath:
            self.filepath = filepath
            print(f"Selected file: {filepath}")
            self.transcribe_button.config(state=tk.NORMAL)
        else:
            self.filepath = None
            self.transcribe_button.config(state=tk.DISABLED)

    def transcribe_file(self):
        try:
            self.transcribe_button.config(state=tk.DISABLED)
            self.transcribe_button.config(text="Cancel", state=tk.NORMAL,
                                          command=self.cancel)
            transcription = self.transcriber.transcribe(self.filepath)
            messagebox.showinfo("Processed transcription.")
            return transcription
        except Exception as e:
            messagebox.showerror("Error", f"Transcription failed: {str (e)}.")
        finally:
            self.transcribe_button.config(text="Transcribe", state=tk.NORMAL)

    def cancel(self):
        self.transcribe_file.quit

if __name__ == "__main__":
    root = tk.Tk()
    app = TranscribeApp(root)
    root.mainloop()