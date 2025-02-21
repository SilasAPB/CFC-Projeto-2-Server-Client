import struct

def datagram_generator(
    tipo:int,
    configs:dict,
    payload:bytearray) -> bytearray:
    """
    **Tipo 1:** [n_servidor,n_pacotes]
    
    **Tipo 2:** []
    
    **Tipo 3:** [id_pacote,n_pacotes,tamanho_pl]
    """
    
    pass