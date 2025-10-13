

# Classificação de Imagens com TensorFlow Lite no Raspberry Pi

Nesse roteiro de laboratório você instalará bibliotecas Python para o seu RPi incluindo TensorFlow Lite, OpenCV, Pillow e outras bibliotecas úteis para processamento de imagens.

## Requisitos
- Configure seu RPi conforme descrito no roteiro de laboratório [Configurações iniciais do RPi](../rpi_basic_config/rpi_basic_config.md)
- Instale o Edge Impulse Linux CLI conforme descrito no roteiro de laboratório [Instalação do Edge Impulse Linux CLI (Command Line Interface) no RPi](../rpi_ei_linux/rpi_ei_linux.md)
- Instale bibliotecas Python conforme descrito no roteiro de laboratório [Instalação de Bibliotecas Python para o RPi](../rpi_ei_linux_sdk/rpi_ei_linux_sdk.md)


- Antes de iniciar a instalação, certifique-se de que o `pip` está atualizado:
    ```bash
    python -m pip install --upgrade pip
    ```
- Instale o Jupyter Notebook e Jupyter Lab:
    ```bash
    pip install jupyter jupyterlab notebook
    ```
- A maneira típica de iniciar o Jupyter Notebook é esse:
    1. Para descobrir o ip do RPi, digite no terminal dele:  
        ```bash
        hostname -I
        ```
    2. No terminal do RPi, execute:  
        ```bash
        jupyter lab --ip=0.0.0.0 --no-browser
        ```
    3. Copie a URL com o token da saída do terminal.  
    4. No navegador do seu computador desktop, cole a URL, substituindo a parte inicial pelo IP do seu Raspberry Pi:  
        ```bash
        http://192.168.1.42:8888/lab?token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        ```
- Para não precisar copiar e colar o token toda vez, configure uma senha permanente.
    1. Pare o servidor Jupyter se ele estiver rodando (`Ctrl+C` no terminal).  
    2. Execute o seguinte comando para gerar os arquivos de configuração:  
        ```bash  
        jupyter server --generate-config
        ```
    3. Agora, crie sua senha. O comando pedirá que você digite e confirme a senha desejada:  
        ```bash
        jupyter server password
        ```
    
Pronto! Da próxima vez que você iniciar o jupyter notebook ou jupyter lab, basta acessar `http://<IP_DO_SEU_PI>:8888` e a interface pedirá a senha que você acabou de criar.