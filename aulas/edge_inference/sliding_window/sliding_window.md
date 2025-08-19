# **Roteiro de Laboratório: Implementação de Janela Deslizante para Processamento de Dados de Aceleração**

## **Descrição:**
Nesta tarefa, você será responsável por desenvolver um código em Python que realiza a leitura de dados de aceleração em tempo real a partir de um sensor conectado via porta serial.
O objetivo principal é implementar um mecanismo de janela deslizante para armazenar e processar um conjunto de dados antes de avançar para o próximo.

## **Objetivo:**
Elaborar um script em Python que:
* Leia continuamente dados de aceleração (accX, accY, accZ) de um sensor conectado via porta serial.  
* Armazene esses dados em uma janela deslizante com tamanho definido.  
* Avance a janela de acordo com um passo (stride) predefinido após cada ciclo de processamento.

## **Instruções:**

1. **Configuração Serial:**

   * Utilize a biblioteca `pyserial` para configurar e abrir a comunicação serial.  
   * Configure a porta serial com os seguintes parâmetros: `/dev/ttyUSB0`, `baudrate=115200`, `timeout=1`.  
2. **Implementação da Janela Deslizante:**

   * Implemente uma função que leia continuamente as linhas recebidas na porta serial.  
   * Separe os dados de aceleração (accX, accY, accZ) utilizando a vírgula como delimitador.  
   * Verifique se a quantidade de dados recebidos é adequada (três valores). Caso contrário, imprima uma mensagem de erro.  
   * Converta os valores de string para float e armazene-os em uma lista que representa a janela deslizante.  
   * Quando a janela atingir o tamanho definido (`WINDOW_SIZE`), processe os dados (por exemplo, imprimir os valores) e deslize a janela conforme o valor do `STRIDE`.  
   * Garanta que a janela retenha os últimos `STRIDE` valores após o processamento, descartando os dados mais antigos.  
3. **Tratamento de Erros:**
   * Adicione tratamento de exceções para lidar com possíveis erros durante a leitura e conversão dos dados.  
   * Implemente uma maneira segura de encerrar o script, assegurando que a porta serial seja fechada corretamente.  
4. Taxa de Amostragem:
   * Utilize `time.sleep(1 / 63)` para manter a taxa de amostragem dos dados em 63 Hz.

## **Entrega:**

* **O código-fonte completo em Python**.  
* **Um breve relatório explicando**:  
  * A implementação da janela deslizante.  
  * Possíveis dificuldades encontradas e como foram resolvidas.  
  * Aplicações práticas de um sistema com janela deslizante.

## **Avaliação:** A tarefa será avaliada com base nos seguintes critérios:

* Funcionamento correto do código.  
* Implementação adequada da janela deslizante.  
* Clareza no tratamento de erros.  
* Estrutura e organização do código.  
* Explicação detalhada no relatório.

