Usar um dispositivo de borda (o Raspberry Pi) para captura e um computador mais potente (o Desktop) para o processamento pesado é uma arquitetura muito comum em projetos de Visão Computacional e IoT.

A forma mais eficiente e simples de fazer isso é usando a biblioteca **imagezmq**. Ela é otimizada exatamente para este caso de uso: enviar frames OpenCV de um computador (RPi) para outro (Desktop) pela rede com o mínimo de latência e complexidade.

Aqui está como você pode estruturar seu projeto:

### ** Pré-requisitos**

1. **No seu Desktop:**  
   Bash  
   pip install imagezmq  
   \# Você já deve ter opencv-python, pytesseract, etc.

2. **No seu Raspberry Pi:**  
   Bash  
   \# Recomendo a versão "headless" se você não for usar a GUI no RPi  
   pip install opencv-python-headless  
   pip install imagezmq  
   pip install picamera2

---

### ** Lado do Desktop (Servidor)**

Este script irá receber os frames, processá-los com a função que criamos e exibir o resultado.

Crie um arquivo chamado servidor\_processamento.py no seu desktop. Ele deve conter **todo o código anterior** (net\_create, tesseract\_setup, processar\_frame\_para\_texto, etc.) e, em vez da função main, ele terá o seguinte:

Python

\# \[COLE AQUI TODO O CÓDIGO ANTERIOR\]  
\# import cv2, pytesseract, imutils, os, gdown, np, urllib.request  
\# def download\_detector(...):  
\# def tesseract\_setup(...):  
\# def preprocessar\_para\_ocr(...):  
\# def tesseract\_OCR(...):  
\# def net\_create(...):  
\# def dados\_geometricos(...):  
\# def calculos\_geometria(...):  
\# def net\_forward(...):  
\# def processar\_frame\_para\_texto(...):  
\# \[FIM DO CÓDIGO ANTERIOR\]

import imagezmq  
import traceback

def iniciar\_servidor():  
    print("Iniciando servidor de processamento...")  
      
    \#\#\#\# CONFIGURAÇÃO (Executado apenas uma vez) \#\#\#\#  
    CONFIG\_TESSERACT \= "--tessdata-dir tessdata \--psm 7"  
    NET\_LARGURA \= 320  
    NET\_ALTURA \= 320  
    MARGEM\_ROI \= 5  
      
    print("Iniciando configuração do Tesseract...")  
    tesseract\_setup(CONFIG\_TESSERACT)  
      
    print("Iniciando carregamento da rede neural...")  
    rede\_neural \= net\_create()  
    print("Servidor pronto para receber imagens.")  
    print("-" \* 30)

    \# Inicializa o ImageHub para receber imagens  
    image\_hub \= imagezmq.ImageHub()  
      
    try:  
        while True:  
            \# Espera por um frame do Raspberry Pi  
            (nome\_rpi, frame) \= image\_hub.recv\_image()  
              
            \# Confirma o recebimento (desbloqueia o RPi)  
            image\_hub.send\_reply(b'OK')

            \# Processa o frame recebido  
            frame\_processado, texto\_encontrado \= processar\_frame\_para\_texto(  
                frame,   
                rede\_neural,   
                CONFIG\_TESSERACT,   
                NET\_LARGURA,   
                NET\_ALTURA,   
                MARGEM\_ROI,  
                lang='eng' \# ou 'por'  
            )  
              
            if texto\_encontrado:  
                print(f"Texto detectado \[de {nome\_rpi}\]: {texto\_encontrado}")

            \# Opcional: Mostrar o vídeo processado no desktop  
            cv2.imshow("Processamento no Desktop", frame\_processado)  
            if cv2.waitKey(1) & 0xFF \== ord('q'):  
                break  
                  
    except (KeyboardInterrupt, SystemExit):  
        print("Encerrando servidor...")  
    except Exception as e:  
        print("Erro no servidor:")  
        print(traceback.format\_exc())  
    finally:  
        cv2.destroyAllWindows()  
        print("Servidor finalizado.")

