from struct import pack,unpack
import headers
        
        

class DatagramGenerator:
    def __init__(self):
        pass

    def generate_header(self,
        tipo:int,
        **kwargs) -> bytearray:
        """
        ## Tipos de mensagens:
        **Tipo 1:** [tipo<1> , id_servidor<1> , n_pacotes<4>]
        - Mensagem de solicitação de transmissão
        
        **Tipo 2:** [tipo<1>]
        - Mensagem de confirmação de transmissão
        
        **Tipo 3:** [tipo<1> , id_pacote<4> , n_pacotes<4> , tamanho_pl<1>]
        - Pacote de dados
        
        **Tipo 4:** [tipo<1> , id_pacote<4>]
        - Mensagem de confirmação de pacote
        
        **Tipo 5:** [tipo<1>]
        - Mensagem de timeout
        
        **Tipo 6:** [tipo<1> , id_pacote<4>]
        - Mensagem de erro de pacote
        """
        
        return headers.encode(tipo,**kwargs)
    
    def decode_header(self,header:bytes):
        return headers.decode(header)
        
    def generate_payload(self,
        data) -> bytearray:
        pass
    
    def EOP(self): return b'\f\f\f'
    
def main():
    generator = DatagramGenerator()
    header = generator.generate_header(1,id_servidor=1,n_pacotes=3)
    print(header)
    decode = generator.decode_header(header)
    print(decode)
    
if __name__=='__main__':
    main()
    