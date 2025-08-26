# **Roteiro de Laboratório: Janela Deslizante para Análise de Dados de Acelerômetro com Python**

## **1\. Contexto**

Nos roteiros anteriores, aprendemos a:

1. [**Ler e Serializar Dados:**](../../../aulas/data_collect_arduino/arduino_imu_comm/arduino_imu_comm.md) Configurar um Arduino com um sensor MPU-6050 para enviar dados de aceleração via porta serial em um formato limpo e padronizado.  
2. [**Ingestão para a Nuvem:**](../../../aulas/data_collect_arduino/data_ingestion/data_ingestion.md) Utilizar o edge-impulse-data-forwarder como uma ponte para enviar esses dados diretamente para uma plataforma de Machine Learning.

Neste laboratório, vamos explorar uma abordagem alternativa e fundamental para o processamento de dados em tempo real: a **análise local**. Em vez de enviar cada leitura do sensor para a nuvem, criaremos um script em Python que captura e processa os dados diretamente no computador. Essa técnica é a base para muitas aplicações de Machine Learning embarcado, onde as decisões precisam ser tomadas localmente no dispositivo.

## **2\. Objetivo**

O objetivo é desenvolver um script em Python que leia os dados de aceleração enviados pelo Arduino, organize-os em blocos de tamanho fixo usando uma **janela deslizante** e simule uma rotina de processamento para cada bloco.

Ao final, você terá aprendido a:

* Estabelecer comunicação serial entre um dispositivo (Arduino) e um script Python.  
* Implementar o conceito de janela deslizante (*sliding window*) para agrupar dados de sensores.  
* Estruturar um código robusto para processamento contínuo de dados em tempo real.

## **3\. Pré-requisitos**

1. **Hardware Configurado:** O Arduino deve estar carregado com o código final da [**Parte 2 do Roteiro de Leitura e Serialização**](../../../aulas/data_collect_arduino/arduino_imu_comm/arduino_imu_comm.md), enviando os dados do acelerômetro no formato x,y,z na taxa de 115200 bps.  
2. **Python 3:** Instalado em seu computador.  
3. **Biblioteca pyserial:** Você instalou durante o roteiro [Instalação das ferramentas de desenvolvimento](../../data_collect_arduino/install_tools/install_tools.md) com o script [install_tools.sh](../../data_collect_arduino/install_tools/install_tools.sh) :
---

## **4\. Conceito-Chave: A Janela Deslizante (Sliding Window)**

Para analisar dados de sensores que chegam continuamente, como os de um acelerômetro, raramente olhamos para uma única amostra isolada. Em vez disso, analisamos um pequeno "pedaço" de tempo, ou uma **janela**, para entender o contexto do que está acontecendo.

A janela deslizante funciona assim:

1. **Coleta:** Acumulamos um número fixo de amostras (ex: 100 leituras) em uma lista. Isso é o `WINDOW_SIZE`.  
2. **Processamento:** Uma vez que a janela está cheia, executamos nossa lógica sobre ela (neste caso, apenas imprimimos os dados).  
3. **Deslocamento:** Para a próxima iteração, não descartamos a janela inteira. Mantemos uma parte dos dados mais recentes e removemos apenas os mais antigos. A quantidade de amostras descartadas é definida pelo **passo** (`STRIDE`).

**Exemplo:** Com `WINDOW_SIZE` = 10 e STRIDE = 4:

* **Janela 1:** `[d1, d2, d3, d4, d5, d6, d7, d8, d9, d10] -> Processa`.  
* Descarta os 4 primeiros (`STRIDE`), mantém os 6 últimos.  
* **Próxima Janela:** `[d7, d8, d9, d10, d11, d12, d13, d14, d15, d16] -> Processa`.

## **5\. Instruções: Construindo o Script**

Modifique o template de código abaixo para implementar a lógica da janela deslizante. Os pontos a serem completados estão marcados com ``## ESCREVA SEU CÓDIGO AQUI ##``.

### **Estrutura do Código (Template)**

```python
import serial
import sys

# --- Constantes de Configuração ---
SERIAL_PORT = '/dev/ttyACM0'
#SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200

# Parâmetros da Janela Deslizante
WINDOW_SIZE = 125  # Número de amostras a serem acumuladas
STRIDE = 50        # Número de amostras a serem descartadas ao deslizar

def process_line(line_str):
##  Inclua aqui função que você desenvolveu na atividade anterior
    ## ESCREVA SEU CÓDIGO AQUI ##


def process_window(window_data):
    """
    Função chamada quando a janela está cheia. Por enquanto, apenas exibe informações.
    """
    print(f"--- Processando Janela de {len(window_data)} amostras ---")
    if window_data:
        print(f"  Primeira amostra: {window_data[0]}")
        print(f"  Última amostra:   {window_data[-1]}")
    print("--------------------------------------------------\n")

def main():
    """
    Função principal: implementa a lógica da janela deslizante.
    """
    print("Iniciando Passo 3: Janela Deslizante...")
    data_window = []

    try:
        # O 'with' garante que a porta serial seja aberta e fechada automaticamente.                
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print(f"Porta serial '{SERIAL_PORT}' aberta com sucesso.")
            ser.flushInput()  # Limpa o buffer de entrada para começar do zero.

            while True:
                # Lê uma linha de bytes, decodifica para string e remove espaços.                                
                line_str = ser.readline().decode('utf-8').strip()
                
                if line_str:
                    # Processa a linha recebida e extrai as features                    
                    features = process_line(line_str)
                    if features:
                    # Adicione as features extraídas à janela de dados na lista data_window
                    # Aqui, cada 'features' representa uma amostra processada do acelerômetro
                        ## ESCREVA SEU CÓDIGO AQUI ##

                # Verifique se a janela atingiu o tamanho definido (WINDOW_SIZE)
                if ## ESCREVA SEU CÓDIGO AQUI ##
                    # Chama a função para processar os dados da janela
                    process_window(data_window)
                    
                    # Implementa o "deslizamento" da janela, removendo as amostras mais antigas
                    # e mantendo as mais recentes
                    ## ESCREVA SEU CÓDIGO AQUI ##

    except serial.SerialException as e:
        print(f"Erro crítico: Não foi possível abrir a porta serial '{SERIAL_PORT}'.")
        print(f"Detalhes: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nPrograma encerrado pelo usuário.")
    finally:
        print("Finalizando o programa.")

if __name__ == "__main__":
    main()

```

---
