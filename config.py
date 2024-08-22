import os
import logging

GROK_API_KEY = os.getenv("GROK_API_KEY")

# Input/Output Paths
VIDEO_PATH = 'input/video.mp4'
AUDIO_PATH = 'input/audio.wav'
OUTPUT_DIR = 'output'

# Transcription and Translation Settings
TRANSCRIBE_LANGUAGE = 'auto'  # Changed to 'auto' for auto-detection
TRANSLATE_LANGUAGE = 'en'

# Transitions Settings
TRANSITIONS_FILE = 'transitions/transitions.json'

# Effects Settings
EFFECTS_FILE = 'effects/effects.json'

# Logging Settings
LOG_LEVEL = 'INFO'
LOG_FILE = 'logs/video_processing.log'

# Initialize Logger
logging.basicConfig(
    filename=LOG_FILE,
    level=LOG_LEVEL,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)