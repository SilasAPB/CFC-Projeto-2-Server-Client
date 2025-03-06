#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################

from enlace import *
import projeto3_generator
import time
import struct
import numpy as np

from random import random
import numpy as np

serialName ="COM9"

def main():
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)

        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        receive_list=[]
        lista_unpack=[]
        numero_pacotes=0
        id_pacote=0

        print("esperando 1 byte de sacrifício")
        rxBuffer, nRx = com1.getData(1) #FICA EM LOOPING ESPERANDO A MENSAGEM
        com1.rx.clearBuffer()

        time.sleep(.1)
        recebido, recebido_size=com1.getData(12)
        print("recebeu {} bytes" .format(len(recebido)))
        byte=decoder(recebido)
        print(byte)

        
        
        
        # sum=0
        # i=0
        # while i<byte[0]:
        #     recebido, recebido_size=com1.getData(4)
        #     number=struct.unpack("!f",recebido)
        #     numbers_list.append(number[0])
        #     sum+=number[0]
        #     print(f"a lista atual de número é {numbers_list}")
        #     i+=1
        # # Encerra comunicação
        # print(f"a soma final foi {sum}")
        # com1.sendData(struct.pack('!f',sum))
        # print("-------------------------")
        # print("Comunicação encerrada")
        # print("-------------------------")
        # com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
