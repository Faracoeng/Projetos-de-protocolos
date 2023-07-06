mtype = {flag, esc, data};

chan tx = [1] of {byte};

int max_size = 32;

active proctype fram_tx() {
  int cnt;

inicio:
  tx!flag;
  cnt = 0;

    do
    :: cnt < max_size ->
        if
        :: tx!data -> cnt++;
        :: tx!esc ->
            tx!data;
            cnt++;
        fi;
    :: cnt > 0 ->
      tx!flag;
        goto inicio;
    :: else ->
      tx!flag;
        goto inicio;
    od;
}

active proctype fram_rx() {
    int cnt;
    mtype octeto;
    bool cnt_rx

estado_ocioso:
    cnt_rx = false
    cnt = 0;
    do
    :: tx?flag -> 
      goto estado_rx;
    :: tx?data -> skip; // ignora 
    :: tx?esc -> skip; // ignora
    :: tx?octeto -> skip; // simula erro de recepção
    od;

estado_rx:
    do
    :: tx?flag ->
        if
        :: cnt == 0 -> skip;
        :: else -> tx_data: goto estado_ocioso;
        fi;
    :: tx?esc ->
        if
        :: cnt < max_size -> cnt++;
        :: else -> 
          cnt_rx = true;
          skip; // Descarta quadro excedente
        fi;
        goto estado_esc;
    :: tx?data ->
        if
        :: cnt < max_size -> cnt++;
        :: else -> 
          cnt_rx = true;
          skip; // Descarta quadro excedente
        fi;
    :: tx?octeto ->
        // perdeu sincronismo
        skip;
    od;

estado_esc:
    do
    :: tx?data -> 
      tx_esc: printf("recebeu data");
        if
        :: cnt <= max_size -> cnt++;
        :: else -> 
          cnt_rx = true;
          skip;
        fi;
        goto estado_rx;
    :: tx?flag -> // erro ... não deveria receber flag
        goto estado_ocioso;
    :: tx?esc -> // erro ... não deveria receber esc
        goto estado_ocioso;
    :: tx?octeto -> 
      // perdeu sincronismo
      skip;
    od;
}

//Quadros que excedam o tamanho máximo são descartados pelo receptor
ltl prop2 { [](fram_rx@tx_data  -> <>(fram_rx:cnt_rx==false)) }