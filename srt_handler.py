# SRT handling for transcription

import re
import srt
from datetime import timedelta

class SRTHandler:
    """Handles generation and saving of SRT subtitle files from transcription data."""

    # example output from text file before srt conversion
    # 0.00s -> 6.80s]  Hi guys, so it's been quite a while.

    # example output after srt conversion
    # 1
    # 00:00:00,000 --> 00:00:06,800
    # Hi guys, so it's been quite a while.
    # 
    # 2
    # 00:00...

    # convert MM.SS to HH:MM:SS:ms
    def convert_time(seconds):
        hours, leftovers = divmod(seconds, 3600)
        minutes, seconds_left = divmod(leftovers, 60)
        whole_seconds = int(seconds_left)
        fraction = seconds_left - whole_seconds
        milliseconds = int(fraction * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{whole_seconds:02d},{milliseconds:03d}"
    
    def parse_line(line):
        timestamp = r"(\d+\.\d+)s\s*->\s*(\d+\.\d+)s\]\s*(.+)"
        match = re.match(timestamp, line.strip())
        if not match:
            raise ValueError("Invaolid Format")
        
        start_section = float(match.group(1))
        end_section = float(match.group(2))
        text = match.group(3)
        
        return start_section, end_section, text
    
        # finish up parsing with convert_time function here

