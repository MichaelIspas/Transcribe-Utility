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

    def convert_time():