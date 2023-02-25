import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

sock.settimeout(15)  # tempo limite de 5 segundos

try:
    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print("Mensagem recebida:", data.decode())
        
        # Envia uma resposta ao transmissor
        MESSAGE = input("Digite uma mensagem: ")
        sock.sendto(MESSAGE.encode(), addr)
except socket.timeout:
    print("Tempo limite de recepção ou transmissão excedido!")
