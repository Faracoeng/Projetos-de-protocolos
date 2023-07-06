# biblioteca contendo a MEF, representada 
# por uma classe chamada Protocolo
# e apelidada de tftp, apenas para facilitar seu uso
from tftp_client_protocol import Protocolo as tftp
import sys


# Endereço IP e porta do servidor TFTP
SERVER_IP = '127.0.0.1'
SERVER_PORT = 6969

# Tratativa para garantir que o programa de testes 
# será executado corretamente
try:
    SERVER_IP = sys.argv[1]
    SERVER_PORT = sys.argv[2]

    print(f'Os dados para conexão com servidor TFTP são: IP {SERVER_IP} e a porta {SERVER_PORT}')

except:
    
    SERVER_IP = '127.0.0.1'
    SERVER_PORT = 6969
    print(f'Como não foram especificados o IP e a porta do servidor TFTP, serão atribuídos os valores default IP {SERVER_IP} e a porta {SERVER_PORT}')


# Instancia um objeto da biblioteca desenvolvida, passando como parametro o IP e a POrta do servidor TFTP
tftp_client = tftp(SERVER_IP, SERVER_PORT)


def upload_file(filename):
    # Inicia o processo de upload de arquivo através da biblioteca
    # enviando o nome do arquivo que se deseja enviar 
    # ao servidor como parametro
    tftp_client.tftp_upload(filename)


def download_file(filename):
    # Inicia o processo de download de arquivo através da biblioteca
    # enviando o nome do arquivo que se deseja baixar 
    # do servidor como parametro
    tftp_client.tftp_download(filename)

# Menu de uso do programa de testes
def menu():

    while True:
        
        print("Escolha uma opção:")
        print("1. Realizar upload de arquivo")
        print("2. Realizar download de arquivo")
        print("3. Sair")
        try:
            opcao = int(input("Digite o número da opção desejada: "))
        except ValueError:
            print("A entrada deve ser um número inteiro. Tente novamente.")

        if opcao == 1:
            filename = input("Digite o nome do arquivo que deseja fazer Upload: ")
            upload_file(filename)
        elif opcao == 2:
            filename = input("Digite o nome do arquivo que deseja fazer Download: ")
            download_file(filename)
        elif opcao == 3:
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")



if __name__ == '__main__':
    menu()
