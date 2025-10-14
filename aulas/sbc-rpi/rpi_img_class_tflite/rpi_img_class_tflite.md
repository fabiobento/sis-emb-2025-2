

# Classificação de Imagens com TensorFlow Lite no Raspberry Pi
> Esse roteiro foi adaptado da seção [*Image Classification Fundamentals*](https://mjrovai.github.io/EdgeML_Made_Ease_ebook/raspi/image_classification/image_classification_fund.html) do [Prof. Marcelo Rovai](https://mjrovai.github.io/) no livro [*EdgeML Made Easy*](https://mjrovai.github.io/EdgeML_Made_Ease_ebook/) e do repositório do GitHub [Edge Machine Learning Systems Engineering](https://github.com/Mjrovai/UNIFEI-IESTI05-EDGE_AI/tree/main).


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