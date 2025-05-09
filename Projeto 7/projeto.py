import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QLabel, QFileDialog
from PyQt5.QtCore import Qt
import pyqtgraph as pg
from scipy.signal import iirpeak, iirnotch, freqz, TransferFunction
from scipy.io import wavfile
import sounddevice as sd

dicio_q = {
    20: 3,
    32: 2.6,
    64: 2.4,
    125: 2.2,
    250: 2,
    500: 1.7,
    1000: 1.5,
    2000: 1.4,
    4000: 1.3,
    8000: 1.2,
    16000: 1.1,
    20000: 1
}

def filtro_IIR_ordem2(signal, tf):
    # Obtém os coeficientes do numerador e denominador
    b = tf.num  # Coeficientes do numerador
    a = tf.den  # Coeficientes do denominador

    signal = np.array(signal, dtype=np.float64)
    y = np.zeros(len(signal), dtype=np.float64)

    # Inicializa o vetor de saída com zeros
    y = [0] * len(signal)
    
    # print(type(signal))
    # print(len(signal))
    # print(signal[200:210])  # Exibe os primeiros 10 elementos
    # signal = np.concatenate(signal)  #
    # signal = [float(x) for x in signal if isinstance(x, (int, float))]

    
    # Aplica a fórmula do filtro IIR
    for n in range(2, len(signal)):
        y[n] = - (a[1] * y[n-1]) - (a[2] * y[n-2]) + (b[0] * signal[n]) + (b[1] * signal[n-1]) + (b[2] * signal[n-2])
    
    return y

def peaking_eq(f0, gain_db, Q, fs):
    """
    Design a peaking EQ filter.
    
    Parameters:
        f0 : float      # center frequency in Hz
        gain_db : float # gain in dB (+boost, -cut)
        Q : float       # quality factor
        fs : float      # sampling rate in Hz
        
    Returns:
        b, a : filter coefficients
    """
    A = 10**(gain_db / 40)  # amplitude
    omega = 2 * np.pi * f0 / fs
    alpha = np.sin(omega) / (2 * Q)

    b0 = 1 + alpha * A
    b1 = -2 * np.cos(omega)
    b2 = 1 - alpha * A
    a0 = 1 + alpha / A
    a1 = -2 * np.cos(omega)
    a2 = 1 - alpha / A

    b = np.array([b0, b1, b2]) / a0
    a = np.array([a0, a1, a2]) / a0
    return b, a

class EqualizerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Mini Equalizador')
        self.bandas_freq = [20, 32, 64, 125, 250, 500, 1000, 2000,4000,8000,16000, 20000]  # Frequências centrais das bandas (Hz)
        self.sliders = []
        self.labels_db = []
        self.ganhos_db = [0]*len(self.bandas_freq)  # Ganhos iniciais (dB)
        self.fs = 44100  # Frequência de amostragem (Hz)
        self.audio_data = None

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        sliders_layout = QHBoxLayout()
        for i, freq in enumerate(self.bandas_freq):
            vbox = QVBoxLayout()
            freq_label = QLabel(f'{freq} Hz')
            freq_label.setAlignment(Qt.AlignCenter)

            slider = QSlider(Qt.Vertical)
            slider.setMinimum(-10)
            slider.setMaximum(10)
            slider.setTickInterval(1)
            slider.setSingleStep(1)
            slider.setTickPosition(QSlider.TicksBothSides)
            slider.setValue(0)
            slider.valueChanged.connect(self.update_ganhos)

            db_label = QLabel("0 dB")
            db_label.setAlignment(Qt.AlignCenter)

            self.sliders.append(slider)
            self.labels_db.append(db_label)

            vbox.addWidget(freq_label)
            vbox.addWidget(slider)
            vbox.addWidget(db_label)
            sliders_layout.addLayout(vbox)

        layout.addLayout(sliders_layout)

        self.plot_widget = pg.PlotWidget(title="Resposta em Frequência (Diagrama de Bode)")
        self.plot_widget.setLabel('left', 'Magnitude (dB)')
        self.plot_widget.setLabel('bottom', 'Frequência (Hz)')
        self.plot_widget.setLogMode(x=True, y=False)
        layout.addWidget(self.plot_widget)

        button_layout = QHBoxLayout()

        load_button = QPushButton('Carregar Áudio')
        load_button.clicked.connect(self.load_audio)
        button_layout.addWidget(load_button)

        plot_button = QPushButton('Plotar Bode')
        plot_button.clicked.connect(self.plot_bode)
        button_layout.addWidget(plot_button)

        apply_button = QPushButton('Aplicar Equalizador e Tocar')
        apply_button.clicked.connect(self.apply_equalizer)
        button_layout.addWidget(apply_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def update_ganhos(self):
        self.ganhos_db = [slider.value() for slider in self.sliders]
        for label, ganho in zip(self.labels_db, self.ganhos_db):
            label.setText(f"{ganho} dB")

    def plot_bode(self):
        w = np.logspace(np.log10(20), np.log10(20000), 1000)
        w_norm = w / (self.fs / 2)

        h_total = np.ones_like(w, dtype=np.complex128)

        for ganho_db, fc in zip(self.ganhos_db, self.bandas_freq):
            if ganho_db != 0:
                if ganho_db > 0:
                    b, a = peaking_eq(fc, ganho_db, Q=dicio_q[fc], fs=self.fs)
                    _, h = freqz(b, a, worN=w, fs=self.fs)
                    ganho_linear = 10**(ganho_db / 20)
                    h_total *= (h * ganho_linear) + (1 - ganho_linear)
                else:
                    b, a = peaking_eq(fc, ganho_db, Q=dicio_q[fc], fs=self.fs)
                    _, h = freqz(b, a, worN=w, fs=self.fs)
                    ganho_linear = 10**(ganho_db / 20)
                    h_total *= (h * ganho_linear) + (1 - ganho_linear)

        magnitude_db = 20 * np.log10(np.abs(h_total) + 1e-6)

        self.plot_widget.clear()
        self.plot_widget.plot(w, magnitude_db, pen='b')

    def load_audio(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Abrir arquivo WAV", "", "Arquivo WAV (*.wav)", options=options)
        if fileName:
            self.fs, data = wavfile.read(fileName)
            if len(data.shape) > 1:  # Verifica se é estéreo
                data = data[:, 0]  # Seleciona o canal esquerdo (coluna 0)
            if data.dtype == np.int16:
                data = data.astype(np.float32) / 32768.0
            self.audio_data = data
        
            
        print(self.audio_data) 
        print(type(self.audio_data))
        print(len(self.audio_data))

    def apply_equalizer(self):
        if self.audio_data is None:
            return

        output = np.copy(self.audio_data)
        
        for ganho_db, fc in zip(self.ganhos_db, self.bandas_freq):
            if ganho_db != 0:
                if ganho_db > 0:
                    b, a = peaking_eq(fc, ganho_db, Q=dicio_q[fc], fs=self.fs)
                    tf = TransferFunction(b, a, dt=1/self.fs)
                    output = filtro_IIR_ordem2(output, tf)
                else:
                    b, a = peaking_eq(fc, ganho_db, Q=dicio_q[fc], fs=self.fs)
                    tf = TransferFunction(b, a, dt=1/self.fs)
                    output = filtro_IIR_ordem2(output, tf)
        

        #q baixo altas frequencias , alto -> baixo
        # max_val = np.max(np.abs(output))
        # if max_val > 1e-6:
        #     output = output / max_val

        sd.play(output, self.fs)
        sd.wait()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EqualizerApp()
    window.show()
    sys.exit(app.exec_())