# **Roteiro de Laboratório: Janela Deslizante para Análise de Dados de Acelerômetro com Python**

## **1\. Contexto**

Nos roteiros anteriores, aprendemos a:

1. **Ler e Serializar Dados:** Configurar um Arduino com um sensor MPU-6050 para enviar dados de aceleração via porta serial em um formato limpo e padronizado.  
2. **Ingestão para a Nuvem:** Utilizar o edge-impulse-data-forwarder como uma ponte para enviar esses dados diretamente para uma plataforma de Machine Learning.

Neste laboratório, vamos explorar uma abordagem alternativa e fundamental para o processamento de dados em tempo real: a **análise local**. Em vez de enviar cada leitura do sensor para a nuvem, criaremos um script em Python que captura e processa os dados diretamente no computador. Essa técnica é a base para muitas aplicações de Machine Learning embarcado, onde as decisões precisam ser tomadas localmente no dispositivo.

## **2\. Objetivo**

O objetivo é desenvolver um script em Python que leia os dados de aceleração enviados pelo Arduino, organize-os em blocos de tamanho fixo usando uma **janela deslizante** e simule uma rotina de processamento para cada bloco.

Ao final, você terá aprendido a:

* Estabelecer comunicação serial entre um dispositivo (Arduino) e um script Python.  
* Implementar o conceito de janela deslizante (sliding window) para agrupar dados de sensores.  
* Estruturar um código robusto para processamento contínuo de dados em tempo real.

## **3\. Pré-requisitos**

1. **Hardware Configurado:** O Arduino deve estar carregado com o código final da **Parte 2 do Roteiro de Leitura e Serialização**, enviando os dados do acelerômetro no formato x,y,z na taxa de 115200 bps.  
2. **Python 3:** Instalado em seu computador.  
3. **Biblioteca pyserial:** Instale-a com o seguinte comando no seu terminal:  
   Bash  
   pip install pyserial

---

## **4\. Conceito-Chave: A Janela Deslizante (Sliding Window)**

Para analisar dados de sensores que chegam continuamente, como os de um acelerômetro, raramente olhamos para uma única amostra isolada. Em vez disso, analisamos um pequeno "pedaço" de tempo, ou uma **janela**, para entender o contexto do que está acontecendo.

A janela deslizante funciona assim:

1. **Coleta:** Acumulamos um número fixo de amostras (ex: 100 leituras) em uma lista. Isso é o WINDOW\_SIZE.  
2. **Processamento:** Uma vez que a janela está cheia, executamos nossa lógica sobre ela (neste caso, apenas imprimimos os dados).  
3. **Deslize:** Para a próxima iteração, não descartamos a janela inteira. Mantemos uma parte dos dados mais recentes e removemos apenas os mais antigos. A quantidade de dados novos que esperamos para encher a janela novamente é o **passo** (STRIDE).

**Exemplo:** Com WINDOW\_SIZE \= 10 e STRIDE \= 4:

* **Janela 1:** \[d1, d2, d3, d4, d5, d6, d7, d8, d9, d10\] \-\> Processa.  
* Descarta os 4 primeiros (STRIDE), mantém os 6 últimos.  
* **Próxima Janela:** \[d7, d8, d9, d10, d11, d12, d13, d14, d15, d16\] \-\> Processa.

## **5\. Instruções: Construindo o Script**

Modifique o template de código abaixo para implementar a lógica da janela deslizante. Os pontos a serem completados estão marcados com TODO.

### **Estrutura do Código (Template)**

```bash
import serial  
import time

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
    if window\_data:  
        print(f"Primeira amostra: {window_data[0]}")  
        print(f"Última amostra: {window_data[-1]}")  
    print("--------------------------------------------------\n")

def main():  
    """  
    Função principal que lê da serial e gerencia a janela deslizante.  
    """  
    print("Iniciando leitor de dados seriais...")  
      
    # Lista para armazenar os dados da janela atual  
    data\_window = []

    try:  
        # TODO 1: Inicie e abra a comunicação serial usando as constantes definidas.  
        # Dica: use serial.Serial() com os parâmetros corretos.  
        # Adicione um 'with' para garantir que a porta seja fechada automaticamente.  
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:  
            print(f"Porta serial {SERIAL_PORT} aberta com sucesso.")  
              
            # Limpa qualquer dado residual no buffer da serial  
            ser.flushInput()

            while True:  
                # TODO 2: Leia uma linha da porta serial.  
                # Dica: use ser.readline()  
                line = ser.readline()

                # TODO 3: Decodifique a linha de bytes para string (use 'utf-8') e remova espaços/quebras de linha.  
                # Dica: use .decode('utf-8').strip()  
                try:  
                    line_str = line.decode('utf-8').strip()

                    # Ignora linhas vazias  
                    if not line_str:  
                        continue  
                      
                    # TODO 4: Separe os valores da linha usando a vírgula como delimitador.  
                    # Dica: use .split(',')  
                    parts = line_str.split(',')

                    # TODO 5: Verifique se a linha contém exatamente 3 valores.  
                    # Se não, imprima um aviso e continue para a próxima linha.  
                    if len(parts) == 3:  
                        # Converte os valores para float e os adiciona à janela  
                        accel_data = [float(p) for p in parts]  
                        data_window.append(accel_data)  
                    else:  
                        print(f"Aviso: Linha mal formatada ignorada: '{line_str}'")  
                        continue

                except (UnicodeDecodeError, ValueError) as e:  
                    print(f"Erro ao processar a linha: {line}. Erro: {e}")  
                    continue

                # TODO 6: Verifique se a janela atingiu o tamanho definido (WINDOW_SIZE).  
                if len(data\_window) >= WINDOW_SIZE:  
                    # Se a janela estiver cheia, processe os dados  
                    process_window(data_window)  
                      
                    # TODO 7: Implemente o "deslize".  
                    # Mantenha apenas os dados mais recentes na janela, descartando os mais antigos.  
                    # A nova janela deve ser uma fatia da janela antiga.  
                    # Dica: data_window = data_window[STRIDE:]  
                    data_window = data\_window\[STRIDE:]

    except serial.SerialException as e:  
        print(f"Erro: Não foi possível abrir a porta serial {SERIAL_PORT}. Verifique a conexão. Detalhes: {e}")  
    except KeyboardInterrupt:  
        print("\nPrograma encerrado pelo usuário.")  
    finally:  
        print("Fim do programa.")

if __name__ \== "__main__":  
    main()
```

## **6\. Entrega e Avaliação**

Para concluir a tarefa, você deve:

1. **Completar o código-fonte** em Python com a lógica funcional.  
2. **Escrever um breve relatório** respondendo às seguintes perguntas:  
   * Como a sua implementação da janela deslizante (data_window = data_window[STRIDE:]) garante que os dados mais antigos sejam descartados e os mais novos mantidos?  
   * Qual foi a maior dificuldade que você encontrou ao desenvolver o script e como a resolveu?  
   * Cite duas aplicações práticas onde um sistema que processa dados em janelas (em vez de amostra por amostra) seria vantajoso.

A avaliação será baseada no funcionamento correto do código, na clareza da implementação, no tratamento de erros e na qualidade das respostas no relatório.