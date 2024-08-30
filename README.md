# SoundFreqAnalyzer

**SoundFreqAnalyzer** is a Python project designed to record audio, analyze its frequency components, and save the frequency data to a file. This tool is useful for audio analysis, signal processing, and frequency domain analysis.

## Features

- **Audio Recording:** Record audio from the microphone and save it as a WAV file.
- **Frequency Analysis:** Convert the recorded audio to the frequency domain using FFT (Fast Fourier Transform).
- **Frequency Data Storage:** Save detected frequencies to a text file for further analysis.

## Requirements

- Python 3.6 or higher
- `pyaudio` for audio recording
- `numpy` for numerical operations
- `scipy` for FFT computation
- `keyboard` for capturing keyboard events

You can install the required Python libraries using pip:

```bash
pip install pyaudio numpy scipy keyboard
```

## Usage

1. **Start Recording:**
   - Run the script.
   - Press `1` to start recording audio.
   - Press `0` to stop recording.

2. **Frequency Analysis:**
   - Once recording is stopped, the script will automatically analyze the frequency components of the recorded audio.
   - The detected frequencies will be saved in `frequency/tape.txt`.

3. **Quit Program:**
   - Press `q` to exit the program.

## File Structure

- `playback/output.wav`: Contains the recorded audio data.
- `frequency/tape.txt`: Contains the analyzed frequency data in Hz.

## Running the Program

To run the program, execute the following command in your terminal:

```bash
python main.py
```

## License

This project is licensed under the MIT License.

## Contributing

If you want to contribute to this project, feel free to open an issue or submit a pull request on GitHub.

## Contact

For any questions or suggestions, please contact [support@jmmentertainment.com](mailto:support@jmmentertainment.com).
