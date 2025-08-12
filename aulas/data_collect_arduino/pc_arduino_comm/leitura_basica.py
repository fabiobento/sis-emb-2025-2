import serial
import time

# --- CONFIGURAÇÕES ---
# Altere esta variável para a porta serial correta do seu Arduino.
# Exemplo Linux: "/dev/ttyACM0"
# Exemplo Windows: "COM3"
PORTA_SERIAL = "/dev/ttyACM1" 
TAXA_DE_TRANSMISSAO = 115200 # Deve ser a mesma configurada no Arduino
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