#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import numpy as np

from random import random
import numpy as np
import struct
import sys
import os
from threading import Thread

from projeto3_generator import DatagramGenerator

serialName ="COM5"
PLMAX = 70
TIMEOUT=3

def main():
    generator = DatagramGenerator()
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)

        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        
        print("Abriu a comunicação")
        file = r'C:\Users\yaman\OneDrive - Insper - Institudo de Ensino e Pesquisa\2025.1\Camadas\Aula1\data\bola_lowres.jpg'
        image = open(file,'rb')
        
        len_image = os.path.getsize(file)
        n_pacotes = len_image/PLMAX if not len_image%PLMAX else (len_image//PLMAX)+1
        print("Enviando byte de sacrifício:")
        time.sleep(.2)
        com1.sendData(b'00')
        time.sleep(1)
        
        # --------------------------- #
        #          HANDSHAKE          #
        # --------------------------- #
        print('Efetuando Handshake:')
        handshake = False
        while not handshake:
            txBuffer = generator.generate_header(1,id_servidor=1,n_pacotes=n_pacotes)
            com1.sendData(txBuffer)
            time.sleep(0.2)
            
            start = time.time()
            while(com1.rx.getBufferLen() < 12):
                time.sleep(0.05)
                if (time.time()-start >= TIMEOUT):
                    res = input('Servidor inativo. Tentar novamente? S/N > ')
                    if res.lower() == 's': continue
                    else:
                        com1.disable()
                        sys.exit()
                    
            rxBuffer = com1.rx.getBuffer(12)
            
            response = generator.decode_header(com1.rx.getBuffer(12))
            if response["type"]==2:
                handshake = True        
            
            
        # --------------------------- #
        #       Envio de Pacotes      #
        # --------------------------- #
        print('HANDSHAKE ESTABELECIDO\nENVIANDO PACOTES')
        n_pacote = 0
        while n_pacote <= n_pacotes:
            txBuffer = generator.generate_header(
                3,
                id_pacote=n_pacote,
                n_pacotes=n_pacotes,
                tamanho_pl=70)
            com1.sendData(txBuffer)
            time.sleep(0.2)
            
            start = time.time()
            while(com1.rx.getBufferLen() < 12):
                time.sleep(0.05)
                if (time.time()-start >= TIMEOUT):
                    res = input('Servidor inativo. Tentar novamente? S/N > ')
                    if res.lower() == 's': continue
                    else: sys.exit()
                    
            rxBuffer = com1.rx.getBuffer(12)
            
            response = generator.decode_header(com1.rx.getBuffer(12))
            if response["type"]==2:
                handshake = True
        n_pacote = 1
        while True:
            print('Efetuando Handshake:')
            txBuffer = generator.generate_header(1,id_servidor=1,n_pacotes=n_pacotes)
            com1.sendData(txBuffer)
            response = generator.decode_header(com1.rx.getBuffer(12))
            time.sleep(0.2)
        
        # time.sleep(.2)
        
        # start = time.time()
        # TIMEOUT = 5
        # while(com1.rx.getBufferLen() < 4):
        #     time.sleep(0.05)
        #     if (time.time()-start >= TIMEOUT):
        #         print("ERRO! Tempo de espera excedido.")
        #         com1.disable()
        #         sys.exit()
        # rxBuffer = com1.rx.getBuffer(4)
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
