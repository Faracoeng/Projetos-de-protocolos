import poller
import socket
import os
import especificacao_pb2

class Protocolo(poller.Callback):
    def __init__(self, ip: str, porta: int):
        self.__handler = None
        self.disable_timeout()
        self.ip = ip
        self.porta_request = int(porta)
        self.porta = int(porta)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', 0))
        poller.Callback.__init__(self, self.sock, 3)
        self.n = 0
        self.filename = ''
        self.file_data = bytearray()

    def handle(self):   
        packet, addr = self.sock.recvfrom(65536)
        self.porta = addr[1]

        message = especificacao_pb2.Mensagem()
        message.ParseFromString(packet)

        if message.HasField('error'):
            error_code = message.error.errorcode
            error_message = especificacao_pb2.ErrorCode.Name(error_code)

            error = f'erro: 0{error_code} / ({error_message})'
            print(error)
            self.disable()
            self.reload_timeout()
            self.disable_timeout()
        else:
            self.__handler(message)

    def handle_timeout(self):
        print('Timeout!')
        self.disable_timeout()
        if (self.__handler == self.handle_rx) or (self.__handler == self.handle_init_tx):
            self.disable()

    def handle_init_tx(self, message):
        self.__handle_tx(True, message)

    def handle_tx(self, message):
        self.__handle_tx(False, message)

    def handle_rx(self, message):

        if message.HasField('data') and message.data.block_n == self.n:
            
            body = message.data.message
            block_num = message.data.block_n

            ack_message = especificacao_pb2.ACK()
            ack_message.block_n = block_num

            # Criando uma instância da mensagem Mensagem com a mensagem ACK
            mensagem = especificacao_pb2.Mensagem()
            mensagem.ack.CopyFrom(ack_message)
            ack_packet = mensagem.SerializeToString()

            self.sock.sendto(ack_packet, (self.ip, self.porta))
            #print(f'Enviado: {ack_packet} para o IP: {self.ip} e porta: {self.porta}')

            if len(body) < 512:
                self.file_data.extend(body)
                arquivo = open(self.filename, 'wb+')
                arquivo.write(self.file_data)
                arquivo.close()
                self.file_data = bytearray()
                self.disable()
                final_rrq_message = f'download do arquivo "{self.filename}" realizado com sucesso'
                print(final_rrq_message)
            else:
                self.n += 1
                self.file_data.extend(body)

            self.disable_timeout()
        elif (message.HasField("data") and message.data.block_n != self.n):
            ack = especificacao_pb2.ACK()
            ack.block_n = self.n
            # Criando uma instância da mensagem Mensagem com a mensagem ACK
            mensagem = especificacao_pb2.Mensagem()
            mensagem.ack.CopyFrom(ack)
            ack_packet = mensagem.SerializeToString()
            self.sock.sendto(ack_packet, (self.ip, self.porta))
            print(f'Enviado novamente: {ack_packet} para o IP: {self.ip} e porta: {self.porta}')

    def handle_finish(self, message):
        if message.HasField('ack'):
            final_wrq_message = f'recebeu o ACK... o upload do arquivo "{self.filename}" foi realizado com sucesso'
            self.file_data = bytearray()
            self.disable_timeout()
            self.disable()
            print(final_wrq_message)

    def tftp_upload(self, filename):
        print('Iniciando upload de arquivo pelo WRQ...')
        if not os.path.exists(filename):
            print(f"O arquivo {filename} não existe!!")
            self.reload_timeout()
            self.disable_timeout()
            self.disable()
        else:
            self.filename = filename
            self.n = 0
            with open(self.filename, 'rb') as arquivo:
                self.file_data = arquivo.read()
            wrq_message = especificacao_pb2.Mensagem()
            wrq_message.wrq.fname = filename
            wrq_message.wrq.mode = especificacao_pb2.Mode.octet
            wrq_packet = wrq_message.SerializeToString()

            self.mef_init(wrq_packet)

    def tftp_download(self, filename):
        print('Iniciando download de arquivo pelo RRQ...')
        if os.path.exists(filename):
            print(f"O arquivo {filename} já existe!!")
            self.reload_timeout()
            self.disable_timeout()
            self.disable()
        else:
            # Criando uma nova Mensagem usando especificacao_pb2.Mensagem().
            rrq_message = especificacao_pb2.Mensagem()
            # Definindo o campo fname da mensagem rrq com o nome do arquivo fornecido.
            rrq_message.rrq.fname = filename
            # Definindo o campo mode da mensagem rrq com especificacao_pb2.Mode.octet.
            rrq_message.rrq.mode = especificacao_pb2.Mode.octet
            # Serializando a mensagem em uma sequência de bytes
            rrq_packet = rrq_message.SerializeToString()

            self.filename = filename
            self.n = 1
            self.mef_init(rrq_packet)

    def mef_init(self, packet):
        print(packet)
        tftp_server_address = (self.ip, self.porta_request)
        self.sock.sendto(packet, tftp_server_address)    

        message = especificacao_pb2.Mensagem()
        # Para extrair informações específicas dos campos da mensagem

        message.ParseFromString(packet)

        if message.WhichOneof('msg') == 'rrq':
            self.__handler = self.handle_rx
        elif message.WhichOneof('msg') == 'wrq':
            self.__handler = self.handle_init_tx
        elif message.WhichOneof('msg') == 'list':
            self.__handler = self.handle_list
        elif message.WhichOneof('msg') == 'mkdir':
            self.__handler = self.handle_mkdir
        elif message.WhichOneof('msg') == 'move':
            self.__handler = self.handle_move

        sched = poller.Poller()
        sched.adiciona(self)
        sched.despache()

        self.enable_timeout()
        self.reload_timeout()
        self.enable()

    def __send_data(self):
        data_message = especificacao_pb2.Mensagem()
        data_message.data.block_n = self.n
        data_message.data.message = self.file_data[(self.n-1)*512:self.n*512]
        data_packet = data_message.SerializeToString()

        self.sock.sendto(data_packet, (self.ip, self.porta))
        return data_packet

    def get_ip(self):
        return self.ip

    def get_port(self):
        return self.porta

    def __handle_tx(self, is_init_tx: bool, message):
        is_ack = False

        if message.HasField('ack'):
            is_ack = True
            self.n += 1
        data_packet = self.__send_data()

        if len(data_packet) < 512:
            self.__handler = self.handle_finish
        elif is_init_tx:
            if len(data_packet) >= 512:
                self.__handler = self.handle_tx

        self.enable_timeout()
        self.reload_timeout()



