# Michael Ispas
# Transcribe Utility

import multiprocessing
import sys
import time
import tkinter as tk
import os
import threading
from tkinter import filedialog, ttk
from transcriber import Transcriber
from srt_handler import SRTHandler

class TranscribeApp: # Covers GUI basic features
    def __init__(self, root_window):
        """Initialize the TranscribeApp with a Tkinter root window.

            Args: root_window (tk.Tk): The main Tkinter window instance.
        """
        self.root = root_window
        self.root.geometry("800x500")
        self.root.title("Transcribe Utility")

        self.transcriber = Transcriber(model_size="small", device="cpu", compute_type="int8")
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.transcribe_button = None
        self.new_window = None
        self.progress_bar = None
        self.filepath = None
        self.transcription_thread = None
        self.cancelled = False

        # File dropdown menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.select_file)
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        # GUI elements
        self.open_button = tk.Button(self.root, text="Open File",
                                     command=self.select_file)
        self.open_button.pack(pady=10)

        self.transcribe_button = None

    @staticmethod
    def run_transcription(filepath, model_size, device, compute_type, progress_callback=None):
        transcriber = Transcriber(model_size=model_size, device=device, compute_type=compute_type)

        txt_output = os.path.splitext(filepath)[0] + '.txt'
        srt_output = os.path.splitext(filepath)[0] + '.srt'

        # Redirect stdout and transcribe with progress
        original_stdout = sys.stdout
        try:
            with open(txt_output, 'w', encoding='utf-8') as f:
                sys.stdout = f
                transcriber.transcribe(filepath, progress_callback=progress_callback)
        finally:
            sys.stdout = original_stdout

        # Generate SRT
        with open(txt_output, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        lines = [line for line in lines if line.strip().startswith('[')]
        srt_content = SRTHandler.create_srt_content(lines)

        with open(srt_output, 'w', encoding='utf-8') as f:
            f.write(srt_content)

        # Signal 100%
        if progress_callback:
            progress_callback(100.0)

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
        else:
            self.filepath = None
            self.transcribe_button.config(state=tk.DISABLED)

    def open_new_window(self):
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("Transcribe")
        self.new_window.geometry("600x350")

        # Display transcribe button
        self.transcribe_button = tk.Button(
            self.new_window,
            text="Transcribe",
            width=15,
            height=2,
            command=self.transcribe_file,
            state=tk.NORMAL if self.filepath else tk.DISABLED
        )
        self.transcribe_button.pack(pady=10)

        self.create_progress_bar()

    def transcribe_file(self):
        self.cancelled = False
        self.transcribe_button.config(text="Cancel", command=self.cancel)

        def update_progress(value):
            self.progress_bar["value"] = value
            self.new_window.update_idletasks()

        # Run transcription in background
        self.transcription_thread = threading.Thread(
            target=self.run_transcription,
            args=(self.filepath, "small", "cpu", "int8", update_progress),
            daemon=True
        )
        self.transcription_thread.start()
        print("Transcription started.")

        # Check every 100 milliseconds if done
        self.root.after(100, self.check_if_done)

    def check_if_done(self):
        if self.transcription_thread.is_alive():
            self.root.after(100, self.check_if_done)
        else:
            if not self.cancelled:
                self.progress_bar["value"] = 100
                self.transcribe_button.config(text="Close", command=self.new_window.destroy)
                print("Transcription completed.")

    def cancel(self):
        self.cancelled = True
        self.transcribe_button.config(state="disabled", text="Cancelling...")
        print("Transcription cancelled.")

        def delayed_close():
            time.sleep(1)  # give thread a moment to die
            if not self.transcription_thread.is_alive():
                self.new_window.destroy()

        threading.Thread(target=delayed_close, daemon=True).start()

    def create_progress_bar(self):
        # Progress bar parameters
        self.progress_bar = ttk.Progressbar(
            self.new_window,
            orient="horizontal",
            length=400,
            mode="determinate",
            maximum=100
        )
        self.progress_bar.pack(pady=30)
        self.progress_bar["value"] = 0

if __name__ == "__main__":
    multiprocessing.freeze_support()
    root = tk.Tk()
    app = TranscribeApp(root)
    root.mainloop()
