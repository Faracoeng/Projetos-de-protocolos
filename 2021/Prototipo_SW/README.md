## Especificação do protocolo de enlace

> Desenvolver um protocolo de enlace ponto-a-ponto usando um canal sem-fio.

**Os objetivos do projeto estão descritos na raiz do repositório**

- Como será utilizada uma interface serial, as leituras e escritas realizadas na comunicação serão executadas como fluxos de dados sequêncial;
- Serão utilizadas APIs elementares para executar esta comunicação serial através de programas que se comunicam entre si, e assim validar o projeto;
- Temos exemplos de API's `tx.py` e `rx.py` fornecidas;
- Será utilizado um emulador de link serial para implementar  `tx.py` e `rx.py` e facilitar o desenvolvimento dos mecanismos básicos do protocolo;

#### Técnica de enquadramento

> Tem por objetivo delimitar os octetos de bytes representando as mensagem encaminhadas na comunicação. O protocolo a ser desenvolvido deve ser capaz de enviar e receber unidades de dados formadas por tais sequências de octetos.
A abordagem definida em aula para delimitar os quadros foi a **Sentinela**, que estabelece um padrão de bits/bytes para delimitar os quadros, exemplos de protocolos que utilizam esta abordagem são (PPP e HDLC).

A sequência de transmissão e recepção de um quadro pode ser descrita da seguinte forma:

- A camada superior envia uma PDU (Packet Data Unit) para a camada de enlace. Essa PDU, formada por múltiplos octetos, pode ter um conteúdo arbitrário.
- A camada de enlace encapsula essa PDU em um quadro (frame), Isso envolve adicionar um cabeçalho (header) e possivelmente um sufixo (trailer) contendo informações necessárias ao protocolo de enlace.
- A camada de enlace analisa o conteúdo do quadro em busca de octetos cujos valores tenham significado especial para a função de enquadramento. Em específico, octetos com valores Flag e ESC não podem aparecer dentro do quadro nesta etapa, pois eles têm um significado especial para que o receptor consiga delimitar o quadro e recebê-lo corretamente. O transmissor realiza o procedimento de preenchimento de byte para cada octeto especial encontrado. Esse procedimento envolve inserir um octeto com valor ESC antes do octeto especial, e então mudar o valor desse octeto. A ideia é esconder o octeto especial, para que não seja interpretado de forma indevida pelo receptor.
- Após o preenchimento de byte, a camada de enlace insere octetos Flag no início e no final do quadro, e então o transmite (na prática, a camada de enlace transmite a Flag, seguida dos octetos do quadro, e da Flag final).
- O receptor identifica o início de um quadro ao receber uma Flag. Ele passa a então a receber os octetos do quadro.
- O receptor, durante a recepção do conteúdo do quadro, fazer o processo reverso ao preenchimento. Sempre que encontrar um octeto com valor ESC, ele o descarta e então recupera o valor original do octeto seguinte.
- O receptor termina a recepção do quadro ao receber uma nova Flag. Ele então interpreta o cabeçalho e o sufixo e, se o quadro for válido, desencapsula seu conteúdo e entrega à camada superior.

