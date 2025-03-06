#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################

from enlace import *
from projeto3_generator import DatagramGenerator
import time
import struct
import numpy as np

from random import random
import numpy as np

serialName ="COM9"

generator=DatagramGenerator()

def main():
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)

        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        lista_unpack=[]

        print("esperando 1 byte de sacrifício")
        rxBuffer, nRx = com1.getData(1) #FICA EM LOOPING ESPERANDO A MENSAGEM
        com1.rx.clearBuffer()
        
        #RECEBE O HEADER
        time.sleep(.1)
        recebido, recebido_size=com1.getData(12)
        print("recebeu {} bytes" .format(len(recebido)))
        head=generator.decode_header(recebido)
        print(head)
        numPckg=head['n_pacotes']

        #MANDA O ACEITE PARA O CLIENT
        aceite=generator.generate_header(tipo=2)
        print(aceite)
        com1.sendData(aceite)

        print(com1.rx.getBufferLen())

        #COMEÇA A CONTAR OS PACOTES
        cont=0
        while cont<=numPckg:
            timer1=time.time()
            timer2=time.time()
            recebido_head, recebido_size=com1.getData(12)
            head=generator.decode_header(recebido_head)
            print(head)
            if cont==head['id_pacote']:
                tamanho_corpo=head['tamanho_pl']
                recebido_corpo, recebido_size=com1.getData(tamanho_corpo)
                recebido_eop,recebido_size=com1.getData(3)
                if recebido_eop=="pig":
                    pass

            pass

        
        
        
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
