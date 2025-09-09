# Instalação do Edge Impulse Linux Python *SDK*
Nesse roteiro de laboratório você instalará a biblioteca Edge Impulse Linux Python *SDK*. Ela permite executar modelos de aprendizado de máquina e coletar dados de sensores em máquinas Linux usando Python. O SDK é open source e está [hospedado no GitHub](https://github.com/edgeimpulse/linux-sdk-python).

Além disso, você instalará o [OpenCV](https://opencv.org/), uma biblioteca de visão computacional amplamente utilizada para processamento de imagens e vídeos.

## Requisitos
- Certifique de que o RPI tem Python 3(>=3.7) instalado:

    Para verificar a versão do Python 3 instalada no seu RPi e garantir que seja 3.7 ou superior, o método mais simples é usar o terminal.
    Abra o terminal no seu RPi e digite um dos seguintes comandos:
    ```bash
        python3 --version
    ```
    Ou sua forma abreviada:
    ```bash
        python3 -V
    ```
    Pressione `Enter` e a saída será algo como
    ```bash
        Python 3.9.2
    ```
    Se o número da versão exibido for `3.7.0` ou superior (como `3.8.x`, `3.9.x`, etc.), então você atende ao requisito.
- Configure seu RPi conforme descrito no roteiro de laboratório [Configurações iniciais do RPi](./rpi_basic_config/rpi_basic_config.md)
- Instale as ferramentas CLI e do SDK do Edge Impulse conforme o roteiro de laboratório [Instalação do Edge Impulse Linux CLI](./rpi_ei_linux/rpi_ei_linux.md)

## Instalação do Edge Impulse Linux Python *SDK*
Para instalar o [Edge Impulse Linux Python *SDK*](https://docs.edgeimpulse.com/tools/libraries/sdks/inference/linux/python), execute os seguintes comandos no terminal do RPi:
```bash
sudo apt-get install libatlas-base-dev libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
pip3 install edge_impulse_linux -i https://pypi.python.org/simple
pip3 install pyaudio
```
## Instalação de outras dependências

### **OpencV**
Instalar o OpenCV em um Raspberry Pi 3B pode ser um processo demorado, especialmente se você compilar a partir do código-fonte. No entanto, é um passo fundamental para projetos de visão computacional.

Abaixo, você tem um guia completo com o método mais recomendado e atualizado: vamos usar pacotes que agilizam o processo e evitam a compilação completa, que pode levar muitas horas.

#### Passo 1: Preparar o RPi
Primeiro, é importante garantir que seu sistema operacional e firmware estejam totalmente atualizados. Abra o terminal e execute os seguintes comandos:
```bash
sudo apt update
sudo apt full-upgrade -y
```
Em seguida, reinicie o RPi para garantir que todas as atualizações sejam aplicadas:
```bash
sudo reboot
```

#### Passo 2: Aumentar o espaço de Swap
A compilação ou instalação de pacotes pesados como o OpenCV pode consumir muita memória RAM. O RPi 3B tem apenas 1 GB de RAM, o que pode causar travamentos. Para evitar isso, vamos aumentar temporariamente o tamanho do arquivo de troca (swap), que funciona como uma "RAM virtual".
1. Abra o arquivo de configuração de swap:
    ```bash
    sudo nano /etc/dphys-swapfile
    ```
2. Altere o tamanho do swap. Procure pela linha `CONF_SWAPSIZE=100` e altere o valor para 2048 (ou seja, 2 GB).
    ```bash
    # set size to absolute value, leaving empty (default) then uses computed value
    #   you most likely don't want this, unless you have an special disk situation
    # CONF_SWAPSIZE=100
    CONF_SWAPSIZE=2048
    ```
3. Salve e saia: Pressione `Ctrl+X`, depois `Y` e `Enter`.
4. Aplique as alterações reiniciando o serviço de swap:
    ```bash
    sudo /etc/init.d/dphys-swapfile restart
    ```
#### Passo 3: Instalar o OpenCV e suas dependências