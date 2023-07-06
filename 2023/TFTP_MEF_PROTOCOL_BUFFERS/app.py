# biblioteca contendo a MEF, representada 
# por uma classe chamada Protocolo
# e apelidada de tftp, apenas para facilitar seu uso
#from tftp_client_protocol import Protocolo as tftp
#from tftp_client_protocol2 import Protocolo as tftp
from tftp_client_protocol2 import Protocolo as tftp
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


protocolo = tftp(SERVER_IP, SERVER_PORT)

def exibir_menu():

    print("\n--- Menu ---")
    print("1. Realizar upload de arquivo")
    print("2. Realizar download de arquivo")
    print("3. Realizar listagem de um path")
    print("4. Criar um diretorio")
    print("5. Excluir ou Renomear")
    print("6. Sair")


def main():



    while True:

        exibir_menu()
        opcao = input("Digite o número da opção desejada: ")

        if opcao == '1':
            filename = input('Digite o nome do arquivo a ser enviado: ')
            protocolo.tftp_upload(filename)
        elif opcao == '2':
            filename = input('Digite o nome do arquivo a ser baixado: ')
            protocolo.tftp_download(filename)
        elif opcao == '3':
            path = input('Digite o caminho a ser listado: ')
            protocolo.tftp_list(path)
        elif opcao == '4':
            path = input('Digite o caminho do diretório a ser criado: ')
            protocolo.tftp_mkdir(path)
        elif opcao == '5':
            nome_original = input('Digite o nome original do arquivo que deseja renomear ou remover: ')
            novo_nome = input('Digite novo nome do arquivo. Se deseja remover, deixe o nome vazio: ')
            protocolo.tftp_move(nome_original, novo_nome)
            #protocolo.tftp_move("a.txt","")

            
        elif opcao == '6':
            break
        else:
            print('Opção inválida. Tente novamente.')

if __name__ == '__main__':
    main()
