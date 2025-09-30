# Instalação de Bibliotecas Python para o RPi
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

### Pyserial
O PySerial é uma biblioteca Python que encapsula o acesso à porta serial, facilitando a comunicação com dispositivos conectados via interfaces seriais, como USB. Ele é amplamente utilizado em projetos de automação, robótica e Internet das Coisas (IoT) para enviar e receber dados de sensores, microcontroladores e outros dispositivos seriais.
#### Passo 1: Instalar o PySerial
 Para instalar o PySerial, execute o seguinte comando no terminal do RPi:
```bash
pip3 install pyserial
```
#### Passo 2: Configurar permissões
Por padrão no Raspberry Pi OS, o usuário `pi` (ou o seu usuário padrão) pode não ter permissão para acessar as portas seriais, o que causaria um erro de `Permission denied`.
Para resolver isso, adicione seu usuário ao grupo dialout:
```bash
sudo usermod -a -G dialout $USER
```
Depois de executar esse comando, é necessário reiniciar o RPi para que as alterações tenham efeito:
```bash
sudo reboot
```

### **OpencV**
Instalar o OpenCV em um Raspberry Pi 3B pode ser um processo demorado, no entanto, é um passo fundamental para projetos de visão computacional.

A instalação pode ser feita de duas maneiras principais:
- usando o gerenciador de pacotes `apt` ou
- compilando a partir do código-fonte.

A seguir, detalho o método usando pacotes `apt`, o qual recomendo para a maioria dos usuários devido à sua simplicidade e rapidez.
> Se decidir compilar a partir do código-fonte, esteja ciente de que o processo pode ser demorado (pode levar de 6 a 12 horas no RPi 3B), complexo  e propenso a erros. A compilação a partir do código-fonte só é recomendada se você precisar de uma funcionalidade muito específica que não está disponível nos pacotes padrão.

Abaixo, você tem um guia completo com o método mais recomendado e atualizado: vamos usar pacotes que agilizam o processo e evitam a compilação completa, que pode levar muitas horas.

#### Passo 1: Preparar o RPi
Primeiro, é importante garantir que seu sistema operacional e firmware estejam totalmente atualizados. Abra o terminal em seu computador pessoal, reestabeleça a comunicação SSH com o RPi. Depois execute os seguintes comandos:
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
Ainda bem que as versões mais recentes do Raspberry Pi OS incluem pacotes pré-compilados para o OpenCV nos seus repositórios, o que torna a instalação muito mais rápida do que compilar do zero.

1. Instale as bibliotecas principais do OpenCV e os pacotes Python:
    ```bash
    sudo apt install python3-opencv -y
    ```
2. Para garantir que o OpenCV possa ler e escrever diferentes formatos de imagem e vídeo (como JPEG, PNG, MP4, etc.), instale as seguintes bibliotecas: 
    ```bash
    sudo apt install -y libjpeg-dev libpng-dev libtiff-dev
    sudo apt install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
    sudo apt install -y libxvidcore-dev libx264-dev
    sudo apt install -y libfontconfig1-dev libcairo2-dev
    sudo apt install -y libgdk-pixbuf2.0-dev libpango1.0-dev
    sudo apt install -y libgtk2.0-dev libgtk-3-dev
    ```
3. Instale a biblioteca ATLAS (Automatically Tuned Linear Algebra Software) pois ela ajuda a otimizar operações matemáticas:
    ```bash
    sudo apt install -y libatlas-base-dev
    ```
4. Instale a biblioteca HDF5 pois ela é útil para armazenar grandes quantidades de dados numéricos.
    ```bash
    sudo apt install -y libhdf5-dev libhdf5-103
    ```
#### Passo 4: Verificar a instalação    
Após a conclusão da instalação, é fundamental verificar se o OpenCV foi instalado corretamente e está acessível pelo Python.
1. Abra o terminal e inicie o interpretador Python 3:
    ```bash
    python3
    ```
2. No prompt do Python, tente importar o módulo `cv2` e verifique a versão instalada:
    ```python
    import cv2
    print(cv2.__version__)
    ```
3. Se o OpenCV estiver instalado corretamente, você verá a versão do OpenCV impressa no terminal, algo como `4.5.3` ou similar.
4. Saia do interpretador Python digitando:
    ```python
    exit()
    ```
#### Passo 5: Restaurar o tamanho do Swap
Manter um arquivo de swap grande pode diminuir a vida útil do seu cartão microSD. Após a instalação, é uma boa prática restaurá-lo ao tamanho original.    
1. Edite o arquivo de configuração novamente:
    ```bash
    sudo nano /etc/dphys-swapfile
    ```
2. Altere o valor de `CONF_SWAPSIZE` de volta para `100`:
    ```bash
    CONF_SWAPSIZE=100
    ```
3. Salve e saia: Pressione `Ctrl+X`, depois `Y` e `Enter`.
4. Reinicie o serviço de swap para aplicar as alterações:
    ```bash
    sudo /etc/init.d/dphys-swapfile restart
    ```    