if \_\_name\_\_ \== "\_\_main\_\_":  
    iniciar\_servidor()

---

### ** Lado do Raspberry Pi (Cliente)**

Este script irá capturar a imagem da câmera e enviá-la para o IP do seu desktop.

Crie um arquivo chamado cliente\_camera.py no seu Raspberry Pi.

Python

import cv2  
import imagezmq  
import socket  
from picamera2 import Picamera2  
import time

\# \--- CONFIGURAÇÃO \---  
\# 1\. Altere para o IP do seu DESKTOP  
IP\_DO\_DESKTOP \= "tcp://192.168.1.100:5555" 

\# 2\. Configurações da Câmera  
LARGURA\_IMG \= 1280  
ALTURA\_IMG \= 720  
\# \--- FIM DA CONFIGURAÇÃO \---

print("Iniciando cliente da câmera...")

\# Conecta-se ao servidor no desktop  
try:  
    sender \= imagezmq.ImageSender(connect\_to=IP\_DO\_DESKTOP)  
except Exception as e:  
    print(f"Erro ao conectar ao servidor {IP\_DO\_DESKTOP}")  
    print("Verifique se o IP está correto e se o script 'servidor\_processamento.py' está em execução no desktop.")  
    print(f"Erro: {e}")  
    exit()

\# Obtém o nome do RPi para identificar no servidor  
nome\_rpi \= socket.gethostname()  
print(f"Conectado ao servidor. Enviando como '{nome\_rpi}'")

\# Inicializa a Picamera2  
picam2 \= Picamera2()  
config \= picam2.create\_video\_configuration(main={"size": (LARGURA\_IMG, ALTURA\_IMG)})  
picam2.configure(config)  
picam2.start()

\# Dá um tempo para a câmera "aquecer"  
time.sleep(2.0)  
print("Câmera iniciada. Enviando frames...")

try:  
    while True:  
        \# Captura um frame como um array numpy  
        \# 'capture\_array()' retorna um array RGB  
        frame\_rgb \= picam2.capture\_array()  
          
        \# O OpenCV (e seu código) espera BGR. Precisamos converter.  
        frame\_bgr \= cv2.cvtColor(frame\_rgb, cv2.COLOR\_RGB2BGR)

        \# Envia o frame para o desktop e espera a resposta 'OK'  
        \# Isso sincroniza o RPi e o Desktop, evitando sobrecarga de rede  
        reply \= sender.send\_image(nome\_rpi, frame\_bgr)  
          
        \# Opcional: Adicionar um pequeno delay se o processamento for muito rápido  
        \# time.sleep(0.1) 

except (KeyboardInterrupt, SystemExit):  
    print("Encerrando cliente...")  
finally:  
    picam2.stop()  
    sender.close()  
    print("Cliente finalizado.")

### ** Instruções de Execução**

1. **Descubra o IP do seu Desktop:**  
   * No Linux/macOS: ifconfig ou ip a  
   * No Windows: ipconfig  
   * Procure pelo endereço IPv4 da sua conexão (Wi-Fi ou Ethernet). Ex: 192.168.1.100.  
2. **Atualize o IP no Raspberry Pi:**  
   * Edite o arquivo cliente\_camera.py e mude o valor da variável IP\_DO\_DESKTOP para o IP que você encontrou.  
3. **Execute o Servidor (Desktop):**  
   * Abra um terminal no seu desktop e execute:  
     Bash  
     python servidor\_processamento.py

   * Você deverá ver as mensagens de configuração e, por fim, "Servidor pronto para receber imagens."  
4. **Execute o Cliente (Raspberry Pi):**  
   * Abra um terminal no seu Raspberry Pi (pode ser por SSH, como você já faz) e execute:  
     Bash  
     python cliente\_camera.py

Agora, o Raspberry Pi começará a capturar imagens, enviá-las para o seu desktop, e o desktop irá processá-las, imprimir o texto e mostrar o vídeo com as detecções.