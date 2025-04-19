import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import time



def plot_fft(sinal, fs):
    """
    Plota o gráfico da Transformada de Fourier (FFT) de um sinal.

    Parâmetros:
    - sinal: lista ou array com os valores do sinal no tempo
    - fs: taxa de amostragem em Hz
    """
    # Converter sinal para array NumPy
    sinal = np.array(sinal)
    
    # Número de amostras e vetor de tempo
    N = len(sinal)
    t = np.arange(N) / fs

    # FFT e cálculo da magnitude
    fft_result = np.fft.fft(sinal)
    freqs = np.fft.fftfreq(N, d=1/fs)
    magnitude = np.abs(fft_result)

    # Manter só metade do espectro (frequências positivas)
    half_N = N // 2
    freqs = freqs[:half_N]
    magnitude = magnitude[:half_N]

    # Plot do sinal no tempo (opcional)
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.plot(t, sinal)
    plt.title("Sinal no tempo")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)

    # Plot do espectro de frequência
    plt.subplot(1, 2, 2)
    plt.stem(freqs, magnitude, basefmt=" ")
    plt.title("Transformada de Fourier (FFT)")
    plt.xlabel("Frequência (Hz)")
    plt.ylabel("Magnitude")
    plt.xlim(0,2500)
    plt.grid(True)


acorde=int(input("Qual acorde você quer executar? "))

frequencias = {
    1: [523.25, 659.25, 783.99],  # "Dó maior"
    2: [587.33, 698.46, 880.00],  # "Ré menor"
    3: [659.25, 783.99, 987.77],  # "Mi menor"
    4: [698.46, 880.00, 1046.50],  # "Fá maior"
    5: [783.99, 987.77, 1174.66],  # "Sol maior"
    6: [880.00, 1046.50, 1318.51],  # "Lá menor"
    7: [493.88, 587.33, 698.46],  # "Si menor"
}

# Parâmetros da senoide
frequencia_escolhida = frequencias[acorde] # Frequência em Hz (Dó central)
duracao = 10        # Duração em segundos
amostragem = 44100   # Taxa de amostragem em Hz

for frequencia in frequencia_escolhida:
    duracao_cada=duracao/3
    # Gerar a senoide
    t = np.linspace(0, duracao_cada, int(amostragem * duracao_cada), endpoint=False)  # Vetor de tempo
    senoide = 0.5 * np.sin(2 * np.pi * frequencia * t)  # Senoide com amplitude de 0.5

    # # Processar o sinal simulado
    # plot_fft(senoide, amostragem)
    # plt.show()


    # Tocar a senoide
    sd.play(senoide, amostragem)
    sd.wait()
    time.sleep(0.3)


t = np.linspace(0, duracao, int(amostragem * duracao), endpoint=False)  # Vetor de tempo

# Gerar a soma das senoides para as 3 frequências do acorde
senoide = sum(0.5 * np.sin(2 * np.pi * frequencia * t) for frequencia in frequencia_escolhida)

# Normalizar o sinal para evitar clipping
senoide = senoide / np.max(np.abs(senoide))

# Plotar o sinal no tempo
plot_fft(senoide, amostragem)
plt.show()
