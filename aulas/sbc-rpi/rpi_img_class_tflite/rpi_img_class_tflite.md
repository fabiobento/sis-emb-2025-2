

# Classificação de Imagens com TensorFlow Lite no Raspberry Pi
> Esse roteiro foi adaptado da seção [*Image Classification Fundamentals*](https://mjrovai.github.io/EdgeML_Made_Ease_ebook/raspi/image_classification/image_classification_fund.html) do [Prof. Marcelo Rovai](https://github.com/Mjrovai) no livro [*EdgeML Made Easy*](https://mjrovai.github.io/EdgeML_Made_Ease_ebook/) e do repositório do GitHub [Edge Machine Learning Systems Engineering](https://github.com/Mjrovai/UNIFEI-IESTI05-EDGE_AI/tree/main).


## Criação de um primeiro Notebook jupyter no Raspberry Pi
- Inicie um servidor no Raspberry Pi conforme descrito na seção "JupyterLab e Jupyter Notebook" do roteiro de laboratório [Instalação de Bibliotecas Python para o RPi](../rpi_ei_linux_sdk/rpi_ei_linux_sdk.md).
- Defina o diretório de trabalho no Raspberry Pi e crie um novo notebook Python 3:
    ```bash
    cd  ~/Documents
    mkdir Python
    ```
- Crie um novo notebook Python 3 chamado `primeiro-notebook-jupyter.ipynb`, entre com o código abaixo:
    ```python
    import time
    import numpy as np
    from PIL import Image
    improt matplotlib.pyplot as plt
    from picamera2 import Picamera2
    ```
## Carregar e exibir uma imagem da internet
- Carregar uma imagem da internet, por exemplo (note que é possível executar linhas de comando de dentro no Notebook, usando ! antes do comando):
    ```python
    !wget https://upload.wikimedia.org/wikipedia/commons/3/3a/Cat03.jpg
    ```    
- A imagem (`Cat03.jpg`) foi baixada para o diretório de trabalho do Notebook. Vamos abrir e exibir a imagem:
    ```python
    img_path = "Cat03.jpg"
    title = "Imagem baixada da internet"
    img = Image.open(img_path)

    #Exibir a imagem
    plt.figure(figsize=(6,6))
    plt.imshow(img)
    plt.title(title)
    plt.axis('off')  # Esconder os eixos
    plt.show()
    ```
## Capturar e exibir uma imagem local capturada pela câmera do RPi
- Agora, vamos utilizar a camera do RPi para capturar uma imagem local:
    ```python
    from picamera2 import Picamera2
    import time

    # Initialize camera
    picam2 = Picamera2()
    picam2.start()

    # Wait for camera to warm up
    time.sleep(2)

    # Capture image
    picam2.capture_file("class_test.jpg")
    print("Imagem capturada : class_test.jpg")

    # Stop camera
    picam2.stop()
    picam2.close()
    ```
- E use um código similar ao código anterior para motrar a imagem(adaptando as variáveis `img_path` e `title`):

    ```python
    img_path = "class_test.jpg"
    title = "Imagem capturada pela câmera do RPi"
    img = Image.open(img_path)

    #Exibir a imagem
    plt.figure(figsize=(6,6))
    plt.imshow(img)
    plt.title(title)
    plt.axis('off')  # Esconder os eixos
    plt.show()
    ```
## Classificação de imagens com TensorFlow Lite
- A seguir, vamos carregar um modelo pré-treinado do TensorFlow Lite e usá-lo para classificar as imagens capturadas. Para maiores detalhes sobre o Tensorflow Lite consulte essa [Visão geral do LiteRT](https://www.tensorflow.org/lite) e o [Guia de início rápido para dispositivos baseados em Linux com Python](https://ai.google.dev/edge/litert/microcontrollers/python?hl=pt-br)

### Crie um novo diretório pra trabalho
- Crie um novo diretório de trabalho no Raspberry Pi:
    ```bash
    mkdir Documents
    cd Documents/
    mkdir TFLITE
    cd TFLITE/
    mkdir IMG_CLASS
    cd IMG_CLASS
    mkdir models
    cd models
    ```
### Baixe o modelo pré-treinado MobileNetV2    

- Um modelo pré-treinado adequado é muito importante para o sucesso da classificação de imagens em dispositivos com recursos limitados, como o Raspberry Pi.
- O [*MobileNet*](https://github.com/tensorflow/models/tree/master/research/slim/nets/mobilenet) foi projetado para aplicações móveis e de visão embarcada, com um bom equilíbrio entre precisão e velocidade
- Várias versões estão disponíveis: `MobileNetV1`, `MobileNetV2`, `MobileNetV3`. Vamos baixar a V2:
    ```bash
    wget https://storage.googleapis.com/download.tensorflow.org/models/tflite_11_05_08/mobilenet_v2_1.0_224_quant.tgz

    tar xzf mobilenet_v2_1.0_224_quant.tgz
    ```
- Agora vamos baixar também os rótulos (labels) das classes:
    ```bash
    wget https://raw.githubusercontent.com/Mjrovai/EdgeML-with-Raspberry-Pi/refs/heads/main/IMG_CLASS/models/labels.txt
    ```
### Carregue o modelo e os rótulos no Notebook    