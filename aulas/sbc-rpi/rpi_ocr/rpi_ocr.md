# OCR Distribuído com Raspberry Pi e `imagezmq`
Usar um dispositivo de borda (o Raspberry Pi) para captura e um computador mais potente (o Desktop) para o processamento pesado é uma arquitetura muito comum em projetos de Visão Computacional e IoT.

Uma forma muito eficiente e simples de fazer isso é usando a biblioteca [imagezmq](https://pypi.org/project/imagezmq/). Ela é otimizada exatamente para o seguinte caso de uso: enviar frames OpenCV de um computador para outro pela rede com o mínimo de latência e complexidade. 

Por isso, nesse tutorial, você vai implementar um sistema de OCR distribuído usando Raspberry Pi para captura de imagens e um desktop para processamento.

## Introdução
### O que é imagezmq? 

[imagezmq](https://pypi.org/project/imagezmq/) é um conjunto de classes Python leve, rápido e multiplataforma (funciona em RPi, Jetson Nano, Linux, Mac, Windows) projetado para uma tarefa muito específica:
- transportar imagens OpenCV de um computador para outro pela rede usando a biblioteca de mensageria ZMQ (ZeroMQ).

Ele foi criado exatamente para o cenário de "computação distribuída" que estamos implementando: múltiplos dispositivos de borda (como RPi com câmeras) capturando imagens e as enviando para um servidor central mais potente (seu desktop) para processamento pesado, como nosso OCR.

Aqui estão alguns pontos-chave sobre o imagezmq:
#### 1. Padrões de Mensageria: REQ/REP vs. PUB/SUB

Isso é o mais importante: imagezmq oferece dois modos de comunicação.
* **Padrão REQ/REP (Request/Reply):**  
  * **Como funciona:** O cliente (RPi) envia uma imagem (REQ) e **obrigatoriamente espera** por uma resposta (REP) do servidor (Desktop) antes de poder enviar a próxima imagem.  
  * **Nosso Código:** É **exatamente** o que estamos usando. O RPi usa ` sender.send_image() e fica "bloqueado" até receber o `image_hub.send_reply(b'OK')` do servidor.  
  * **Vantagem:** É ótimo para sincronização. O RPi não vai sobrecarregar o servidor ou a rede, pois ele só envia um novo frame quando o servidor confirma que terminou o processamento (ou pelo menos recebeu) o anterior.  
* **Padrão PUB/SUB (Publish/Subscribe):**  
  * **Como funciona:** O cliente (RPi) "publica" (envia) frames de vídeo o mais rápido que pode, sem se importar se o servidor os recebeu. Ele **não espera por nenhuma resposta**.  
  * **Vantagem:** Permite uma taxa de quadros (FPS) muito mais alta, pois não há bloqueio.  
  * **Desvantagem:** Se o servidor for mais lento que o cliente, ele começará a perder frames. Não há garantia de entrega.

#### 2. Estrutura da Mensagem: (texto, imagem)
As mensagens enviadas não são apenas a imagem. Elas são um **tupla (texto, imagem)**.
* O **imagem** é o frame do OpenCV, que o imagezmq comprime em JPEG por padrão para economizar banda de rede.  
* O **texto** é uma string usada para identificação. No nosso script, estamos usando o `nome_rpi` (hostname) nesse campo. Isso é pois porque permite que o servidor (ImageHub) receba frames de *múltiplos* clientes e saiba quem enviou o quê.

#### **3\. O "Hub"**
O componente do servidor é chamado de **ImageHub** (e não ImageReceiver) por um motivo: ele é projetado para atuar como um "hub" central, recebendo e organizando imagens de *muitos* emissores (ImageSender) simultaneamente.

## Pré-requisitos

1. No seu desktop, a essa altura do curso, você já deve ter instalado o OpenCV e outras ferramentas durante o roteiro [Instalação das ferramentas de desenvolvimento](../../data_collect_arduino/install_tools/install_tools.md). Instale mais algumas bibliotecas necessárias:  
   ```bash
   pip install imagezmq  pytesseract imutils gdown
   ```

2. No seu RPi você também já deve ter instalado várias ferramentas no roteiro [Instalação de Bibliotecas Python para o RPi](../rpi_ei_linux_sdk/rpi_ei_linux_sdk.md). Instale mais alguns dependências:*  
   ```bash
   pip install imagezmq pytesseract
   ```

## Teste de Streaming de Vídeo com Flask no RPi
Utilize o script [`cam-stream.py`](https://raw.githubusercontent.com/fabiobento/sis-emb-2025-2/refs/heads/main/aulas/sbc-rpi/rpi_ocr/scripts/cam-stream.py) abaixo no RPi para testar o streaming de vídeo simples com Flask no seu RPi, garantindo que a câmera está funcionando corretamente.

```python
import cv2
from picamera2 import Picamera2
from flask import Flask, Response
import time

# --- Configuração do Servidor Flask ---
app = Flask(__name__)

# --- Configuração da Câmera ---
camera = Picamera2()
config = camera.create_video_configuration(main={"size": (640, 480), "format": "RGB888"})
camera.configure(config)
camera.start()
time.sleep(1.0)  # Tempo para a câmera inicializar

def generate_frames():
    """Gera frames de vídeo para o stream MJPEG."""
    print("Iniciando geração de frames...")
    while True:
        try:
            # 1. Captura o frame (formato RGB)
            img_rgb = camera.capture_array()
            
            # 2. Converte de RGB (Picamera2) para BGR (OpenCV)
            img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
            
            # 3. Codifica o frame BGR para o formato JPEG
            ret, buffer = cv2.imencode('.jpg', img_bgr)
            
            if not ret:
                print("Erro ao codificar frame")
                continue
            
            # 4. Converte o buffer para bytes
            frame_bytes = buffer.tobytes()
            
            # 5. "Entrega" (yield) o frame no formato MJPEG
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                   
        except Exception as e:
            # Se o cliente desconectar (ex: fechar o navegador), 
            # uma exceção pode ocorrer aqui. O break garante que o loop pare.
            # print(f"Erro no loop de geração de frames: {e}") 
            break
    print("Geração de frames parada.")

# --- Rotas do Servidor Web ---

@app.route('/')
def index():
    """Página principal que exibe o stream de vídeo."""
    return """
    <html>
    <head>
        <title>RPi - Video Stream</title>
        <style>
            body { font-family: sans-serif; text-align: center; padding-top: 20px; }
            img { border: 2px solid #333; }
        </style>
    </head>
    <body>
        <h1>Streaming de Vídeo(RPi)</h1>
        <img src="/video_feed" width="640" height="480">
    </body>
    </html>
    """

@app.route('/video_feed')
def video_feed():
    """A rota que fornece o stream de vídeo MJPEG."""
    return Response(generate_frames(), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# --- Ponto de Entrada Principal (MODIFICADO) ---
if __name__ == "__main__":
    print("Iniciando servidor web...")
    print("Pressione Ctrl+C para sair.")
    
    try:
        # Inicia o servidor Flask
        app.run(host='0.0.0.0', port=5000, threaded=True)
        
    except KeyboardInterrupt:
        # Captura o Ctrl+C para uma saída limpa
        print("\nServidor interrompido pelo usuário.")
        
    finally:
        # Este bloco é EXECUTADO SEMPRE, garantindo que a câmera seja liberada
        print("Limpando recursos... Parando a câmera.")
        camera.stop()
        camera.close()
        print("Recursos liberados. Saindo.")
```

## Lado do Desktop (Servidor)

Vamos iniciar pelo lado do desktop, que irá receber as imagens do RPi, processá-las com OCR e exibir o resultado.

Crie um arquivo chamado [`servidor_processamento.py`](https://raw.githubusercontent.com/fabiobento/sis-emb-2025-2/refs/heads/main/aulas/sbc-rpi/rpi_ocr/scripts/servidor_processamento.py) no seu desktop com o seguinte código:
```python
import cv2
import pytesseract
import imutils
from imutils.object_detection import non_max_suppression
import os
import gdown
import numpy as np
import urllib.request

def download_detector(url, output):
    """Verifica se o arquivo já existe antes de baixá-lo."""
    if not os.path.exists(output):
        print(f"Baixando {output}...")
        urllib.request.urlretrieve(url, output)
        print("Download concluído!")
    else:
        print(f"Arquivo {output} já existe, não é necessário fazer o download.")

def tesseract_setup(config_tesseract="--tessdata-dir tessdata --psm 7"):
    """Baixa e configura os dados de idioma do Tesseract."""
    os.makedirs('./tessdata', exist_ok=True)
    
    # URL do arquivo do detector em PORTUGUÊS
    url_por = 'https://github.com/tesseract-ocr/tessdata/blob/main/por.traineddata?raw=true'
    output_por = './tessdata/por.traineddata'
    download_detector(url_por, output_por)
    
    # URL do arquivo do detector em INGLÊS
    url_eng = 'https://github.com/tesseract-ocr/tessdata/blob/main/eng.traineddata?raw=true'
    output_eng = './tessdata/eng.traineddata'
    download_detector(url_eng, output_eng)

def preprocessar_para_ocr(img):
    """Pre-processa uma imagem (ROI) para melhor desempenho do OCR."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Aumentar a imagem pode ajudar o Tesseract a ler fontes pequenas
    maior = cv2.resize(gray, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
    valor, otsu = cv2.threshold(maior, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    return otsu

def tesseract_OCR(roi, config_tesseract, lang='por'):
    """Executa OCR em uma Região de Interesse (ROI) pre-processada."""
    # Garante que a ROI não está vazia
    if roi.shape[0] == 0 or roi.shape[1] == 0:
        return ""
        
    preprocess_roi = preprocessar_para_ocr(roi)
    texto = pytesseract.image_to_string(preprocess_roi, lang=lang, config=config_tesseract)
    return texto

def net_create(detector='./Modelos/frozen_east_text_detection.pb'):
    """Baixa o modelo EAST e o carrega na memória."""
    os.makedirs('./Modelos', exist_ok=True)
    
    # Verifica se o arquivo já existe
    if not os.path.exists(detector):
        print("Baixando modelo EAST...")
        url = 'https://drive.google.com/uc?id=1-RbGz-8K7kC_Fve6J0eLtcRZQhmKS3UQ'
        gdown.download(url, detector, quiet=False)
        print("Download do modelo concluído!")
    else:
        print("Arquivo frozen_east_text_detection.pb já existe.")
        
    # Carregar o modelo neural EAST
    return cv2.dnn.readNet(detector)

# --- Funções Auxiliares da Rede Neural EAST ---

def dados_geometricos(geometry, y):
    xData0 = geometry[0, 0, y]
    xData1 = geometry[0, 1, y]
    xData2 = geometry[0, 2, y]
    xData3 = geometry[0, 3, y]
    data_angulos = geometry[0, 4, y]
    return data_angulos, xData0, xData1, xData2, xData3

def calculos_geometria(x, y, data_angulos, xData0, xData1, xData2, xData3):
    (offsetX, offsetY) = (x * 4.0, y * 4.0)
    angulo = data_angulos[x]
    cos = np.cos(angulo)
    sin = np.sin(angulo)
    h = xData0[x] + xData2[x]
    w = xData1[x] + xData3[x]

    fimX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
    fimY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))

    inicioX = int(fimX - w)
    inicioY = int(fimY - h)
    return inicioX, inicioY, fimX, fimY

def net_forward(img,
                rede_neural,
                min_confianca=0.90,
                nomes_camadas=['feature_fusion/Conv_7/Sigmoid', 'feature_fusion/concat_3']):
    """Executa a detecção de texto (EAST) na imagem."""
    blob = cv2.dnn.blobFromImage(img, 1.0, (img.shape[1], img.shape[0]), swapRB=True, crop=False)
    rede_neural.setInput(blob)
    scores, geometry = rede_neural.forward(nomes_camadas)
    
    linhas, colunas = scores.shape[2:4]
    caixas = []
    confiancas = []
    
    for y in range(0, linhas):
        data_scores = scores[0, 0, y]
        data_angulos, xData0, xData1, xData2, xData3 = dados_geometricos(geometry, y)
        
        for x in range(0, colunas):
            if data_scores[x] < min_confianca:
                continue
            
            inicioX, inicioY, fimX, fimY = calculos_geometria(x, y, data_angulos, xData0, xData1, xData2, xData3)
            confiancas.append(data_scores[x])
            caixas.append((inicioX, inicioY, fimX, fimY))
            
    return non_max_suppression(np.array(caixas), probs=confiancas)

def processar_frame_para_texto(frame, rede_neural, config_tesseract, 
                               net_width, net_height, 
                               margem=5, lang='por'):
    """
    Processa um único frame para detectar e extrair texto.

    Argumentos:
        frame: A imagem de entrada (OpenCV).
        rede_neural: O modelo EAST carregado.
        config_tesseract: A string de configuração do Tesseract.
        net_width: A largura que a rede EAST espera.
        net_height: A altura que a rede EAST espera.
        margem: Margem (em pixels) para adicionar ao redor da caixa de detecção.
        lang: Idioma para o Tesseract ('por', 'eng', etc.).

    Retorna:
        Tuple: (frame_processado, texto_completo)
        - frame_processado: O frame original com as caixas de detecção desenhadas.
        - texto_completo: Uma string com todo o texto encontrado, separado por espaços.
    """
    # Cria uma cópia para desenhar e extrair ROIs
    copia_frame = frame.copy()
    (H, W) = frame.shape[:2]

    # Calcula a proporção para redimensionar as caixas de volta ao tamanho original
    proporcao_W = W / float(net_width)
    proporcao_H = H / float(net_height)

    # Redimensiona a imagem para o tamanho esperado pela rede neural
    img_redimensionada = cv2.resize(frame, (net_width, net_height))

    # Executa a detecção de texto
    deteccoes = net_forward(img_redimensionada, rede_neural)
    
    textos_extraidos = []

    for (inicioX, inicioY, fimX, fimY) in deteccoes:
        # Redimensiona as coordenadas da caixa de volta ao tamanho original
        inicioX_orig = int(inicioX * proporcao_W)
        inicioY_orig = int(inicioY * proporcao_H)
        fimX_orig = int(fimX * proporcao_W)
        fimY_orig = int(fimY * proporcao_H)

        # Adiciona uma margem e garante que a ROI não saia dos limites da imagem
        roi_inicioY = max(0, inicioY_orig - margem)
        roi_inicioX = max(0, inicioX_orig - margem)
        roi_fimY = min(H, fimY_orig + margem)
        roi_fimX = min(W, fimX_orig + margem)

        # Extrai a ROI do frame *original*
        roi = copia_frame[roi_inicioY:roi_fimY, roi_inicioX:roi_fimX]

        # Executa o Tesseract na ROI
        texto = tesseract_OCR(roi, config_tesseract, lang=lang)
        
        texto_limpo = texto.strip()
        if texto_limpo:
            textos_extraidos.append(texto_limpo)
            
        # Desenha a caixa de detecção (sem a margem) no frame
        cv2.rectangle(copia_frame, (inicioX_orig, inicioY_orig), (fimX_orig, fimY_orig), (0, 255, 0), 2)

    # Junta todos os textos encontrados em uma única string
    texto_completo = " ".join(textos_extraidos)
    
    return copia_frame, texto_completo

import imagezmq
import traceback

def iniciar_servidor():
    print("Iniciando servidor de processamento...")
    
    #### CONFIGURAÇÃO (Executado apenas uma vez) ####
    CONFIG_TESSERACT = "--tessdata-dir tessdata --psm 7"
    NET_LARGURA = 320
    NET_ALTURA = 320
    MARGEM_ROI = 5
    
    print("Iniciando configuração do Tesseract...")
    tesseract_setup(CONFIG_TESSERACT)
    
    print("Iniciando carregamento da rede neural...")
    rede_neural = net_create()
    print("Servidor pronto para receber imagens.")
    print("-" * 30)

    # Inicializa o ImageHub para receber imagens
    image_hub = imagezmq.ImageHub()
    
    try:
        while True:
            # Espera por um frame do Raspberry Pi
            (nome_rpi, frame) = image_hub.recv_image()
            
            # Confirma o recebimento (desbloqueia o RPi)
            image_hub.send_reply(b'OK')

            # Processa o frame recebido
            frame_processado, texto_encontrado = processar_frame_para_texto(
                frame, 
                rede_neural, 
                CONFIG_TESSERACT, 
                NET_LARGURA, 
                NET_ALTURA, 
                MARGEM_ROI,
                lang='eng' # ou 'por'
            )
            
            if texto_encontrado:
                print(f"Texto detectado [de {nome_rpi}]: {texto_encontrado}")

            # Opcional: Mostrar o vídeo processado no desktop
            cv2.imshow("Processamento no Desktop", frame_processado)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except (KeyboardInterrupt, SystemExit):
        print("Encerrando servidor...")
    except Exception as e:
        print("Erro no servidor:")
        print(traceback.format_exc())
    finally:
        cv2.destroyAllWindows()
        print("Servidor finalizado.")

if __name__ == "__main__":
    iniciar_servidor()
```
## Lado do Raspberry Pi (Cliente)

Este script irá capturar a imagem da câmera e enviá-la para o IP do seu desktop.

Crie um arquivo chamado `cliente_camera.py  no seu RPi.

```python
import cv2
import imagezmq
import socket
from picamera2 import Picamera2
import time

# --- CONFIGURAÇÃO ---
# 1. Altere para o IP do seu DESKTOP
IP_DO_DESKTOP = "tcp://XXX.XXX.XX.XX:5555" 

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
```

## Instruções de Execução

1. **Descubra o IP do seu Desktop:**  
   * No Linux/macOS: `hoistname -I`, `ifconfig` ou `ip a` 
   * No Windows: `ipconfig` 
   * Procure pelo endereço `IPv4` da sua conexão (*Wi-Fi* ou Ethernet). Ex: $192.168.1.100$.  
2. **Atualize o IP no Raspberry Pi:**  
   * Edite o arquivo `cliente_camera.py` e mude o valor da variável `IP_DO_DESKTOP` para o IP que você encontrou.  
3. **Execute o Servidor (Desktop):**  
   * Abra um terminal no seu desktop e execute:  
    ```bash
     python servidor_processamento.py
     ```

   * Você deverá ver as mensagens de configuração e, por fim, `Servidor pronto para receber imagens.`  
4. **Execute o Cliente (RPi):**  
   * Abra um terminal no seu RPi (pode ser por `SSH`, como você já faz) e execute:  
    ```bash
     python cliente_camera.py
    ```

Agora, o RPi começará a capturar imagens, enviá-las para o seu desktop, e o desktop irá processá-las, imprimir o texto e mostrar o vídeo com as detecções.
