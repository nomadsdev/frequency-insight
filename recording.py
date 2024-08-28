import pyaudio as pya
import wave as wav
import numpy as np
from scipy.fft import fft as fft_transform
import os as osys

# กำหนดค่าพารามิเตอร์สำหรับการบันทึก
FMT = pya.paInt16
CH = 1
RATE = 44100
CHUNK = 1024
OUT_DIR = "playback"
FREQ_DIR = "frequency"
OUT_FILE = osys.path.join(OUT_DIR, "output.wav")
TAPE_FILE = osys.path.join(FREQ_DIR, "tape.txt")

# สร้างโฟลเดอร์ถ้ายังไม่มี
osys.makedirs(OUT_DIR, exist_ok=True)
osys.makedirs(FREQ_DIR, exist_ok=True)

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

    def end_recording(self):
        if self.stream:
            print("Recording stopped.")
            self.stream.stop_stream()
            self.stream.close()
            self._write_wav_file()
            self._process_frequency()

    def _write_wav_file(self):
        with wav.open(OUT_FILE, 'wb') as wf:
            wf.setnchannels(CH)
            wf.setsampwidth(self.audio.get_sample_size(FMT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(self.frames))

    def _process_frequency(self):
        with wav.open(OUT_FILE, 'rb') as wf:
            sample_rate = wf.getframerate()
            n_samples = wf.getnframes()
            audio_data = np.frombuffer(wf.readframes(n_samples), dtype=np.int16)

        transformed_yf = fft_transform(audio_data)
        frequency_xf = np.fft.fftfreq(n_samples, 1 / sample_rate)
        magnitudes = np.abs(transformed_yf)

        threshold = np.max(magnitudes) * 0.1
        peak_freqs = frequency_xf[magnitudes > threshold]

        self._record_frequencies(peak_freqs)

    def _record_frequencies(self, peak_freqs):
        with open(TAPE_FILE, 'a') as file:
            for freq in peak_freqs:
                if freq > 0:
                    file.write(f"{freq:.2f} Hz\n")

    def clean_up(self):
        self.audio.terminate()