# Video Processor

A powerful Python-based tool for automated video processing, including transcription, translation, topic segmentation, and application of effects and transitions.

## Features

- Audio extraction from video
- Speech-to-text transcription with timestamps
- Text translation using Google Translate
- AI-powered topic segmentation
- Dynamic application of video effects
- Intelligent transition suggestions between segments
- Final video compilation with effects and transitions

## Requirements

- Python 3.7+
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/video-processor.git
   cd video-processor
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your API keys in `config.py`:
   - Groq API key for LLM functionality
   - Google Cloud API key for speech recognition (if using Google Speech-to-Text)

## Usage

1. Place your input video in the project directory.

2. Run the main script:
   ```
   python vid_edit.py
   ```

3. Follow the prompts to specify input video and output preferences.

## Configuration

- Adjust settings in `config.py` (API keys, default parameters)
- Customize effects in `effects/effects.json`
- Modify transitions in `transitions/transitions.json`

## Project Structure

- `vid_edit.py`: Main script for video processing
- `effects/`: Contains effects-related files
  - `effects.py`: Implementation of video effects
  - `effects.json`: Configuration for available effects
- `transitions/`: Contains transitions-related files
  - `transitions.py`: Implementation of video transitions
  - `transitions.json`: Configuration for available transitions
- `llm/`: Contains LLM-related files
  - `llama.py`: Implementation of LLM functionality using Groq

## Available Effects

The project supports various video effects, including:

- Fade in/out
- Color inversion
- Brightness and contrast adjustment
- Black and white conversion
- Rotation and resizing
- Cropping and mirroring
- Speed adjustment
- Text overlay
- Vignette effect
- Color filtering
- Edge detection
- Zoom effect
- Saturation adjustment

For a complete list of effects and their parameters, refer to `effects/effects.json`.

## Available Transitions

The project offers multiple transition effects between video segments:

- Roll transition
- B-roll overlay
- Crossfade
- Slide transition
- Wipe effect
- Zoom transition
- Split screen
- Circle reveal
- Page turn effect
- Light leak
- Color inversion
- Rotate transition
- Diagonal wipe
- Heart shape reveal
- Film roll effect
- Ripple effect
- Starfield transition

For a complete list of transitions and their descriptions, refer to `transitions/transitions.json`.

## Customization

### Adding New Effects

1. Implement the effect in `effects/effects.py`
2. Add the effect details to `effects/effects.json`

### Adding New Transitions

1. Implement the transition in `transitions/transitions.py`
2. Add the transition details to `transitions/transitions.json`

## AI-Powered Features

- Topic Segmentation: Utilizes LLM to intelligently divide the video into distinct topics.
- Effect Suggestion: AI suggests appropriate effects based on video content.
- Transition Recommendation: Intelligent selection of transitions between segments.

## Performance Considerations

- Processing time depends on video length and complexity of applied effects.
- Consider using shorter video clips for testing and experimentation.

## Troubleshooting

- Ensure all dependencies are correctly installed.
- Check API key configurations in `config.py`.
- Verify input video format compatibility.
- For LLM-related issues, check Groq API status and quota.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch: `git checkout -b feature-branch-name`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-branch-name`
5. Submit a pull request

## License

[Your chosen license]

## Acknowledgements

- MoviePy for video processing capabilities
- Groq for LLM functionality
- Google Cloud Speech-to-Text for transcription
- Google Translate for translation services

## Future Enhancements

- Support for batch processing multiple videos
- GUI for easier interaction and preview of effects
- Integration with cloud storage services
- Enhanced AI-driven content analysis and editing suggestions
- Support for additional languages in transcription and translation

## Contact

For questions, issues, or suggestions, please open an issue on the GitHub issue.