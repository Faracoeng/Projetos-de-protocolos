# promela

Gerar o `pan.c` do enquadramento:

> ./spin -a enq.pml

Para o arq:

> ./spin -a arq.pml


Após gerar o pan.c do pml desejado, basta compilar ele:

> gcc -o pan pan.c

Na sequênica é so rodar:

> ./pan -a -N prop1


### Resultados e análises

#### Protocolo ARQ do tipo pare-espere

Primeira propriedade:

> "Se uma mensagem for transmitida, ela será recebida em algum momento"

A sentença LTL definida foi:

> ltl rcv {[] (transmissor@send_data -> <> !(receptor@not_rcv))}

A sentença principal `(transmissor@send_data -> <> !(receptor@not_rcv))` sempre deve espera-se que seja verdade, por conta do operador '[]'.

A lóga da análise consiste em uma label `send_data` aplicada no processo (transmissor), para identificar o envio de dados.

Este envio, segundo a primeira propriedade, espera que seja retornado, o que não é verdade, pois o modelo de fato não trabalha com esta garantia.

Portanto no LTL, existe uma label `not_rcv` no receptor, acionada pela validação `tx?data,num`. Este é o caso em que a mensagens é perdida, e o LTL, trabalha com a negação deste possível evento, porém, considerando apenas que ele **EVENTUALMENTE**"<>" ocorre.

**Conforme ilustrado abaixo, a saída não relatou erros:**

warning: only one claim defined, -N ignored

(Spin Version 6.5.2 -- 30 May 2023)
        + Partial Order Reduction

Full statespace search for:
        never claim             + (rcv)
        assertion violations    + (if within scope of claim)
        acceptance   cycles     + (fairness disabled)
        invalid end states      - (disabled by never claim)

State-vector 52 byte, depth reached 63, errors: 0
       58 states, stored (62 visited)
       16 states, matched
       78 transitions (= visited+matched)
        0 atomic steps
hash conflicts:         0 (resolved)



unreached in proctype transmissor
        arq.pml:31, state 10, "printf('transmissor recebeu ack incorreto: %d\n',!(seq))"
        arq.pml:37, state 18, "-end-"
        (2 of 18 states)
unreached in proctype receptor
        arq.pml:56, state 13, "-end-"
        (1 of 13 states)
unreached in claim rcv
        _spin_nvr.tmp:10, state 13, "-end-"
        (1 of 13 states)


Partes do código inalcançáveis (unreached):

- O Spin identificou partes do código que não são alcançáveis durante a execução do modelo.
- No proctype "transmissor", os estados nas linhas 10 e 18 são considerados inalcançáveis. Isso ocorre porque esses estados não podem ser alcançados de acordo com a lógica do modelo para esta análise (LTL).
- No proctype "receptor", o estado na linha 13 é considerado inalcançável.
- Na reivindicação (claim) "rcv", o estado na linha 13 também é considerado inalcançável.


Ao ajustar o LTL para:

> ltl rcv {[] (transmissor@send_data -> !(receptor@not_rcv))}

**Removendo o **EVENTUALMENTE**"<>", a saída demonstra o erro esperado:**

warning: only one claim defined, -N ignored
pan:1: assertion violated  !( !(( !((transmissor._p==send_data))|| !((receptor._p==not_rcv))))) (at depth 4)
pan: wrote arq.pml.trail

(Spin Version 6.5.2 -- 30 May 2023)
Warning: Search not completed
        + Partial Order Reduction

Full statespace search for:
        never claim             + (rcv)
        assertion violations    + (if within scope of claim)
        acceptance   cycles     + (fairness disabled)
        invalid end states      - (disabled by never claim)

State-vector 52 byte, depth reached 4, errors: 1
        3 states, stored
        0 states, matched
        3 transitions (= stored+matched)
        0 atomic steps


Com o erro, o arquivo `arq.pml.trail` é criado pelo analisador.

**Analisando o trail com o comando:**

> ./spin -t arq.pml

A saida abaixo é ilustrada:

ltl rcv: [] ((! ((transmissor@send_data))) || (! ((receptor@not_rcv))))
Never claim moves to line 4     [(1)]
spin: _spin_nvr.tmp:3, Error: assertion violated
spin: text of failed assertion: assert(!(!((!((transmissor._p==send_data))||!((receptor._p==not_rcv))))))
Never claim moves to line 3     [assert(!(!((!((transmissor._p==send_data))||!((receptor._p==not_rcv))))))]
spin: trail ends after 5 steps
#processes: 2
                queue 1 (tx): 
                send_data = 0
                not_rcv = 0
  5:    proc  1 (receptor:1) arq.pml:46 (state 2)
  5:    proc  0 (transmissor:1) arq.pml:19 (state 2)
  5:    proc  - (rcv:1) _spin_nvr.tmp:2 (state 6)
2 processes created


Essa análise indica que a propriedade LTL especificada não foi satisfeita durante a verificação do modelo.

Informações sobre os processos:

- O processo "receptor" está no estado 2 (arq.pml:46) no passo 5 do rastro de execução.
- O processo "transmissor" está no estado 2 (arq.pml:19) no passo 5 do rastro de execução.
- O processo "rcv" está no estado 6 (_spin_nvr.tmp:2) no passo 5 do rastro de execução.
- Foram criados 2 processos no total.


Detalhes do erro:

