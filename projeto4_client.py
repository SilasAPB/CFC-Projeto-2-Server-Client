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
from crc import Calculator, Crc16

import logging
logger = logging.getLogger('p4_client')
logging.basicConfig(filename='p4_client.log', level=logging.INFO,format='%(asctime)s | %(message)s')

serialName ="COM5"
PLMAX = 70
TIMEOUT = 5

def split_in_chunks(list,size):
    total = len(list)
    chunks = []
    i = 0
    while i+size<total:
        chunks.append(list[i:i+size])
        i+=size
    chunks.append(list[i:])
    return chunks,len(chunks)

def main():
    generator = DatagramGenerator()
    checksum = Calculator(Crc16.DNP,optimized=True)
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)

        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        
        print("Abriu a comunicação")
        file = r'C:\Users\yaman\OneDrive - Insper - Institudo de Ensino e Pesquisa\2025.1\Camadas\Aula1\data\bola_lowres.jpg'
        image = open(file,'rb').read()
        pacotes,total_pacotes = split_in_chunks(image,PLMAX)
        
        
        
        # --------------------------- #
        #          HANDSHAKE          #
        # --------------------------- #
        handshake = False
        while not handshake:
            print("Enviando byte de sacrifício:")
            time.sleep(.2)
            com1.sendData(b'00')
            com1.rx.clearBuffer()
            time.sleep(.5)
            
            print('Efetuando Handshake:')
            txBuffer = generator.generate_header(
                1,
                id_servidor=1,
                n_pacotes=total_pacotes)
            com1.sendData(txBuffer)
            time.sleep(0.2)
            
            active = True
            start = time.time()
            while(com1.rx.getBufferLen() < 12):
                time.sleep(0.05)
                if (time.time()-start >= TIMEOUT):
                    active = False
                    break
                
            if not active:
                res = input('Servidor inativo. Tentar novamente? S/N > ')
                if res.lower() == 's':
                    continue
                else:
                    com1.disable()
                    sys.exit()
            
            response = generator.decode_header(com1.rx.getBuffer(12))
            if response["type"]==2:
                handshake = True     
            
            
        # --------------------------- #
        #       Envio de Pacotes      #
        # --------------------------- #
        print('HANDSHAKE ESTABELECIDO\nENVIANDO PACOTES')
        n_pacote = 0
        while n_pacote < total_pacotes:
            print(f'Enviando pacote [{n_pacote}] | {(n_pacote/total_pacotes)*100:.2f}%',end='\r')
            crc16 = checksum.checksum(pacotes[n_pacote])
            txBuffer = generator.generate_header(
                3,
                id_pacote=n_pacote, # if n_pacote != 3 else 20
                n_pacotes=total_pacotes,
                tamanho_pl = len(pacotes[n_pacote]),
                crc16 = crc16)
            
            tries = 5
            while tries:
                tries-=1
                
                com1.sendData(txBuffer)            # Enviando Header
                time.sleep(0.05)
                
                com1.sendData(pacotes[n_pacote])   # Enviando Payload
                time.sleep(0.05)
                
                com1.sendData(generator.EOP())     # Enviando EOP
                com1.rx.clearBuffer()
                time.sleep(0.05)
                logger.info('envio | 3 | {tamanho} | {pacote} | {total} | {crc}'.format(
                    tamanho=len(txBuffer)+len(pacotes[n_pacote])+2,
                    pacote=n_pacote,
                    total=total_pacotes,
                    crc=crc16
                ))
                
                
                start = time.time()
                while(com1.rx.getBufferLen() < 12):
                    if (time.time()-start >= TIMEOUT):
                        if tries:
                            print(f"\nTempo esgotado para recebimento de resposta do servidor. Tentando novamente. [{tries}] restantes")
                            com1.rx.clearBuffer()
                            break
                        else:
                            print(f"\nTentativas esgotadas. Enviando header de timeout e encerrando comunicação.")
                            txBuffer = generator.generate_header(5)
                            logger.info('envio | 5 | {tamanho}'.format(
                                tamanho=len(txBuffer)
                            ))
                            com1.sendData(txBuffer)
                            time.sleep(.05)
                            com1.disable()
                            sys.exit()
                    
                    time.sleep(0.01)

                if com1.rx.getBufferLen():
                    break

            response = generator.decode_header(com1.rx.getBuffer(12))
            if 'error' in response.keys():
                logger.info('recebido | 0 | 12')
            
            logger.info('recebido | {tipo} | {tamanho}'.format(
                    tipo=response['type'],
                    tamanho=12
                ))
            if response["type"]==4:
                n_pacote = response['id_pacote']+1
            if response["type"]==6:
                print(f"\nErro no pacote {response['id_pacote']}. Tentando novamente")
                n_pacote = response["id_pacote"]
        
        print("\n-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print('Erro:',erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
