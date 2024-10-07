import sounddevice as sd
import wave
import numpy as np
import threading

# Audio settings
OUTPUT_FILE = 'path/translation_input.wav'
FORMAT = 'float32'
CHANNELS = 1
RATE = 48000 
CHUNK = 1024  # Process in small chunks to allow checking for input

# Variable to control the recording loop
stop_recording = False

def wait_for_enter():
    global stop_recording
    input()
    stop_recording = True

print("Press Enter to start recording.")
input()
print("Recording... Press Enter to stop.")

# Start a separate thread to listen for the Enter key
thread = threading.Thread(target=wait_for_enter)
thread.start()

# List to store recorded chunks
frames = []

# Continuously record audio in chunks
with sd.InputStream(samplerate=RATE, channels=CHANNELS, dtype=FORMAT, blocksize=CHUNK) as stream:
    while not stop_recording:
        data, _ = stream.read(CHUNK)
        frames.append(data)

# Convert recorded frames to a numpy array
audio_data = np.concatenate(frames)

# Convert from float32 to int16 for WAV format
audio_data = np.int16(audio_data * 32767)

# Save the audio to a .wav file
with wave.open(OUTPUT_FILE, 'wb') as wave_file:
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(2)  # 2 bytes for int16
    wave_file.setframerate(RATE)
    wave_file.writeframes(audio_data.tobytes())

print(f"Recording saved to '{OUTPUT_FILE}'.")






