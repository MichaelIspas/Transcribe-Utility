# Michael Ispas
# Transcribe Utility

import tkinter as tk
#import srt
from tkinter import filedialog, messagebox
from transcriber import Transcriber
from multiprocessing import Process

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
        from transcriber import Transcriber
        transcriber = Transcriber(model_size=model_size, device=device, compute_type=
                                  compute_type)
        transcriber.transcribe(filepath)

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
            self.transcribe_button.config(state=tk.NORMAL)
        else:
            self.filepath = None
            self.transcribe_button.config(state=tk.DISABLED)

    def open_new_window(self):
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("Transcribe")
        self.new_window.geometry("250x150")
        self.transcribe_button = tk.Button(self.new_window, text="Transcribe",
                                        command=self.transcribe_file,
                                        state=tk.DISABLED)
        self.transcribe_button.pack(pady=10)

    def transcribe_file(self):
        try:
            self.transcribe_button.config(state=tk.DISABLED)
            self.transcribe_button.config(text="Cancel", state=tk.NORMAL,
                                          command=self.cancel)
            self.transcription_process = Process(
                target=TranscribeApp.run_transcription, 
                args=(self.filepath, "small", "cpu", "int8"))
            self.transcription_process.start()
            #messagebox.showinfo(message="Transcription Completed.")
        except Exception as e:
            messagebox.showerror(message=f"Error, Transcription failed: {str (e)}.")
        finally:
            self.transcribe_button.config(text="Transcribe", state=tk.NORMAL)

    def cancel(self):
        if hasattr(self, 'transcription_process') and self.transcription_process and self.  transcription_process.is_alive():
            self.transcription_process.terminate()
        if hasattr(self, 'new_window') and self.new_window.winfo_exists():
            self.new_window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TranscribeApp(root)
    root.mainloop()