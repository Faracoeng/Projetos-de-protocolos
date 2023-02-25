import socket

MESSAGE = input("Digite uma mensagem: ")
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(15)  # tempo limite de 5 segundos

try:
    # Envia a mensagem ao receptor
    sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
    
    # Espera por uma resposta do receptor
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print("Resposta do receptor:", data.decode())
    
except socket.timeout:
    print("Tempo limite de transmissão excedido!")
