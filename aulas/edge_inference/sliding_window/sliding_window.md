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

Modifique o template de código abaixo para implementar a lógica da janela deslizante. Os pontos a serem completados estão marcados com TODO.

### **Estrutura do Código (Template)**

```python

import serial  
import sys

# --- Constantes de Configuração ---  
# TODO: Ajuste a porta serial para a correta no seu sistema (ex: 'COM3' no Windows)  
SERIAL_PORT = '/dev/ttyUSB0'  
BAUD_RATE = 115200

WINDOW_SIZE = 100  # Quantas amostras (linhas) vamos armazenar na janela  
STRIDE = 50        # Quantas amostras vamos descartar ao deslizar a janela

def process_window(window_data):  
    """  
    Função para processar os dados acumulados na janela.  
    Por enquanto, vamos apenas imprimir o tamanho e o primeiro e último item.  
    """  
    print(f"--- Processando Janela de {len(window_data)} amostras ---")  
    if window_data:  
        print(f"Primeira amostra: {window_data[0]}")  
        print(f"Última amostra: {window_data[-1]}")  
    print("--------------------------------------------------\n")

def main():  
    """  
    Função principal que lê da serial e gerencia a janela deslizante.  
    """  
    print("Iniciando leitor de dados seriais...")  
      
    # Lista para armazenar os dados da janela atual  
    data_window = []

    try:  
        # TODO 1: Inicie e abra a comunicação serial usando as constantes definidas.  
        # Dica: use o gerenciador de contexto 'with serial.Serial(...)' para garantir  
        # que a porta seja fechada automaticamente.  
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:  
            print(f"Porta serial {SERIAL_PORT} aberta com sucesso.")  
              
            # Limpa qualquer dado residual no buffer da serial  
            ser.flushInput()

            while True:  
                # TODO 2: Leia uma linha da porta serial e decodifique-a.  
                # Dica: use ser.readline().decode('utf-8').strip()  
                try:  
                    line_str = ser.readline().decode('utf-8').strip()

                    if not line_str:  
                        continue  
                      
                    # TODO 3: Separe os valores da linha usando a vírgula como delimitador.  
                    parts = line_str.split(',')

                    # TODO 4: Verifique se a linha contém exatamente 3 valores.  
                    if len(parts) == 3:  
                        # Converte os valores para float e os adiciona à janela  
                        accel_data = [float(p) for p in parts]  
                        data_window.append(accel_data)  
                    else:  
                        print(f"Aviso: Linha mal formatada ignorada: '{line_str}'")  
                        continue

                except (UnicodeDecodeError, ValueError) as e:  
                    print(f"Erro ao processar a linha. Detalhes: {e}")  
                    continue

                # TODO 5: Verifique se a janela atingiu o tamanho definido (WINDOW_SIZE).  
                if len(data_window) >= WINDOW_SIZE:  
                    process_window(data_window)  
                        
                    # TODO 6: Implemente o "deslocamento".  
                    # A nova janela deve ser uma fatia da janela antiga.  
                    # Dica: data\_window = data_window[STRIDE:]  
                    data_window = data_window[STRIDE:]

    except serial.SerialException as e:  
        print(f"Erro: Não foi possível abrir a porta serial {SERIAL_PORT}. Verifique a conexão. Detalhes: {e}")  
        sys.exit(1)  
    except KeyboardInterrupt:  
        print("\nPrograma encerrado pelo usuário.")  
    finally:  
        print("Fim do programa.")

if __name__== "__main__":  
    main()
```

---
