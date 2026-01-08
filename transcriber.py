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

    def transcribe(self, filepath, progress_callback=None, stop_event=None):
        if not self.model:
            return None, "Model not loaded!"
        try:
            segments, info = self.model.transcribe(filepath, beam_size=5)

            print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

            total_duration = info.duration if info.duration > 0 else 1
            processed = 0.0  # Track progress across segments

            for segment in segments:
                if stop_event and stop_event.is_set():
                    print("\n[Transcription cancelled by user]")
                    break
                
                print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

                if progress_callback and total_duration:
                    new_processed = segment.end
                    if new_processed > processed:
                        processed = new_processed
                        progress = (processed / total_duration) * 100
                        progress_callback(progress)

            # Signal 100% when finished
            if progress_callback and not (stop_event and stop_event.is_set()):
                progress_callback(100.0)

        except Exception as e:
            return None, f"Error during transcription: {e}"