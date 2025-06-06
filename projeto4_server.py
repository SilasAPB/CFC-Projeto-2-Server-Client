#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################

from enlace import *
from projeto3_generator import DatagramGenerator
from crc import Calculator, Crc16
import logging
import time
import struct
import numpy as np
from datetime import datetime

from random import random
import numpy as np
serialName ="COM7"
generator=DatagramGenerator()

def geral_log(logger,head,tamanho,tipo):
    dic={0:"receb",
         1:"envio"
        }
    #Pega as info de tempo
    agora = datetime.now()
    saida = agora.strftime("%d/%m/%Y %H:%M:%S.") + f"{agora.microsecond // 1000:03d}"
    #Definindo a mensagem
    msg=f"{saida} / {dic[tipo]} / {head['type']} / {tamanho}"
    
    if head['type']==3:
        id_atual=head['id_pacote']
        n_pacotes=head['n_pacotes']
        crc=head['crc16']
        msg += f' / {id_atual} / {n_pacotes} / {crc}'

    logger.info(msg)


def main():
    checksum = Calculator(Crc16.DNP,optimized=True)
    try:
        logger=logging.getLogger("Projeto4_Server")
        logging.basicConfig(filename='project4.log', level=logging.INFO)
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        imageW="./img/paiolcopy.jpg"

        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        lista_unpack=[]

        print("esperando 1 byte de sacrifício")
        rxBuffer, nRx = com1.getData(1) #FICA EM LOOPING ESPERANDO A MENSAGEM
        com1.rx.clearBuffer()
        
        #RECEBE O HEADER
        time.sleep(.1)
        recebido, recebido_size=com1.getData(12)
        tamanho=len(recebido)
        print("recebeu {} bytes" .format(len(recebido)))
        head=generator.decode_header(recebido)
        print(head)
        geral_log(logger,head,tamanho,0)
        numPckg=head['n_pacotes']

        #MANDA O ACEITE PARA O CLIENT
        aceite=generator.generate_header(tipo=2)
        tamanho_aceite=len(aceite)
        aceite_head=generator.decode_header(aceite)
        geral_log(logger,aceite_head,tamanho_aceite,1)
        com1.sendData(aceite)

        print(com1.rx.getBufferLen())
        deu_bom=False

        #COMEÇA A CONTAR OS PACOTES
        cont=0
        while cont<numPckg:
            timer2=time.time()
            while time.time()-timer2<=20:
                timer1=time.time()
                while time.time()-timer1<=2:
                    if (com1.rx.getBufferLen()>=12):
                        try:
                            recebido_head, recebido_size=com1.getData(12)
                            print(recebido_head)
                            head=generator.decode_header(recebido_head)
                            print(head)
                            print(f"PACOTE DE ID {head['id_pacote']} LIDO COM SUCESSO")
                            tamanho_corpo=head['tamanho_pl']
                            recebido_corpo, recebido_size=com1.getData(tamanho_corpo)
                            
                            print(head["id_pacote"],cont)
                            recebido_eop,recebido_size=com1.getData(3)
                            # if not checksum.verify(recebido_corpo,head['crc16']):
                            if not checksum.verify(recebido_corpo,head['crc16'] if head['id_pacote']!= 3 else 1):
                                print("Checksum errado!")
                                raise ValueError("Checksum errado")
                            geral_log(logger,head,(len(head)+tamanho_corpo+3),0)
                        except:
                            aceite=generator.generate_header(tipo=6,id_pacote=cont)
                            tamanho_aceite=len(aceite)
                            aceite_head=generator.decode_header(aceite)
                            geral_log(logger,aceite_head,tamanho_aceite,1)
                            com1.sendData(aceite)
                            break

                        if (recebido_eop==generator.EOP()) and (cont==head['id_pacote']):
                            print("----- PACOTE LIDO COM SUCESSO -----")
                            lista_unpack.append(recebido_corpo)
                            aceite=generator.generate_header(tipo=4,id_pacote=head["id_pacote"])
                            tamanho_aceite=len(aceite)
                            aceite_head=generator.decode_header(aceite)
                            geral_log(logger,aceite_head,tamanho_aceite,1)
                            com1.sendData(aceite)
                            # cont+=1
                            cont+=1 if cont!=3 else 3
                        else:
                            print("----- ERRO ENCONTRADO -----")
                            aceite=generator.generate_header(tipo=6,id_pacote=cont)
                            tamanho_aceite=len(aceite)
                            aceite_head=generator.decode_header(aceite)
                            geral_log(logger,aceite_head,tamanho_aceite,1)
                            com1.sendData(aceite)
                    else:
                        time.sleep(0.5)
            
        if cont<numPckg:
            aceite=generator.generate_header(tipo=5,id_pacote=cont)
            tamanho_aceite=len(aceite)
            aceite_head=generator.decode_header(aceite)
            geral_log(logger,aceite_head,tamanho_aceite,1)
            com1.sendData(aceite)
            com1.disable()
        else:
            deu_bom=True

        if deu_bom:
            #SALVANDO CADA PACOTE
            imagem=b"".join(lista_unpack)
            print(imagem)
            f= open(imageW, "+wb")
            f.write(imagem)
            f.close()
            com1.disable()
                
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