## Funcionalidades da parte 2:

    def tftp_list(self, path):
        message = especificacao_pb2.Mensagem()
        # Instância da mensagem Path
        path_message = especificacao_pb2.Path()
        # Preenchendo o campo "path"
        path_message.path = path
        # Definindo a mensagem ListResponse no campo "list" da mensagem Mensagem
        message.list.CopyFrom(path_message)

        # Converta a mensagem para sequência de bytes
        packet = message.SerializeToString()


        self.mef_init(packet)

    def handle_list(self, message):
        for item in message.list_resp.items:
            if item.HasField('file'):
                print(f"f: {item.file.nome} ({item.file.tamanho} bytes)")
            elif item.HasField('dir'):
                print(f"d: {item.dir.path}")
        self.disable_timeout()
        self.disable()




    def tftp_mkdir(self, path):
        message = especificacao_pb2.Mensagem()
        mkdir_message = especificacao_pb2.Path()
        mkdir_message.path = path
        message.mkdir.CopyFrom(mkdir_message)
        packet = message.SerializeToString()
        self.mef_init(packet)
        self.disable_timeout()
        self.disable()

    def handle_mkdir(self, message):
        if message.HasField('ack'):
            print("Diretório criado com sucesso !!")
            print("Número do bloco ACK:", message.ack.block_n)
        self.disable_timeout()
        self.disable()





    def tftp_move(self, original_name, new_name):
        print(len(new_name))
        print(f'original_name: {original_name}//////new: {new_name}')
        message = especificacao_pb2.Mensagem()
        # Instância da mensagem MOVE
        move_message = especificacao_pb2.MOVE()
        # Preenchendo o campo "nome_orig"
        move_message.nome_orig = original_name
        # Preenchendo o campo "nome_novo"
        move_message.nome_novo = new_name
        # Definindo a mensagem MOVE no campo "move" da mensagem Mensagem
        message.move.CopyFrom(move_message)
        packet = message.SerializeToString()


        
        self.mef_init(packet)
        self.disable_timeout()
        self.disable()

    def handle_move(self, message):
        print("veio")
        if message.HasField('ack'):
            print(f'Sucesso: mensagem Ack com número de bloco 0')
        elif message.HasField('error'):
            error_code = message.error.errorcode
            error_message = message.error.errmsg
            print(f'Erro: mensagem Err com código de erro {error_code} e mensagem de erro: {error_message}')
        self.disable_timeout()
        self.disable()
