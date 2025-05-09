from scipy.signal import chirp
import numpy as np
from scipy.io.wavfile import write

fs = 44100  # Frequência de amostragem
t = np.linspace(0, 8, fs*8)  # 5 segundos
signal = chirp(t, f0=20, f1=20000, t1=8, method="log")

# Normalizar para int16
signal_int16 = np.int16(signal / np.max(np.abs(signal)) * 32767)

write('sweep.wav', fs, signal_int16)
