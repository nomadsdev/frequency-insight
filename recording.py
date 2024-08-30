import pyaudio as pya
import wave
import numpy as np
from scipy.fft import fft as fft_transform
import os

# กำหนดค่าพารามิเตอร์สำหรับการบันทึก
FMT = pya.paInt16
CH = 1
RATE = 44100
CHUNK = 1024
OUT_DIR = "playback"
FREQ_DIR = "frequency"
OUT_FILE = os.path.join(OUT_DIR, "output.wav")
TAPE_FILE = os.path.join(FREQ_DIR, "tape.txt")

# สร้างโฟลเดอร์ถ้ายังไม่มี
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(FREQ_DIR, exist_ok=True)

class Recorder:
    def __init__(self):
        self.frames = []
        self.stream = None
        self.audio = pya.PyAudio()

    def begin_recording(self):
        print("Recording started...")
        self.frames = []
        self.stream = self.audio.open(format=FMT,
                                      channels=CH,
                                      rate=RATE,
                                      input=True,
                                      frames_per_buffer=CHUNK)
        self._record_audio()

    def _record_audio(self):
        try:
            while self.stream.is_active():
                data = self.stream.read(CHUNK)
                self.frames.append(data)
        except IOError as e:
            print(f"Error recording audio: {e}")

    def end_recording(self):
        if self.stream:
            print("Recording stopped.")
            self.stream.stop_stream()
            self.stream.close()
            self._write_wav_file()
            self._process_frequency()
        else:
            print("No active recording to stop.")

    def _write_wav_file(self):
        try:
            with wave.open(OUT_FILE, 'wb') as wf:
                wf.setnchannels(CH)
                wf.setsampwidth(self.audio.get_sample_size(FMT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(self.frames))
        except IOError as e:
            print(f"Error writing WAV file: {e}")

    def _process_frequency(self):
        try:
            with wave.open(OUT_FILE, 'rb') as wf:
                sample_rate = wf.getframerate()
                n_samples = wf.getnframes()
                audio_data = np.frombuffer(wf.readframes(n_samples), dtype=np.int16)

            transformed_yf = fft_transform(audio_data)
            frequency_xf = np.fft.fftfreq(n_samples, 1 / sample_rate)
            magnitudes = np.abs(transformed_yf)

            threshold = np.max(magnitudes) * 0.1
            peak_freqs = frequency_xf[magnitudes > threshold]

            self._record_frequencies(peak_freqs)
        except Exception as e:
            print(f"Error processing frequency: {e}")

    def _record_frequencies(self, peak_freqs):
        try:
            with open(TAPE_FILE, 'a') as file:
                for freq in peak_freqs:
                    if freq > 0:
                        file.write(f"{freq:.2f} Hz\n")
        except IOError as e:
            print(f"Error writing frequencies to file: {e}")

    def clean_up(self):
        if self.audio:
            self.audio.terminate()
