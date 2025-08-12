# **Roteiro de Laboratório: Comunicação básica de seu computador com o Arduino**

## **1\. Objetivo**

O objetivo desta etapa é desenvolver e executar um script em Python para ler e exibir os dados de aceleração que estão sendo enviados pelo Arduino via porta serial. Isso validará a comunicação entre o hardware (Arduino) e o software no computador.

## **2\. Pré-requisitos**

1. **Python 3 instalado** em seu computador.  
2. **Biblioteca pyserial instalada.**
3. **Arduino conectado** ao computador via USB.  
4. **Código do Roteiro Anterior:** O Arduino deve estar executando o script desenvolvido no laboratório "[Serialização dos dados do sensor MPU-6050](https://www.google.com/search?q=../arduino_imu_comm/arduino_imu_comm.md)", que envia os dados do acelerômetro no formato x,y,z pela serial.

---
## **3\. Instruções Passo a Passo**
### **Passo 1: Identificar a Porta Serial do Arduino**

Antes de executar o script, você precisa saber em qual porta seu Arduino está conectado.

* **Em Linux ou macOS:** Abra o terminal e execute um dos comandos abaixo. Geralmente a porta se chama ttyACM\* ou ttyUSB\*.  
  Bash  
  ls /dev/ttyACM\*  
  \# ou  
  ls /dev/ttyUSB\*


### **Passo 2: Criar e Configurar o Script Python**

1. Crie um arquivo chamado leitor\_serial.py.  
2. Copie e cole o código-fonte abaixo no arquivo.  
3. **Ajuste a variável PORTA\_SERIAL** no início do código com o nome da porta que você identificou no passo anterior.

---

#### **4\. Código-Fonte Exemplo (leitor\_serial.py)**

Este código foi otimizado para maior clareza e robustez.

```python
import serial
import time

# --- CONFIGURAÇÕES ---
# Altere esta variável para a porta serial correta do seu Arduino.
# Exemplo Linux: "/dev/ttyACM0"
# Exemplo Windows: "COM3"
PORTA_SERIAL = "/dev/ttyACM1" 
TAXA_DE_TRANSMISSAO = 9600 # Deve ser a mesma configurada no Arduino
TIMEOUT_LEITURA = 1      # Tempo em segundos para esperar por dados

def ler_dados_seriais():
    """
    Função principal para ler e exibir os dados da porta serial continuamente.
    """
    print(f"Tentando conectar na porta {PORTA_SERIAL} a {TAXA_DE_TRANSMISSAO} bps...")

    # O bloco 'with' garante que a porta serial será fechada automaticamente.
    try:
        with serial.Serial(PORTA_SERIAL, TAXA_DE_TRANSMISSAO, timeout=TIMEOUT_LEITURA) as ser:
            print("Conexão bem-sucedida! Lendo dados... (Pressione Ctrl+C para parar)")
            
            while True:
                # Lê uma linha (até encontrar '\n'), decodifica de bytes para string
                # e remove espaços em branco no início ou fim.
                linha = ser.readline().decode('utf-8').strip()
                
                # Exibe a linha somente se ela não estiver vazia.
                if linha:
                    print(linha)

    except serial.SerialException as e:
        print(f"Erro ao abrir a porta serial: {e}")
    except KeyboardInterrupt:
        print("\nLeitura interrompida pelo usuário.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
    finally:
        print("Script finalizado.")

# Ponto de entrada do script
if __name__ == "__main__":
    ler_dados_seriais()
```
### **Passo 3: Executar o Script**

Abra um terminal na pasta onde você salvou o arquivo leitor\_serial.py e execute o comando:

```bash
python leitor\_serial.py
```
---

#### **5\. Resultado Esperado**

Se tudo estiver configurado corretamente, o terminal começará a exibir o fluxo de dados enviados pelo Arduino, com cada linha contendo os três valores de aceleração (X, Y, Z) separados por vírgula, conforme ilustrado na figura abaixo:

![Saída do Serial Monitor](./imagens/pc_python_output_protocol.png)