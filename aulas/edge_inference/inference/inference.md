# **Roteiro de Laboratório: Implementação de Classificação de Dados de Aceleração em Tempo Real usando Edge Impulse**

## **Descrição**:
** Nesta tarefa, você deverá desenvolver um código em Python que realiza a leitura de dados de aceleração em tempo real a partir de um sensor conectado via porta serial. Os dados coletados serão processados por um modelo de classificação treinado na plataforma Edge Impulse. O objetivo é aplicar técnicas de Machine Learning para classificar os dados em tempo real e avaliar o desempenho da classificação.

##
**Objetivo:** Elaborar um script em Python que:

* Leia continuamente dados de aceleração (accX, accY, accZ) de um sensor conectado via porta serial.  
* Armazene os dados em uma janela deslizante.  
* Utilize o SDK do Edge Impulse para classificar os dados coletados, retornando os resultados em tempo real.  
* Exiba os resultados da classificação e o tempo necessário para processar cada janela de dados.

## **Instruções:**

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
  
5. **Execução e Encerramento:**

   * Certifique-se de que o script pode ser encerrado de maneira segura, fechando a porta serial e parando o runner do Edge Impulse.

## **Entrega:**

* O código-fonte completo em Python.  
* Um breve relatório explicando:  
  * A implementação do processo de classificação em tempo real.  
  * O desempenho observado durante os testes (tempo de processamento e precisão).  
  * Possíveis dificuldades encontradas e como foram resolvidas.

## **Avaliação:** A tarefa será avaliada com base nos seguintes critérios:

* **Funcionamento correto do código**.  
* **Implementação adequada da janela deslizante e integração com o modelo Edge Impulse**.  
* **Clareza no tratamento de erros e na exibição dos resultados**.  
* **Estrutura e organização do código**.  
* **Explicação detalhada no relatório**.

## **Recursos Adicionais:**

* Documentação do SDK Edge Impulse para Linux.  
* Documentação sobre Edge AI Hardware.

