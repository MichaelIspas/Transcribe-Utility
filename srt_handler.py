# SRT handling for transcription

import re
from datetime import timedelta
import srt

class SRTHandler:
    """Handles generation and saving of SRT subtitle files from transcription data."""
    # example output from text file before srt conversion
    # [0.00s -> 6.80s]  Hi guys, so it's been quite a while.
    # [6.80s -> 14.50s] I hope you all are doing great.

    # example output after srt conversion
    # 1
    # 00:00:00,000 --> 00:00:06,800
    # Hi guys, so it's been quite a while.
    #
    # 2
    # 00:00:06,800 --> 00:00:14,500
    # I hope you all are doing great.

    # convert MM.SS to HH:MM:SS:ms
    @staticmethod
    def convert_time(seconds):
        hours, leftovers = divmod(seconds, 3600)
        minutes, seconds_left = divmod(leftovers, 60)
        whole_seconds = int(seconds_left)
        fraction = seconds_left - whole_seconds
        milliseconds = int(fraction * 1000)

        return f"{int(hours):02d}:{int(minutes):02d}:{whole_seconds:02d},{milliseconds:03d}"
    
    @staticmethod
    def parse_line(line):
        timestamp = r"\[(\d+\.\d+)s\s*->\s*(\d+\.\d+)s\]\s*(.+)"
        match = re.match(timestamp, line.strip())
        if not match:
            raise ValueError("Invaolid Format")

        start_section = float(match.group(1))
        end_section = float(match.group(2))
        text = match.group(3)

        return start_section, end_section, text

    @staticmethod
    def create_srt_content(txt_file):
        segments = []
        for index, line in enumerate(txt_file, 1):
            try:
                start_section, end_section, text = SRTHandler.parse_line(line.strip())
            except ValueError:
                print("Skipping bad line:", line.strip())
                continue

            start_str = SRTHandler.convert_time(start_section)
            end_str = SRTHandler.convert_time(end_section)

            section = str(index) + "\n" + start_str + " --> " + end_str + "\n" + text + "\n"

            segments.append(section)

        return "\n".join(segments)