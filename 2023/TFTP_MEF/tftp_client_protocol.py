import poller
import socket 
import struct 
import os
from tftp_messages import *
#from enum import IntEnum as enum

class Protocolo(poller.Callback):

    def __init__(self, ip:str, porta:int):

        # Atributo recebe sempre a referência do método que
        # representa o Estado Atual do Protocolo
        self.___handler = None
        self.disable_timeout()
        self.ip = ip
        self.porta = int(porta)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', 0))
        poller.Callback.__init__(self, self.sock, 3)
        self.n = 0
        self.filename = ''
        self.file_data = bytearray()
        # Instanciando objetos genéricos de cada mensagen TFTP
        self.RRQ_message = RRQMessage()
        self.WRQ_message = WRQMessage()
        self.Data_message = DataMessage()
        self.Error_message = ErrorMessage()
        self.ACK_message = AckMessage()

# Sempre que chegar algum pacote no socket sendo monitorado pelo Poller,
# Este método será invocado
# Ele é responsável por ler o pacote, validar se é um erro,
# E se não for, joga para o Estado atual do protocolo para dar sequência
    def handle(self):
        # 516 por conta do pacote Data
        packet, addr = self.sock.recvfrom(516)

        print("handle: ", str(packet))
        
        if(self.Error_message.unpack(packet)):
            
            error_code = self.Error_message.get_error_code()
            error_message = self.Error_message.get_error_message()
            error = f'erro : 0{error_code} / ({error_message})'
            print(error)
            self.disable()
            self.reload_timeout()
            self.disable_timeout()
        else :
            self.__handler(packet)

    def handle_timeout(self):
        #packet = 'timeout'
        #self.__handler(packet)
        print('Timeout !')
        self.disable_timeout()
        if((self.__handler == self.handle_rx)|(self.__handler == self.handle_init_tx)):
            #self.__handler = self.handle_idle
            self.disable()
        if(self.__handler == self.handle_tx)|(self.__handler ==self.handle_finish):
            self.__send_data()
        self.n = 0

# Métodos Que representam os Estados da MEF

# Estado inicial do protocolo, responsável por validar se app() 
# solicitou upload (WRQ) ou download (RRQ), cujo pacote é 
# recebido pelos métodos tftp_download() ou tftp_upload()

# Quando o handle() receber um pacote do socket através do poller 
# Ele encaminha o pacote para o estado atual, neste caso, o estado 
# deverá receber um ACK para só então enviar um "Data"  

    def handle_init_tx(self, packet):
        print("handle_init_tx: ", str(packet))
        self.__handle_tx(True, packet)

    def handle_tx(self, packet):
        print("handle_tx: ", str(packet))
        self.__handle_tx(False, packet)
        
# Este método é acionado quando o app() aciona o método download(),
# O idle automaticamento ajusat a referencia de Estado pelo 
# atributo self.__handler, e o estado recebe o pacote solicitado pelo RRQ

    def handle_rx(self, packet):
        print("handle_rx: ", str(packet))
        if(len(packet)==0):
            pass
        elif(self.Data_message.unpack(packet)):
            
            # Se for de fato um pacote de dados,
            # Pega seu body e seu block_num
            body = self.Data_message.get_body()
            block_num = self.Data_message.get_block_num()

            # Cria o pacote ACK para confirmar seu recebimento
            ack_packet = self.ACK_message.pack(block_num)
            print('I SEND THE ACK: ',str(ack_packet))

            self.sock.sendto(ack_packet, (self.ip, self.porta))
            
            if(self.n+1 == block_num):
                self.n+=1
                self.file_data.extend(body)

            # Quando finalizar o recebimento do arquivo
            # Volta para o esta idle
            if((len(body) < 512)):
                arquivo = open(self.filename, 'a')
                # Aqui pode dar erro,
                arquivo.write(self.file_data.decode())
                arquivo.close()
                self.file_data = bytearray()
                #self.__handler = self.handle_idle
                self.disable()
                final_rrq_message = f'download do arquivo "{self.filename}" realizado com sucesso'
                print(final_rrq_message)
            self.disable_timeout()

    def handle_finish(self, packet):
        print("handle_finish: ", str(packet))
        if(self.ACK_message.unpack(packet)):

            final_wrq_message = f'recebeu o ACK... o upload do arquivo "{self.filename}" foi realizado com sucesso'   
            print(final_wrq_message)
            self.file_data = bytearray()
            # Ao finalizar o upload, volta para o estado idle
            self.disable_timeout()
            self.disable()
            #self.__handler = self.handle_idle



# Métodos operacionais

    def tftp_upload(self, filename):
        print('Inciando upload de arquivo pelo WRQ...')
        self.filename = filename
        if os.path.exists(filename)==False:
            print(f"O arquivo {self.filename} não existe!!")
            self.reload_timeout()
            self.disable_timeout()
            self.disable()
        else:
            #fazer a leitura do arquivo, jogar numa variavel 
            with open(self.filename, 'rb+') as arquivo:
                self.file_data=bytearray(arquivo.read())
                arquivo.close()
            wrq_request = self.WRQ_message.pack(filename)
            #wrq_request = b'\x00\x02' + b'algo2.txt' + b'\x00' + b'octet' + b'\x00'
            self.n = 0
            self.mef_init(wrq_request)

    def tftp_download(self, filename):
        print('Inciando download de arquivo pelo RRQ...')
        self.filename = filename
        if os.path.exists(filename)==True:
            print(f"O arquivo {self.filename} ja existe!!")
            self.reload_timeout()
            self.disable_timeout()
            self.disable()
        else:
            rrq_request = self.RRQ_message.pack(filename)            
            #self.n = 1
            self.mef_init(rrq_request)

# Garante o ciclo correto do protocolo e inicia o poller
    def mef_init(self, packet):
        
        
        tftp_server_address = (self.ip, self.porta)

        self.sock.sendto(packet, tftp_server_address)
        print('enviei pro servidor: ', str(packet))        
        if(self.RRQ_message.is_rrq(packet)):
            self.__handler = self.handle_rx
            print('RRQ')
        elif(self.WRQ_message.is_wrq(packet)):
            self.__handler = self.handle_init_tx
            print('WRQ')
        #self.__handler(packet)
        sched = poller.Poller()
        sched.adiciona(self)
        sched.despache()

        self.enable_timeout()
        self.reload_timeout()
        self.enable()

# Deve criar uma pacote do tipo DATA com o body 
# do arquivo que se deseja enviar ao servidor

    def __send_data(self):

        # Para funcionar, deve-se encaminhar o caminho 
        # absoluto do arquivo pelo app()

        

        data_packet = self.Data_message.pack(self.n, self.file_data[self.n*512:(self.n+1)*512])
        print('send: ', str(data_packet))

        self.sock.sendto(data_packet, (self.ip, self.porta))
        return data_packet


    def get_ip(self):
        return self.ip

    def get_port(self):
        return self.porta     
    
    def __handle_tx(self, is_init_tx:bool, packet):
        is_ack = False

        if(len(packet)>0):
            is_ack = self.ACK_message.unpack(packet)

        if(len(packet)==0) or (is_ack and self.ACK_message.get_block_num()==self.n):
            print('entrou no is ack: ',self.n)
            if not is_init_tx:
                self.n+=1
            data_packet = self.__send_data()
            if((len(data_packet) < 512)):   
                self.__handler = self.handle_finish
            elif is_init_tx:
                if((len(data_packet) >= 512)):
                    self.__handler = self.handle_tx

        self.enable_timeout()
        self.reload_timeout()
