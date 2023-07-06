# Modo de uso da biblioteca

#### O programa de teste `app.py` esta localizado na raiz do repositório. Para executá-lo corretamente, é necessário passar como parâmetro o IP e a Porta em que o servidor TFTP está trabalhando, conforme exemplo abaixo:

> python3 app.py 127.0.0.1 6969

#### Caso contrário, um IP e Porta *default* serão assumidos.

#### Após a execução, um menu interativo será ilustrado, norteando os processos de *upload* e *download* de arquivos que a biblioteca provê.


**Importante que os arquivos que se deseja realizar o *upload* estejam na raiz do diretório!!!** 


## Funcionalidades da biblioteca

### Função `tftp_upload(filename)`

É responsável por realizar o upload de um arquivo para o servidor TFTP. Ela recebe como parâmetro o nome do arquivo a ser enviado.

A sequência de ações executadas pela função é descrita abaixo:

- Estabelece uma conexão com o servidor TFTP.
- Envia uma mensagem de solicitação de escrita (WRQ) contendo o nome do arquivo e o modo de transferência.
- Entra em um estado de espera por resposta do servidor.
- Implementa a Máquina de Estados Finitos (MEF) para processar os pacotes recebidos e enviar pacotes ACK para confirmar o recebimento correto.
- Trata casos de timeout e erros durante o processo de upload.
- Exibe uma mensagem de confirmação se o upload for concluído com sucesso.

#### Função `tftp_download(filename)`

É responsável por realizar o download de um arquivo do servidor TFTP. Ela recebe como parâmetro o nome do arquivo a ser baixado.

A sequência de ações executadas pela função é descrita abaixo:

- Estabelece uma conexão com o servidor TFTP.
- Envia uma mensagem de solicitação de leitura (RRQ) contendo o nome do arquivo e o modo de transferência.
- Entra em um estado de espera por resposta do servidor.
- Implementa a Máquina de Estados Finitos (MEF) para processar os pacotes recebidos e enviar pacotes ACK para confirmar o recebimento correto.
- Trata casos de timeout e erros durante o processo de download.
- Exibe uma mensagem de confirmação se o download for concluído com sucesso.
- Salva o arquivo baixado no sistema local.



# TFTP2

Alterações em relalção a V1:

- Utiliza Protocol Buffers para padronizar as mensagens TFTP.
- Implementação de novas funcionalidades:
    - **LIST**: fazer listagem de uma pasta;
    - **MKDIR**: cria uma pasta;
    - **MOVE**: renomeia ou remove arquivos;



`Especificacao_pb2.py` foi gerada pelo comando:

> protoc -I=. --python_out=. `tftp_messages.proto`
