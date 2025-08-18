# Michael Ispas
# Transcribe Utility

import tkinter as tk
#import srt
import threading
#import time
from tkinter import filedialog, messagebox
from transcriber import Transcriber
from multiprocessing import Process

class TranscribeApp: # Covers GUI basic features
    def __init__(self, root_window):
        """Initialize the TranscribeApp with a Tkinter root window.

            Args: root_gui (tk.Tk): The main Tkinter window instance.
        """
        self.root = root_window
        self.root.geometry("800x500")
        self.root.title("Transcribe Utility")

        # Initialize Transcriber
        self.transcriber = Transcriber(model_size="small", device="cpu",
                                       compute_type="int8")

        # Create menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.transcribe_button = None

        # File dropdown menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.select_file)
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        # GUI elements
        self.open_button = tk.Button(self.root, text="Open File",
                                     command=self.select_file)
        self.open_button.pack(pady=10)

        self.filepath = None

        self.transcription_process = None

    def open_new_window(self):
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("Transcribe")
        self.new_window.geometry("250x150")
        self.transcribe_button = tk.Button(self.new_window, text="Transcribe",
                                        command=threading.Thread(target=self.transcribe_file).start,
                                        state=tk.DISABLED)
        self.transcribe_button.pack(pady=10)

    def select_file(self):
        filepath = filedialog.askopenfilename(
            title="Select a file",
            initialdir="/", # Start from the root directory
            filetypes=[("Video files", "*.mp4 *.webm *.mov *.mkv")]
        )
        if filepath:
            self.filepath = filepath
            print(f"Selected file: {filepath}")
            self.open_new_window()
            if self.transcribe_button:
                self.transcribe_button.config(state=tk.NORMAL)
        else:
            self.filepath = None
            if self.transcribe_button:
                self.transcribe_button.config(state=tk.DISABLED)

    def transcribe_file(self):
        try:
            if self.transcribe_button:
                self.transcribe_button.config(state=tk.DISABLED)
            self.transcribe_button.config(text="Cancel", state=tk.NORMAL,
                                          command=self.cancel)
            self.transcription_process = Process(target=self.transcriber.transcribe,
                                                 args=(self.filepath,))
            self.transcription_process.start()
            messagebox.showinfo(message="Transcription Completed.")
        except Exception as e:
            messagebox.showerror(message=f"Error, Transcription failed: {str (e)}.")
        finally:
            self.transcribe_button.config(text="Transcribe", state=tk.NORMAL)

    def cancel(self):
        self.new_window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TranscribeApp(root)
    root.mainloop()