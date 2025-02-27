from struct import pack,unpack

class DatagramGenerator:
    """
    ## Tipos de mensagens:
    **Tipo 1:** [n_servidor,n_pacotes]
    - Mensagem de solicitação de transmissão
    
    **Tipo 2:** []
    - Mensagem de confirmação de transmissão
    
    **Tipo 3:** [id_pacote,n_pacotes,tamanho_pl]
    - Pacote de dados
    
    **Tipo 4:** [id_pacote]
    - Mensagem de confirmação de pacote
    
    **Tipo 5:** []
    - Mensagem de timeout
    
    **Tipo 6:** [id_pacote]
    - Mensagem de erro de pacote
    
    ---
    
    ## Payload Format
    h0 - tipo de mensagem
    h1 - livre
    h2 - livre
    h3 - número total de pacotes do arquivo
    h4 - número do pacote sendo enviado
    h5 - se tipo for handshake: id do arquivo (crie um)
    h5 - se tipo for dados: tamanho do payload
    h6 - pacote solicitado para recomeço quando a erro no envio.
    h7 - último pacote recebido com sucesso.
    h8 - h9 - CRC (Por ora deixe em branco. Fará parte do projeto 5)
    """
    def __init__(self):
        self.tipos = {
            1:self.type1
        }

    def generate_header(self,
        tipo:int,
        configs:dict,
        payload:bytearray) -> bytearray:
        header = bytearray(10)
        header[0] = 1
        
    def generate_payload(self,
        data) -> bytearray:
        pass
    
    def type1(header:bytearray, configs):
        bytestring = b''
        bytestring += (
            header[0].to_bytes()+                # 1byte
            pack('!B',configs['id_servidor'])+   # 1byte
            pack('!I',configs['n_pacotes'])+     # 4bytes
            bytearray(4))                        # 4bytes
        
        return bytestring