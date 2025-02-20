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
 
# SOURCE: https://www.geeksforgeeks.org/python-program-to-represent-floating-number-as-hexadecimal-by-ieee-754-standard/
# def float_bin(my_number, places = 3): 
#     my_whole, my_dec = str(my_number).split(".")
#     my_whole = int(my_whole)
#     res = (str(bin(my_whole))+".").replace('0b','')
 
#     for x in range(places):
#         my_dec = str('0.')+str(my_dec)
#         temp = '%1.20f' %(float(my_dec)*2)
#         my_whole, my_dec = temp.split(".")
#         res += my_whole
#     return res

# def IEEE754(n) : 
#     # identifying whether the number
#     # is positive or negative
#     sign = 0
#     if n < 0 : 
#         sign = 1
#         n = n * (-1) 
#     p = 30
#     # convert float to binary
#     dec = float_bin (n, places = p)
 
#     dotPlace = dec.find('.')
#     onePlace = dec.find('1')
#     # finding the mantissa
#     if onePlace > dotPlace:
#         dec = dec.replace(".","")
#         onePlace -= 1
#         dotPlace -= 1
#     elif onePlace < dotPlace:
#         dec = dec.replace(".","")
#         dotPlace -= 1
#     mantissa = dec[onePlace+1:]
 
#     # calculating the exponent(E)
#     exponent = dotPlace - onePlace
#     exponent_bits = exponent + 127
 
#     # converting the exponent from
#     # decimal to binary
#     exponent_bits = bin(exponent_bits).replace("0b",'') 
 
#     mantissa = mantissa[0:23]
 
#     # the IEEE754 notation in binary     
#     final = str(sign) + exponent_bits.zfill(8) + mantissa
#     hstr = '0x%0*X' %((len(final) + 3) // 4, int(final, 2)) 
#     return hstr

from random import random
import numpy as np

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
        
        k = 5 # Numero de números gerados
        numeros = [round(random(),6) for i in range(0,k)]
        print(f"Os seguintes {k} números foram gerados:\n{numeros}")
        txBuffer = np.asarray(numeros)
       
        print("meu array de bytes tem tamanho {}" .format(len(''.join(txBuffer))))


        #finalmente vamos transmitir os todos. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        print("A transmissão irá começar!")
        #tente entender como o método send funciona!
        #Cuidado! Apenas trasmita arrays de bytes!    
        com1.sendData(txBuffer)  #as array apenas como boa pratica para casos de ter uma outra forma de dados
          
        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # O método não deve estar fincionando quando usado como abaixo. deve estar retornando zero. Tente entender como esse método funciona e faça-o funcionar.
        txSize = com1.tx.getStatus()
        print('enviou = {}' .format(txSize))
        
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX

        #print um aviso de que a recepção vai começar.
        print("a recepção vai começar")
        
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        print(com1.rx.buffer)
        #Veja o que faz a funcao do enlaceRX  getBufferLen
      
        #acesso aos bytes recebidos
        txLen = len(txBuffer)
        rxBuffer, nRx = com1.getData(txLen)
        print("recebeu {} bytes" .format(len(rxBuffer)))
    
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
