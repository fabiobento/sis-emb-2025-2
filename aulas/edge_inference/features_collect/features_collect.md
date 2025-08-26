
# **Roteiro de Laboratório: Extração de Features de Aceleração via Comunicação Serial**

## **1\. Visão Geral**

O foco desta atividade é a **extração de características (raw features)** de um sensor de aceleração. Você desenvolverá um script em Python que se conecta ao hardware via porta serial para capturar dados brutos e processá-los, isolando as informações de interesse em variáveis específicas.

O diferencial deste roteiro é a ênfase na atribuição correta dos dados a variáveis que representam as características físicas do movimento: a **aceleração linear nos eixos X, Y e Z**. Esta é a etapa fundamental para qualquer projeto de análise de dados, visualização ou Machine Learning com sensores.

---
## **2\. Requisitos Técnicos**

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
---
## **3\. Instruções: Construindo o Script**

Modifique o template de código abaixo para implementar a lógica da extração de características. Os pontos a serem completados estão marcados com ``## ESCREVA SEU CÓDIGO AQUI ##``.

### **Estrutura do Código (Template)**
```python
import serial
import sys

# --- Constantes de Configuração ---
SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 115200

def process_line(line_str):
    """
    Processa uma única linha de texto: valida, extrai e converte os dados.
    Retorna uma tupla com as features (acc_x, acc_y, acc_z) ou None se for inválida.
    """
    # Divide a linha em partes usando vírgula como separador
    partes = ## ESCREVA SEU CÓDIGO AQUI ##
    if len(partes) == 3:
        try:
            # Tenta converter cada parte da linha para float
            acc_x = ## ESCREVA SEU CÓDIGO AQUI ##
            acc_y = ## ESCREVA SEU CÓDIGO AQUI ##
            acc_z = ## ESCREVA SEU CÓDIGO AQUI ##
            return [acc_x, acc_y, acc_z]
        except (ValueError, IndexError):
            # Caso haja erro na conversão, exibe aviso
            print(f"Aviso: Não foi possível converter a linha: '{line_str}'")
            return None
    else:
        # Se a linha não tiver 3 partes, exibe aviso de formato incorreto
        if line_str:
            print(f"Aviso: Linha mal formatada ignorada: '{line_str}'")
        return None

def main():
    """
    Função principal: lê dados da serial e os processa em features nomeadas.
    """
    print("Iniciando Passo 2: Extração de Features...")

    try:
        # O 'with' garante que a porta serial seja aberta e fechada automaticamente.        
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print(f"Porta serial '{SERIAL_PORT}' aberta com sucesso.")
            ser.flushInput()  # Limpa o buffer de entrada para começar do zero.

            while True:
                # Lê uma linha de bytes, decodifica para string e remove espaços.                
                line_str = ser.readline().decode('utf-8').strip()

                # Processa a linha somente se ela não estiver vazia.                
                if line_str:
                    # Processa a linha recebida e extrai as features
                    features = process_line(line_str)
                    if features:
                        acc_x, acc_y, acc_z = features
                        # Exibe os valores das features formatados
                        print(f"X: {acc_x:.2f}, Y: {acc_y:.2f}, Z: {acc_z:.2f}")

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

#### **Recursos Adicionais**

* **Documentação PySerial:** [https://pyserial.readthedocs.io/](https://pyserial.readthedocs.io/)