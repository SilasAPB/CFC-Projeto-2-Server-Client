import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import time


# Identificar o acorde com base nos picos detectados
def identificar_acorde(freqs_top_peaks, frequencias):
    menor_diferenca = float('inf')
    acorde_identificado = None

    for acorde, valores in frequencias.items():
        # Calcular a soma das diferenças absolutas entre os picos e as frequências do acorde
        diferenca = sum(min(abs(freq - valor) for valor in valores) for freq in freqs_top_peaks)
        
        # Verificar se essa soma é a menor encontrada
        if diferenca < menor_diferenca:
            menor_diferenca = diferenca
            acorde_identificado = acorde

    return acorde_identificado

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
    plt.subplot(1, 3, 1)
    plt.plot(t, sinal)
    plt.title("Sinal no tempo")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)

    # Plot do espectro de frequência
    plt.subplot(1, 3, 2)
    plt.stem(freqs, magnitude, basefmt=" ")
    plt.title("Transformada de Fourier (FFT)")
    plt.xlabel("Frequência (Hz)")
    plt.ylabel("Magnitude")
    plt.grid(True)


    peaks, _ = find_peaks(magnitude, height=0.05, distance=300)  # Ajuste 'height' e 'distance'

    # Ordenar os picos pela magnitude e selecionar os 3 maiores
    top_peaks = sorted(peaks, key=lambda x: magnitude[x], reverse=True)[:5]

    freqs_top_peaks = freqs[top_peaks][:3]

    acorde = identificar_acorde(freqs_top_peaks, frequencias)

    # Exibir as frequências correspondentes aos 3 maiores picos
    print("Frequências dos 5 maiores picos:", freqs[top_peaks])

    # Opcional: destacar os 3 maiores picos no gráfico
    plt.subplot(1, 3, 3)
    plt.stem(freqs, magnitude, basefmt=" ")
    plt.plot(freqs[top_peaks], magnitude[top_peaks], "r*", label="Top 5 Picos")  # Marcar picos em vermelho
    plt.title("Transformada de Fourier (FFT)")
    plt.xlabel("Frequência (Hz)")
    plt.ylabel("Magnitude")
    plt.xlim(0,2000)
    plt.legend()
    plt.grid(True)

    return acorde


frequencias = {
    1: [523.25, 659.25, 783.99],  # "Dó maior"
    2: [587.33, 698.46, 880.00],  # "Ré menor"
    3: [659.25, 783.99, 987.77],  # "Mi menor"
    4: [698.46, 880.00, 1046.50],  # "Fá maior"
    5: [783.99, 987.77, 1174.66],  # "Sol maior"
    6: [880.00, 1046.50, 1318.51],  # "Lá menor"
    7: [493.88, 587.33, 698.46],  # "Si menor"
}

duracao = 10       # Duração em segundos
amostragem = 44100   # Taxa de amostragem em Hz


# # Gerar um sinal senoidal para teste
# frequencia_teste = 440  # Frequência em Hz
# t = np.linspace(0, duracao, int(amostragem * duracao), endpoint=False)
# audio_teste = 0.5 * np.sin(2 * np.pi * frequencia_teste * t)

# # Processar o sinal simulado
# plot_fft(audio_teste, amostragem)
# plt.show()




# Para gravar, utilize
audio = sd.rec(int(amostragem*duracao), samplerate=amostragem, channels=1)
sd.wait()

audio = audio.flatten()
audio = audio / np.max(np.abs(audio))
acorde_ouvido=plot_fft(audio,amostragem)
print(f"... FIM -- O acorde identificado foi {acorde_ouvido}")
plt.show()
