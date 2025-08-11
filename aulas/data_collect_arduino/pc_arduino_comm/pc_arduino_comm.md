A listagem abaixo é um código básico para comunicação serial do seu PC com o arduino UNO:
```python
import serial
import time

# Configuração da porta serial
#port = "/dev/ttyUSB0"  # Exemplo de porta USB
port = "/dev/ttyACM1"   # Porta atualmente utilizada
# Para identificar a porta serial utilize:
#    ls -la /dev/ttyACM*
#    ls -la /dev/ttyUSB*
baudrate = 9600  # Taxa de transmissão em bits por segundo
timeout = 1      # Tempo limite para leitura (em segundos)

# Abrir a porta serial
ser = serial.Serial(port, baudrate, timeout=timeout)

def read_serial_data():
    # Função para ler dados da porta serial continuamente
    while True:
        try:
            # Lê uma linha da porta serial, decodifica e remove espaços extras
            line = ser.readline().decode("utf-8").strip()
            if line:
                print(line)  # Exibe a linha lida
        except Exception as e:
            print(f"Error: {e}")  # Exibe erro, se ocorrer
            break  # Encerra o loop em caso de erro

if __name__ == "__main__":
    try:
        read_serial_data()  # Inicia a leitura dos dados
    except KeyboardInterrupt:
        print("Parando o script.")  # Mensagem ao interromper com Ctrl+C
    finally:
        ser.close()  # Fecha a porta serial ao finalizar
```