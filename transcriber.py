# Michael Ispas
# Transcriber module for Transcribe Utility

from faster_whisper import WhisperModel

class Transcriber:
    def __init__(self, model_size="small", device="cpu", compute_type="int8"):
        try:
            self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None

    def transcribe(self, filepath):
        if not self.model:
            return None, "Model not loaded!"
        try:
            segments, info = self.model.transcribe(filepath, beam_size=5)

            print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

            for segment in segments:
                print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
        
        except Exception as e:
            return None, f"Error during transcription: {e}"