import cv2
import imagezmq
import socket
from picamera2 import Picamera2
import time

# --- CONFIGURAÇÃO ---
# 1. Altere para o IP do seu DESKTOP
IP_DO_DESKTOP = "tcp://XXX.XXX.XXX.XXX:5555" 

# 2. Configurações da Câmera
LARGURA_IMG = 1280
ALTURA_IMG = 720
# --- FIM DA CONFIGURAÇÃO ---

print("Iniciando cliente da câmera...")

# Conecta-se ao servidor no desktop
try:
    sender = imagezmq.ImageSender(connect_to=IP_DO_DESKTOP)
except Exception as e:
    print(f"Erro ao conectar ao servidor {IP_DO_DESKTOP}")
    print("Verifique se o IP está correto e se o script 'servidor_processamento.py' está em execução no desktop.")
    print(f"Erro: {e}")
    exit()


# Obtém o nome do RPi para identificar no servidor
nome_rpi = socket.gethostname()
print(f"Conectado ao servidor. Enviando como '{nome_rpi}'")

# Inicializa a Picamera2
picam2 = Picamera2()
config = picam2.create_video_configuration(main={"size": (LARGURA_IMG, ALTURA_IMG)})
picam2.configure(config)
picam2.start()

# Dá um tempo para a câmera "aquecer"
time.sleep(2.0)
print("Câmera iniciada. Enviando frames...")

try:
    while True:
        # Captura um frame como um array numpy
        # 'capture_array()' retorna um array RGB
        frame_rgb = picam2.capture_array()
        
        # O OpenCV (e seu código) espera BGR. Precisamos converter.
        frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

        # Envia o frame para o desktop e espera a resposta 'OK'
        # Isso sincroniza o RPi e o Desktop, evitando sobrecarga de rede
        reply = sender.send_image(nome_rpi, frame_bgr)
        
        # Opcional: Adicionar um pequeno delay se o processamento for muito rápido
        # time.sleep(0.1) 

except (KeyboardInterrupt, SystemExit):
    print("Encerrando cliente...")
finally:
    picam2.stop()
    sender.close()
    print("Cliente finalizado.")