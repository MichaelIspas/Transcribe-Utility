# Michael Ispas
# Transcribe Utility

import tkinter as tk
import sys
import os
from multiprocessing import Process
from tkinter import filedialog, messagebox, ttk
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
        self.filepath = None
        self.transcription_process = None

        # File dropdown menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.select_file)
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        # GUI elements
        self.open_button = tk.Button(self.root, text="Open File",
                                     command=self.select_file)
        self.open_button.pack(pady=10)

    @staticmethod
    def run_transcription(filepath, model_size, device, compute_type):
        transcriber = Transcriber(model_size=model_size, device=device, compute_type=compute_type)

        txt_output = os.path.splitext(filepath)[0] + '.txt'
        srt_output = os.path.splitext(filepath)[0] + '.srt'
        
        with open(txt_output, 'w', encoding='utf-8') as f:
            sys.stdout = f
            transcriber.transcribe(filepath)
            sys.stdout = sys.__stdout__

        with open(txt_output, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        lines = [line for line in lines if line.strip().startswith('[')]
        srt_content = SRTHandler.create_srt_content(lines)

        with open(srt_output, 'w', encoding='utf-8') as f:
            f.write(srt_content)

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
        self.new_window.geometry("350x250")

        # Display progress bar
        self.progress_bar = ttk.Progressbar(self.new_window, orient="horizontal", length=200)
        self.progress_bar.place(x=30, y=60, width=200)
        self.progress_bar.pack(pady=30)

        # Display transcribe button
        self.transcribe_button = tk.Button(self.new_window, text="Transcribe",
                                        command=self.transcribe_file,
                                        state=tk.NORMAL if self.filepath else
                                        tk.DISABLED)
        self.transcribe_button.pack(pady=10)

    def transcribe_file(self):
        try:
            # Start progress bar visual
            self.progress_bar.start(10)

            # Change button to Cancel
            self.transcribe_button.config(text="Cancel", command=self.cancel)
            
            # Run transcription in background
            self.transcription_process = Process(
                target=TranscribeApp.run_transcription, 
                args=(self.filepath, "small", "cpu", "int8"))
            self.transcription_process.start()
            print("Transcription started.")

            # Check every 100 milliseconds if done
            self.root.after(100, self.check_if_done)
        
        except Exception as e:
            messagebox.showerror(message=f"Error, Transcription failed: {str (e)}.")

    def check_if_done(self):
        if self.transcription_process.is_alive():
            self.root.after(100, self.check_if_done)
        else:
            self.progress_bar.stop()
            self.transcribe_button.config(text="Close", command=self.new_window.destroy)
            print("Transcription completed.")

    def cancel(self):
        if self.transcription_process and self.transcription_process.is_alive():
            self.transcription_process.terminate()
        self.new_window.destroy()
        print("Transcription cancelled. ")

if __name__ == "__main__":
    root = tk.Tk()
    app = TranscribeApp(root)
    root.mainloop()
