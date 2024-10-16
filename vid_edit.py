import os
import moviepy.editor as mp
import speech_recognition as sr
from googletrans import Translator
from llm.llama import LLM
import logging
import re
import json
import random
from transitions import transitions
from typing import List, Dict
from effects.effects import VideoEffects

from config import VIDEO_PATH, AUDIO_PATH, OUTPUT_DIR, TRANSITIONS_FILE, EFFECTS_FILE

class VideoProcessor:
    def __init__(self):
        self.translator = Translator()
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def process_video(self):
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
        
        self.extract_audio_from_video(VIDEO_PATH, AUDIO_PATH)
        transcript, timestamps = self.transcribe_audio_with_timestamps(AUDIO_PATH)
        
        if not transcript:
            logging.warning("No transcript available, skipping video processing.")
            return

        translated_transcript = self.translate_text(transcript)
        topics_text = self.divide_transcription_into_topics(translated_transcript)
        parsed_topics = self.parse_topics(topics_text)
        
        if not parsed_topics:
            logging.warning("No valid topics found, skipping video processing.")
            return

        transitions_info = self.load_transitions(TRANSITIONS_FILE)
        if not transitions_info:
            logging.warning("No transitions loaded. Proceeding without transitions.")
        
        effects_info = self.load_effects(EFFECTS_FILE)
        if not effects_info:
            logging.warning("No effects loaded. Proceeding without effects.")
        
        video = mp.VideoFileClip(VIDEO_PATH)
        segments = self.process_video_segments(video, parsed_topics, OUTPUT_DIR, effects_info)
        self.create_final_video(segments, transitions_info, OUTPUT_DIR)

    def extract_audio_from_video(self, video_path: str, audio_path: str):
        try:
            video = mp.VideoFileClip(video_path)
            audio = video.audio
            audio.write_audiofile(audio_path)
            logging.info(f"Audio extracted to {audio_path}")
        except IOError as e:
            logging.error(f"IO Error while extracting audio: {e}")
        except Exception as e:
            logging.error(f"Unexpected error while extracting audio: {e}")

    def transcribe_audio_with_timestamps(self, audio_path: str) -> tuple[str, List[tuple[float, float]]]:
        recognizer = sr.Recognizer()
        transcript = ""
        timestamps = []

        try:
            with sr.AudioFile(audio_path) as source:
                audio = recognizer.record(source)
            response = recognizer.recognize_google_cloud(audio, show_all=True)
            results = response.get('results', [])
            for result in results:
                alternatives = result.get('alternatives', [])
                for alternative in alternatives:
                    transcript += alternative.get('transcript', '') + ' '
                    # Append timestamp info if available
                    if 'timestamp' in alternative:
                        timestamps.append((alternative['timestamp'][0], alternative['timestamp'][1]))
            logging.info(f"Transcription completed. Detected language: {response.get('language', 'Unknown')}")
        except sr.UnknownValueError:
            logging.warning("Google Cloud Speech API could not understand audio")
        except sr.RequestError as e:
            logging.error(f"Could not request results from Google Cloud Speech API; {e}")
        return transcript.strip(), timestamps

    def translate_text(self, text: str, dest_language: str = 'en') -> str:
        try:
            translations = self.translator.translate([text], dest=dest_language)
            return ' '.join([translation.text for translation in translations])
        except Exception as e:
            logging.error(f"Error in translation: {e}")
            return text

    def divide_transcription_into_topics(self, transcript: str) -> str:
        prompt = (
            "You are given a transcription of a video. Please divide the transcription into distinct topics or segments. "
            "For each topic, provide the approximate start and end times in seconds. Format the response as follows:\n\n"
            "- Topic 1: Start Time - End Time\n"
            "- Topic 2: Start Time - End Time\n"
            "\nFor example:\n"
            "- Introduction: 0.0 - 30.5\n"
            "- Main Discussion: 30.5 - 120.0\n"
            "- Conclusion: 120.0 - 150.0\n\n"
            f"Transcript follows:\n\n{transcript}"
        )
        try:
            response = LLM(prompt)
            return response
        except Exception as e:
            logging.error(f"Error from LLM API: {e}")
            return ""

    def parse_topics(self, topics_text: str) -> List[Dict[str, float]]:
        parsed_topics = []
        for topic in topics_text.split('\n'):
            if topic.strip():
                match = re.match(r'(\d+(\.\d+)?) - (\d+(\.\d+)?)', topic)
                if match:
                    try:
                        start, end = map(float, match.groups()[0:3:2])
                        parsed_topics.append({'start': start, 'end': end})
                    except ValueError:
                        logging.warning(f"Invalid timestamp format: {topic}")
        return parsed_topics

    def load_transitions(self, transitions_file: str) -> Dict[str, Dict[str, any]]:
        try:
            with open(transitions_file, 'r') as f:
                data = json.load(f)
                return {t['name']: t for t in data['transitions']}
        except Exception as e:
            logging.error(f"Error loading transitions: {e}")
            return {}

    def load_effects(self, effects_file: str) -> Dict[str, Dict[str, any]]:
        try:
            with open(effects_file, 'r') as f:
                data = json.load(f)
                return {e['name']: e for e in data['effects']}
        except Exception as e:
            logging.error(f"Error loading effects: {e}")
            return {}

    def get_transition_suggestion(self, topic1: str, topic2: str, transitions: Dict[str, Dict[str, any]]) -> str:
        transition_names = list(transitions.keys())
        prompt = (
            f"Given two consecutive video segments with the following topics:\n"
            f"1. {topic1}\n"
            f"2. {topic2}\n"
            f"Suggest the most suitable transition effect from the following list:\n"
            f"{', '.join(transition_names)}\n"
            f"Respond with only the name of the transition effect."
        )
        try:
            response = LLM(prompt).strip()
            return response if response in transitions else random.choice(transition_names)
        except Exception as e:
            logging.error(f"Error getting transition suggestion: {e}")
            return random.choice(transition_names)

    def get_effect_suggestion(self, topic: str, effects: Dict[str, Dict[str, any]]) -> str:
        effect_names = list(effects.keys())
        prompt = (
            f"Given a video segment with the following topic:\n"
            f"{topic}\n"
            f"Suggest the most suitable video effect from the following list:\n"
            f"{', '.join(effect_names)}\n"
            f"Respond with only the name of the effect."
        )
        try:
            response = LLM(prompt).strip()
            return response if response in effects else random.choice(effect_names)
        except Exception as e:
            logging.error(f"Error getting effect suggestion: {e}")
            return random.choice(effect_names)

    def apply_transition(self, clip1_path: str, clip2_path: str, transition_name: str, transitions_info: Dict[str, Dict[str, any]]) -> mp.VideoClip:
        transition_info = transitions_info.get(transition_name)
        if transition_info and hasattr(transitions, transition_name):
            logging.info(f"Applying transition: {transition_info['description']}")
            transition_func = getattr(transitions, transition_name)
            output_file = transition_info['output_file']
            transition_func(clip1_path, clip2_path)
            return mp.VideoFileClip(output_file)
        else:
            logging.warning(f"Transition '{transition_name}' not found or not implemented. Concatenating clips without transition.")
            return mp.concatenate_videoclips([mp.VideoFileClip(clip1_path), mp.VideoFileClip(clip2_path)])

    def apply_effect(self, clip: mp.VideoClip, effect_name: str, effects_info: Dict[str, Dict[str, any]]) -> mp.VideoClip:
        effect_info = effects_info.get(effect_name)
        if effect_info and hasattr(VideoEffects, effect_name):
            logging.info(f"Applying effect: {effect_info['description']}")
            effect_func = getattr(VideoEffects, effect_name)
            return effect_func(clip)
        else:
            logging.warning(f"Effect '{effect_name}' not found or not implemented. Returning original clip.")
            return clip

    def process_video_segments(self, video: mp.VideoClip, parsed_topics: List[Dict[str, float]], output_dir: str, effects_info: Dict[str, Dict[str, any]]) -> List[str]:
        segments = []
        for i, topic in enumerate(parsed_topics):
            start_time, end_time = topic['start'], topic['end']
            segment = video.subclip(start_time, end_time)
            
            effect_name = self.get_effect_suggestion(f"Topic {i+1}", effects_info)
            segment_with_effect = self.apply_effect(segment, effect_name, effects_info)
            
            segment_path = os.path.join(output_dir, f"segment_{i}.mp4")
            segment_with_effect.write_videofile(segment_path)
            segments.append(segment_path)
        return segments

    def create_final_video(self, segments: List[str], transitions_info: Dict[str, Dict[str, any]], output_dir: str):
        final_video = mp.VideoFileClip(segments[0])
        for i in range(1, len(segments)):
            if transitions_info:
                transition_name = self.get_transition_suggestion(f"Topic {i}", f"Topic {i+1}", transitions_info)
                transition_clip = self.apply_transition(segments[i-1], segments[i], transition_name, transitions_info)
                final_video = mp.concatenate_videoclips([final_video, transition_clip])
            else:
                final_video = mp.concatenate_videoclips([final_video, mp.VideoFileClip(segments[i])])
    
        output_file = os.path.join(output_dir, "final_video_with_transitions.mp4")
        final_video.write_videofile(output_file, codec='libx264')
        logging.info(f"Final video with transitions saved to {output_file}")

if __name__ == "__main__":
    processor = VideoProcessor()
    processor.process_video()
