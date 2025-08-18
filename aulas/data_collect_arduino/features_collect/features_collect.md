
# **Roteiro de Laboratório: Extração de Features de Aceleração via Comunicação Serial**

## **Visão Geral**

O foco desta atividade é a **extração de características (raw features)** de um sensor de aceleração. Você desenvolverá um script em Python que se conecta ao hardware via porta serial para capturar dados brutos e processá-los, isolando as informações de interesse em variáveis específicas.

O diferencial deste roteiro é a ênfase na atribuição correta dos dados a variáveis que representam as características físicas do movimento: a **aceleração linear nos eixos X, Y e Z**. Esta é a etapa fundamental para qualquer projeto de análise de dados, visualização ou Machine Learning com sensores.

---
## **Requisitos Técnicos**

O script final deve ser uma implementação robusta que atenda aos seguintes requisitos:

1. **Configuração da Conexão:**  
   * Utilizar a biblioteca [`pyserial`](https://pypi.org/project/pyserial/).  
   * Configurar a porta serial com os seguintes parâmetros:
    - Porta `/dev/ttyUSB0` (ou equivalente),
    - `baud rate= 115200`,
    - `timeout=1`.  
2. **Loop de Leitura:**  
   * Ler os dados da porta serial continuamente, linha por linha.  
   * Decodificar os dados de bytes para string (padrão UTF-8).  
3. **Processamento e Validação da String:**  
   * Separar a string recebida (ex: "1.23,-0.45,9.81") em uma lista de valores, usando a vírgula (`,`) como delimitador.  
   * Validar se a lista resultante contém **exatamente três** elementos. Linhas malformadas devem ser ignoradas, exibindo uma mensagem de alerta.  
4. **Extração e Atribuição das Features (Requisito Chave):**  
   * Converter os três valores validados para o tipo `float`.  
   * Atribuir cada valor a uma **variável distinta e claramente nomeada** que represente a característica física correspondente. Exemplo: `acc_x`, `acc_y`, `acc_z`.  
5. **Exibição no Console:**  
   * Imprimir os valores das variáveis (`acc_x`, `acc_y`, `acc_z`) no console de forma limpa e organizada em cada iteração.  
6. **Tratamento de Exceções:**  
   * Implementar um bloco `try...except` para lidar com erros que possam ocorrer durante o processamento, como erro de conversão (`ValueError`) ou de acesso a índices inválidos (`IndexError`).  
7. **Encerramento Seguro:**  
   * Garantir que o script possa ser encerrado de forma limpa com **Ctrl+C** (`KeyboardInterrupt`).  
   * A porta serial **deve ser fechada corretamente** ao final da execução. O uso do gerenciador de contexto (`with`) é fortemente recomendado.  
8. **Controle de Frequência:**  
   * Adicionar um atraso de time.sleep(1/63) no final do loop para sincronizar a leitura com a taxa de amostragem do sensor.

---

#### **Recursos Adicionais**

* **Documentação PySerial:** [https://pyserial.readthedocs.io/](https://pyserial.readthedocs.io/)