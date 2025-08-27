# **Roteiro de Laboratório: Implementação de Classificação de Dados de Aceleração em Tempo Real usando Edge Impulse**

## **1\. Descrição**:
Nesta tarefa, você deverá desenvolver um código em Python que realiza a leitura de dados de aceleração em tempo real a partir de um sensor conectado via porta serial. Os dados coletados serão processados por um modelo de classificação treinado na plataforma Edge Impulse. O objetivo é aplicar técnicas de Machine Learning para classificar os dados em tempo real e avaliar o desempenho da classificação.

## **2\. Objetivo:** Elaborar um script em Python que:

* Leia continuamente dados de aceleração (accX, accY, accZ) de um sensor conectado via porta serial.  
* Armazene os dados em uma janela deslizante.  
* Utilize o SDK do Edge Impulse para classificar os dados coletados, retornando os resultados em tempo real.  
* Exiba os resultados da classificação e o tempo necessário para processar cada janela de dados.

## **3\. Instruções:**

1. **Configuração Serial:**

   * Utilize a biblioteca `pyserial` para configurar e abrir a comunicação serial.  
   * Configure a porta serial com os seguintes parâmetros: `/dev/ttyUSB0`, `baudrate=115200`, `timeout=1`.  
2. **Configuração do Modelo Edge Impulse:**

   * Faça o download do modelo `.eim` treinado na plataforma Edge Impulse utilizando a seguinte linha de comando: `edge-impulse-linux-runner --clean --download modelfile.eim`.  
   * Para rodar o script com o modelo `.eim` como argumento, caso precise de ajuda, utilize o comando `python classify.py model.eim`.  
3. **Implementação da Janela Deslizante:**

   * Implemente uma função que leia continuamente as linhas recebidas na porta serial.  
   * Separe os dados de aceleração (accX, accY, accZ) utilizando a vírgula como delimitador.  
   * Verifique se a quantidade de dados recebidos é adequada (três valores). Caso contrário, imprima uma mensagem de erro.  
   * Converta os valores de string para float e armazene-os em uma lista que representa a janela deslizante.  
   * Quando a janela atingir o tamanho definido (`WINDOW_SIZE`), envie os dados para o modelo para classificação.  
   * Avance a janela conforme o valor do `STRIDE`, retendo os últimos dados relevantes.  
4. **Classificação e Resultados:**

   * A função de classificação deve utilizar o modelo carregado para classificar os dados da janela.  
   * Implemente a função `classify_data` para exibir os resultados da classificação e o tempo de processamento. Para isso:  
     * Inclua a biblioteca `edge_impulse_linux` para carregar e inicializar o modelo, utilizando: `from edge_impulse_linux.runner import ImpulseRunner`.  
     * Instancie o objeto de manipulação de modelos, informando o caminho até o `modelfile.eim` que você baixou: `runner = ImpulseRunner(model)`.
     * Implemente a função `classify_data` conforme o modelo abaixo:  
        ```bash
        def classify_data(features, runner):  
            res = runner.classify(features)  
            print("classificação:")  
            print(res["result"])  
            print("tempo:")  
            print(res["timing"])
        ```
  
## **5\. Instruções: Construindo o Script**

Modifique o template de código abaixo para implementar a lógica da classificação local de movimentos contínuos. Os pontos a serem completados estão marcados com ``## ESCREVA SEU CÓDIGO AQUI ##``.

### **Estrutura do Código (Template)**

```python

# Referência:
#      https://docs.edgeimpulse.com/docs/tools/edge-impulse-for-linux/linux-python-sdk
#      https://docs.edgeimpulse.com/docs/edge-ai-hardware/cpu/linux-x86_64
# Ajuda:
#      - Primeiro baixe o impulso completo do edge impulse com a seguinte linha de comando:
#           $ edge-impulse-linux-runner --clean --download modelfile.eim
#      - Depois execute esse script:
#           $python3 classify.py ./model.eim
#

import serial
import time
import sys  
from edge_impulse_linux.runner import ImpulseRunner

# --- Constantes de Configuração ---
SERIAL_PORT = '/dev/ttyACM0'
#SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200

# Hiperparâmetros para leitura de dados em janela deslizante
WINDOW_SIZE = 125  # Número de amostras a serem acumuladas
STRIDE = 12  # Defina o passo(stride), ou seja,
             # o número de amostras para avançar após cada classificação

def process_line(line_str):
##  Inclua aqui função que você desenvolveu na atividade anterior
    ## ESCREVA SEU CÓDIGO AQUI ##

def process_window(window_data, runner):
    res = runner.classify(window_data)
    print("classificação:")
    print(res["result"])
    print("tempo:")
    print(res["timing"])

def main():
    """
    Função principal: implementa a lógica doclassificador.
    """
    print("Iniciando Passo 4: Classificação de dados...")

    model = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "./modelfile.eim"
    )
    runner = ImpulseRunner(model)

    data_window = []
    try:
        model_info = runner.init()
        print(
            'Carregado o runner para "'
            + model_info["project"]["owner"]
            + " / "
            + model_info["project"]["name"]
            + '"'
        )
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
                
                # Verifica se a janela atingiu o tamanho necessário
                if len(data_window) >= WINDOW_SIZE * 3:
                    # Chama a função para processar os dados da janela                  
                    process_window(data_window, runner)
                    
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
        if runner:
            runner.stop()
        print("Finalizando o programa.")

if __name__ == "__main__":
    main()

```

## **Recursos Adicionais:**

* [Documentação do SDK Edge Impulse para Linux](https://docs.edgeimpulse.com/tools/libraries/sdks/inference/linux).  
* [Documentação sobre Edge AI Hardware](https://docs.edgeimpulse.com/hardware/overview).

