from struct import pack,unpack

class DatagramGenerator:
    """
    ## Tipos de mensagens:
    **Tipo 1:** [tipo<1> , n_servidor<1> , n_pacotes<4>]
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
    def __init__(self):
        self.tipos = {
            1:self.type1
        }

    def generate_header(self,
        tipo:int,
        configs:dict) -> bytearray:
        header = bytearray(10)
        header[0] = tipo
        
        if tipo in self.tipos.keys():
            header = self.tipos[tipo](header,configs)
        
        return header
    
    def type1(header:bytearray, configs):
        bytestring = b''
        bytestring += (
            header[0].to_bytes()+                # 1byte
            pack('!B',configs['id_servidor'])+   # 1byte
            pack('!I',configs['n_pacotes'])+     # 4bytes
            bytearray(6))                        # 6bytes
        
        return bytestring
    
    
    def generate_payload(self,
        data) -> bytearray:
        pass