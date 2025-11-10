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

# --- Nova Função de Processamento ---

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