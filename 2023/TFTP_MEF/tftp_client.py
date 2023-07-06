import socket
import struct
import tftp_client_protocol as tftp_client



mef = tftp_client


# O protocolo possui duas ações, ou traz um arquivo do servidor, ou envia

# Como parametro recebe o nome do arquivo

def tftp_download(filename):
    # # Intanciando socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    # # Se conecta em qualquer porta livre no Host
    sock.bind(('0.0.0.0', 0))

    # # Envia requisição de leitura para o servidor
    # #A classe RRQ deve retornar essa string
    rrq_packet = struct.pack('!H{}sB5sB'.format(len(filename)), 1, filename.encode(), 0, b'octet', 0)
    # # requisição fica assim:
    # # b'\x00\x01./arquivo_teste.txt\x00octet\x00'
    # # Envia a requisição para endereço e porta do servidor
    # # Despache, maciona o callback
    sock.sendto(rrq_packet, (SERVER_IP, SERVER_PORT))



    # Recebendo os pacotes do servidor e escrevendo no em um arquivo local
    # 
    with open(filename, 'wb') as f:
         # Número do bloco
         block_num = 1

         while True: # Não vai precisar desse while
    #         # O poller vai ficar sempre escutando
    #         #Retorna os dados e o endereço e porta do servidor
             data, addr = sock.recvfrom(516)
             # data: b'\x00\x03\x00\x01ola\ncliente\n'

             # Aqui descompacta os 4 prmeiros bytes
    #         # Número do bloco e o opcode
             opcode, block = struct.unpack_from('!HH',data)
    #         # Conteúdo para ser escrito no arquivo 
    #         body = data[struct.calcsize('!HH'):]
    #         #opcode, block = struct.unpack('!H2xH', data[:4])
    #         # Caso seja um pacote de dados
    #         if opcode == 3:  
    #             if block == block_num:
    #                 # Escreve body no arquivo 
    #                 f.write(body)
    #                 # Como o pacote foi recebido, monta o pacote de
    #                 # ACK e envia para o endereço do servidor
    #                 ack_packet = struct.pack('!HH', 4, block_num)
    #                 # b'\x00\x04\x00\x01'
    #                 sock.sendto(ack_packet, addr)
                    
    #                 # Incrementa o número do bloco
    #                 block_num += 1
    #                 # SE o pacote for menor que 512 bytes, encerra
    #                 if len(data) < 512:
    #                     break
    #             # Caso de pacote duplicado, se vier com o mesmo block_num, reenvia o ACK
    #             else:  
    #                 sock.sendto(ack_packet, addr)
            
    #         # Caso seja um pacote de erro
    #         elif opcode == 5:  
    #             print(f"Error: {data[4:-1].decode()}")
    #             break

    # sock.close()

def tftp_upload(filename):



    # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    # sock.bind(('0.0.0.0', 0))


    # wrq_packet = struct.pack('!H{}sB5sB'.format(len(filename)), 2, filename.encode(), 0, b'octet', 0)
    # sock.sendto(wrq_packet, (SERVER_IP, SERVER_PORT))

    # # Enviando os pacotes de dados para o servidor
    # # Abre arquivo em modo binario e lê 512 bytes dele
    with open(filename, 'rb') as f:
         block_num = 1
         while True:
             data = f.read(512)
             if not data:
                 break
             data_packet = struct.pack('!HH{}s'.format(len(data)), 3, block_num, data)

             # Aqui preciso esperar o ACK antes de enviar o DATA
    #         print(data_packet)
    #         sock.sendto(data_packet, (SERVER_IP, SERVER_PORT))
    #         #Aguarda até receber o ACK
    #         while True:  
    #             ack_data, addr = sock.recvfrom(4)
    #             print(ack_data)
    #             opcode, block = struct.unpack('!HH', ack_data)
    #             # Aguarda o ACK e valida o numero do bloco, se der tudo certo, incrementa 
    #             if opcode == 4 and block == block_num:
    #                 block_num += 1
    #                 break
    #             # Caso seja um pacote de erro
    #             elif opcode == 5:  
    #                 print(f"Error: {ack_data[4:-1].decode()}")
    #                 return

    # sock.close()

#tftp_upload("arquivo_cliente.txt")
#tftp_download("arquivo_server.txt")