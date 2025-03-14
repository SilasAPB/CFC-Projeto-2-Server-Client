from struct import pack,unpack
TYPE_FEATURES = {
        1:['id_servidor','n_pacotes'],
        3:['id_pacote','n_pacotes','tamanho_pl','crc16'],
        4:['id_pacote'],
        6:['id_pacote'],
}

DATATYPES = {
        'tipo':'B',
        'id_servidor':'B',
        'id_pacote':'I',
        'n_pacotes':'I',
        'tamanho_pl':'B',
        'crc16':'H'
}

DATASIZES = {'B':1,'I':4,'H':2}

TYPE_LEN = 6

HEADER_SIZE = 12

def encode(
    type_id:int,
    **kwargs) -> bytearray:
    """
        ## Tipos de mensagens:
        **Tipo 1:** [tipo<1> , id_servidor<1> , n_pacotes<4>]
        - Mensagem de solicitação de transmissão
        
        **Tipo 2:** [tipo<1>]
        - Mensagem de confirmação de transmissão
        
        **Tipo 3:** [tipo<1> , id_pacote<4> , n_pacotes<4> , tamanho_pl<1> , crc16<2>]
        - Pacote de dados
        
        **Tipo 4:** [tipo<1> , id_pacote<4>]
        - Mensagem de confirmação de pacote
        
        **Tipo 5:** [tipo<1>]
        - Mensagem de timeout
        
        **Tipo 6:** [tipo<1> , id_pacote<4>]
        - Mensagem de erro de pacote
    """
    
    bytestring = b''+pack('!B',type_id)
    
    if type_id in TYPE_FEATURES.keys():
        for feature in TYPE_FEATURES[type_id]:
            try:
                bytestring += pack(
                    f'!{DATATYPES[feature]}',
                    kwargs[feature])
            except KeyError:
                print("Parâmetro {feature} não encontrado\nParâmetros necessários:\n- {params}".format(
                    feature=feature,params='\n- '.join(TYPE_FEATURES[type_id])))
                raise(KeyError("Parâmetro {feature} não encontrado. Parâmetros necessários: {params}.".format(
                    feature=feature,params=', '.join(TYPE_FEATURES[type_id]))))

    str_size = len(bytestring)
    bytestring += bytearray(HEADER_SIZE-str_size)
    
    if type_id > TYPE_LEN or type_id<=0:
        return bytearray(HEADER_SIZE)
    
    return bytestring
 
def decode(header:bytes) -> dict:
    res = {'type':header[0]}

    index = 1
    if res['type'] in TYPE_FEATURES.keys():
        for feature in TYPE_FEATURES[res['type']]:
            datatype = DATATYPES[feature]
            slice = header[index:index+DATASIZES[datatype]] if DATASIZES[datatype]>1 else header[index].to_bytes()
            res[feature] = unpack(
                f'!{datatype}',
                slice
            )[0]
            index += DATASIZES[datatype]
    
    if res['type'] > TYPE_LEN or res['type']<=0:
        return {'error': 'Header type not listed'}
    
    return res