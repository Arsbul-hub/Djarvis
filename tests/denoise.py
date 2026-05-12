import noisereduce as nr
import soundfile as sf
import matplotlib.pyplot as plt

# Load audio file (returns waveform and sample rate)
audio, sample_rate = sf.read("./g1.wav")

# Plot the original audio (time domain)
plt.figure(figsize=(10, 4))
plt.plot(audio)
plt.title("Original Noisy Audio")
plt.xlabel("Time (samples)")
plt.ylabel("Amplitude")
plt.show()

# Extract noise profile (use the first 0.5 seconds as noise-only)
noise_duration = 0.5  # seconds
noise_sample = audio[:int(noise_duration * sample_rate)]

# Denoise the audio
print(type(noise_sample))
denoised_audio = nr.reduce_noise(
    y=audio,
    # y_noise=noise_sample,
    sr=44100
)

# Save the denoised audio
sf.write("denoised_audio_noisereduce.wav", denoised_audio, sample_rate)

# Plot denoised audio
plt.figure(figsize=(10, 4))
plt.plot(denoised_audio)
plt.title("Denoised Audio (noisereduce)")
plt.xlabel("Time (samples)")
plt.ylabel("Amplitude")
plt.show()