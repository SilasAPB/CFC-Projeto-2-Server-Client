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

serialName ="COM5"

def main():
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
        
        k = 5 # Numero de números gerados
        numeros = [round((random()*5), 6) for i in range(0,k)]
        print(f"Os seguintes {k} números foram gerados:\n{numeros}")
        txBuffer = [bytearray(struct.pack("!f",n)) for n in numeros]
        # txBuffer[2] = bytearray(b'\ff')
       
        print(f"Enviando quantidade de números: {k}")
        time.sleep(.2)
        com1.sendData(struct.pack('!B',k))
        time.sleep(1)
        
        
        for i in range(len(numeros)):
            print(f'Enviando {numeros[i]:}')
            print("meu array de bytes tem tamanho {}" .format(len(txBuffer[i])))

            com1.sendData(txBuffer[i])
        
            txSize = com1.tx.getStatus()
            print('enviou = {}' .format(txSize))
            time.sleep(.2)
        
        start = time.time()
        TIMEOUT = 5
        while(com1.rx.getBufferLen() < 4):
            time.sleep(0.05)
            if (time.time()-start >= TIMEOUT):
                print("ERRO! Tempo de espera excedido.")
                com1.disable()
                sys.exit()
        rxBuffer = com1.rx.getBuffer(4)

        correto = round(sum(numeros),6)
        
        soma = round(struct.unpack("!f",rxBuffer)[0],6)
        
        print(f'A soma dos números é {correto}')
        print(f'A soma recebida é {soma}')
        
        
        err = soma-correto
        
        print(f'Erro de transmissão: {err}')
        if abs(err) > 0.0000001:
            print("Erro de transmissão alto demais!")
        
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