- A verificação do modelo Spin encontrou um erro no cumprimento da propriedade LTL especificada.
- O erro ocorreu na linha 3 do arquivo "_spin_nvr.tmp".
- O texto do erro indica que a afirmação assert(!(!((!((transmissor._p==send_data))||!((receptor._p==not_rcv)))))) foi violada.
- A propriedade LTL negada !(!((!((transmissor._p==send_data))||!((receptor._p==not_rcv)))) não foi satisfeita.

Fim do rastro (trail):

- O rastro (trail) de execução termina após 5 passos.


Segunda propriedade:

> "Uma nova mensagem é transmitida somente se a mensagem anterior for confirmada"

A sentença LTL definida foi:

> ltl tx {[] (transmissor@send_data -> <>(receptor@recebeu U transmissor@send_data))}

- transmissor@send_data: O evento "transmissor envia dados" ocorre em algum momento.
- receptor@recebeu: O evento "receptor recebeu dados" ocorre em algum momento.
- receptor@recebeu U transmissor@send_data: O evento "receptor recebeu dados" ocorre em algum momento até que o evento "transmissor envia dados" ocorra.
- [] (transmissor@send_data -> <>(receptor@recebeu U transmissor@send_data)): É sempre verdade que se o evento "transmissor envia dados" ocorrer, de acordo com a *tag* aplicada, então eventualmente o evento "receptor recebeu dados" ocorrerá antes do próximo evento "transmissor envia dados".


Após aplicar o LTL no modelo, erros são encontrados:

ltl tx: [] ((! ((transmissor@send_data))) || (<> (((receptor@recebeu)) U ((transmissor@send_data)))))
Never claim moves to line 4     [(1)]
          transmissor transmitiu msg 0
          retransmitiu data 0
spin: trail ends after 16 steps
#processes: 2
                queue 1 (tx): 
                send_data = 0
                recebeu = 0
 16:    proc  1 (receptor:1) arq.pml:48 (state 4)
 16:    proc  0 (transmissor:1) arq.pml:22 (state 15)
 16:    proc  - (tx:1) _spin_nvr.tmp:2 (state 5)


Neste caso, após a linha "Never claim moves to line 4     [(1)]".

As linhas seguintes fornecem informações sobre o estado dos processos no sistema/modelo.

- "transmissor transmitiu msg 0" indica que o processo "transmissor" transmitiu a mensagem 0.
- "retransmitiu data 0" indica que a data 0 foi retransmitida.

A linha "spin: trail ends after 16 steps" indica que a execução do modelo foi concluída após 16 passos.

As linhas a seguir fornecem informações detalhadas sobre o estado dos processos no momento da conclusão da execução:

- "send_data = 0" indica que o valor da variável "send_data" no processo é 0.
- "recebeu = 0" indica que o valor da variável "recebeu" no processo é 0.

As próximas três linhas fornecem informações sobre o estado atual de cada processo:

- "16: proc 1 (receptor:1) arq.pml:48 (state 4)" indica que o processo 1 (receptor) está no estado 4.
- "16: proc 0 (transmissor:1) arq.pml:22 (state 15)" indica que o processo 0 (transmissor) está no estado 15.
- "16: proc - (tx:1) _spin_nvr.tmp:2 (state 5)" indica que o processo - (tx) está no estado 5.

#### Enquadramento

Primeira propriedade:

> "Quadros que excedam o tamanho máximo são descartados pelo receptor"

A sentença LTL definida foi:

> ltl prop2 { [](fram_rx@tx_data  -> <>(fram_rx:cnt_rx==false)) }


A sentença LTL diz que quando `tx_data`, uma label de monitoramento de envio de dado, é acionada, implica que **EVENTUALMENTE**"<>", a variável local `cnt_rx` é false, indica que o *buffer* não estourou. O uso desta variável de apoio se fez necessário devido a um cenário de teste que estava ocorrendo na validação do LTL. Após validar a sentença, para o caso de monitorar o contador do *buffer* diretamente no LTL, uma séria de variações de estados eram geradas no spin, de modo que foram necessárias 5 milhões de rotas para validar o modelo, pois a cada passo que a variavel contadora incrementava, uma nova combinação de modelo etra definida. Desta forma, através apenas de uma variável booleana que acompanhan o estouro do `buffer`, é possível simplificar significativamente o processo.

Conforme a saída abaixo:

(Spin Version 6.5.1 -- 20 December 2019) + Partial Order Reduction

Full statespace search for: never claim + (prop2) assertion violations + (if within scope of claim) acceptance cycles + (fairness disabled) invalid end states - (disabled by never claim)

State-vector 48 byte, depth reached 4523, errors: 0 
252330 states, stored (253086 visited) 126960 states, matched 380046 transitions (= visited+matched) 0 atomic steps hash conflicts: 564 (resolved)


unreached in proctype fram_tx enq.pml:26, state 15, "tx!flag" enq.pml:29, state 20, "-end-" (2 of 20 states) unreached in proctype fram_rx enq.pml:93, state 62, "-end-" (1 of 63 states) unreached in claim prop2 _spin_nvr.tmp:10, state 13, "-end-" (1 of 13 states)



O analisador não identificou erros.

Informações sobre a busca no espaço de estados:

- O Spin realizou uma busca completa no espaço de estados para verificar o modelo.
- O estado do vetor (state-vector) tem tamanho de 48 bytes.
- A profundidade alcançada durante a busca foi de 4523.
- Não foram encontrados erros durante a verificação.

Estatísticas sobre o espaço de estados:

- O modelo possui um total de 252330 estados, sendo 253086 visitados e 252330 armazenados.
- O modelo possui 380046 transições, considerando estados visitados e estados armazenados.

Partes do código inalcançáveis (unreached):

- O Spin identificou partes do código que não são alcançáveis durante a execução do modelo.
- No proctype "fram_tx", os estados nas linhas 15 e 20 são considerados inalcançáveis.
- No proctype "fram_rx", o estado na linha 62 é considerado inalcançável.