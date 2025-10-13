

# Classificação de Imagens com TensorFlow Lite no Raspberry Pi

Nesse roteiro de laboratório você instalará bibliotecas Python para o seu RPi incluindo TensorFlow Lite, OpenCV, Pillow e outras bibliotecas úteis para processamento de imagens.

## Requisitos
- Configure seu RPi conforme descrito no roteiro de laboratório [Configurações iniciais do RPi](../rpi_basic_config/rpi_basic_config.md)
- Instale o Edge Impulse Linux CLI conforme descrito no roteiro de laboratório [Instalação do Edge Impulse Linux CLI (Command Line Interface) no RPi](../rpi_ei_linux/rpi_ei_linux.md)
- Instale bibliotecas Python conforme descrito no roteiro de laboratório [Instalação de Bibliotecas Python para o RPi](../rpi_ei_linux_sdk/rpi_ei_linux_sdk.md)

## Passo 1: Configurar um ambiente virtual Python    
Para evitar conflitos entre bibliotecas Python, é recomendável criar um ambiente virtual dedicado para este projeto. Execute os seguintes comandos no terminal do seu Raspberry Pi:
```bash
python3 -m venv ~/tflite_env --system-site-packages
```
Ative o ambiente virtual:
```bash
source ~/tflite_env/bin/activate
```
Quando o ambiente virtual estiver ativo, você verá o nome do ambiente (neste caso, `tflite_env`) no início da linha de comando do terminal.
```bash
(tflite_env) pi@rpi0:~ $
```
Quando terminar de trabalhar no projeto, você pode desativar o ambiente virtual com o comando:
```bash
deactivate
```
## Passo 2: Instalar bibliotecas Python necessárias dentro do ambiente virtual


