import struct

class TFTPMessage:
    def __init__(self, opcode):
        self.opcode = opcode

    def pack(self):
        return struct.pack('!H', self.opcode)


class RRQMessage(TFTPMessage):
    def __init__(self, mode='octet'):
        super().__init__(1)
        self.filename = ""
        self.mode = mode

    def pack(self, filename):
        self.filename = filename
        packet = struct.pack('!H{}sB5sB'.format(len(self.filename)), 1, self.filename.encode(), 0, b'octet', 0)
        return packet

    def is_rrq(self, data):
        is_rrq = True if data[0] == 0 and data[1] == self.opcode else False
        return is_rrq


class WRQMessage(TFTPMessage):
    def __init__(self, mode='octet'):
        super().__init__(2)
        self.filename = ""
        self.mode = mode

    def pack(self, filename):
        self.filename = filename
        packet = struct.pack('!H{}sB5sB'.format(len(self.filename)), 2, self.filename.encode(), 0, b'octet', 0)
        return packet

    def is_wrq(self, data):
        is_wrq = True if data[0] == 0 and data[1] == self.opcode else False
        return is_wrq

class DataMessage(TFTPMessage):
    def __init__(self, block_num=-1, body=b'0'):
        super().__init__(3)
        self.block_num = block_num
        self.body = body


    def pack(self, block_number:int, body:bytes):
        
        if len(body)> 512:
            raise ValueError('Corpo deve ter no máximo 512 Bytes')
        packet = struct.pack('!HH{}s'.format(len(body)), self.opcode, block_number, body)
        return packet
    
    def unpack(self, data):

        is_data = True if data[1] == self.opcode else False
        if is_data:

            self.body = data[struct.calcsize('!HH'):]
            self.block_num = struct.unpack_from('!HH',data)[1]
            return is_data
        else: return False

    def get_block_num(self):
        return self.block_num
    
    def get_body(self):
        return self.body



# Classe para representar uma mensagem de ACK
class AckMessage(TFTPMessage):
    #def __init__(self, block_number):
    # O ack vai ser construido sem parametros, apenas opcode
    def __init__(self, block_num=-1):
        super().__init__(4)
        self._block_num=block_num


    def pack(self, block_num):

        # Monta o pacote do ACK quando o servidor 
        ack_packet = struct.pack('!HH', 4, block_num)
        return ack_packet

    
    def unpack(self, packet):
         
        ack_header = b'\x00\x04'
        is_ack = True if packet[0:2] == ack_header else False
        if is_ack:
            #Aqui ele retorna uma Tupla [opccode,block_num]
            # pegando o segundo indice retorna só block_num
            self.block_num = struct.unpack('!HH', packet)[1]
            return is_ack
        else: return False 
    
    def get_block_num(self):
        return self.block_num


# Classe para representar uma mensagem de erro
class ErrorMessage(TFTPMessage):
    def __init__(self, error_code=0, error_message=""):
        super().__init__(5)
        self.error_code = error_code
        self.error_message = error_message

    def pack(self):
        packet = super().pack()
        packet += struct.pack('!H', self.error_code)
        packet += self.error_message.encode('ascii') + b'\x00'
        return packet
    
    def unpack(self,  packet):

        error_header = b'\x00\x05'
        is_error = True if packet[0:2] == error_header else False
        if is_error:
            #Aqui ele retorna uma Tupla [opccode,error_code]
            # pegando o segundo indice retorna só error_code
            self.error_code = struct.unpack('!HH', packet[:4])[1]
            self.error_message = packet[4:-1]
            return is_error
        
        else: return False 

    def get_error_message(self):
        return self.error_message

    def get_error_code(self):
        return self.error_code    
        


