import serial
import sys

# --- Constantes de Configuração ---
SERIAL_PORT = '/dev/ttyACM0'  # Altere para a porta correta (ex: 'COM3' no Windows)
BAUD_RATE = 115200

def main():
    """
    Função principal: conecta-se à porta serial e lê os dados brutos continuamente.
    """
    print("Iniciando Passo 1: Leitura Básica de Dados...")

    try:
        # O 'with' garante que a porta serial seja aberta e fechada automaticamente.
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print(f"Porta serial '{SERIAL_PORT}' aberta com sucesso.")
            ser.flushInput() # Limpa o buffer de entrada para começar do zero.

            while True:
                # Lê uma linha de bytes, decodifica para string e remove espaços.
                line_str = ser.readline().decode('utf-8').strip()
                
                # Exibe a linha somente se ela não estiver vazia.
                if line_str:
                    print(f"Recebido: {line_str}")

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
