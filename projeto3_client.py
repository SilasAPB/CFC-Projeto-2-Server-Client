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

from projeto3_generator import DatagramGenerator

serialName ="COM5"

def main():
    generator = DatagramGenerator()
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)

        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")
        
        print("Enviando byte de sacrifício:")
        time.sleep(.2)
        com1.sendData(b'00')
        time.sleep(1)
        
        
        txBuffer = generator.generate_header(1,{'id_servidor':1,'n_pacotes':3})
        print(txBuffer)      
        
        com1.sendData(txBuffer)
        
        txSize = com1.tx.getStatus()
        print('enviou = {}' .format(txSize))
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
