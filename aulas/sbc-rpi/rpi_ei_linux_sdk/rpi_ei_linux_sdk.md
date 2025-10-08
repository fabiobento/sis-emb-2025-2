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
---
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
---
### **JupyterLab e Jupyter Notebook (opcional)**
- O *Jupyter Notebook* é uma aplicação web que permite criar e compartilhar documentos que contêm código executável, equações, visualizações e texto narrativo. Ele é amplamente utilizado em ciência de dados, aprendizado de máquina, análise estatística e outras áreas que envolvem programação interativa.
- O *JupyterLab* é a interface de próxima geração para o Jupyter Notebook, oferecendo uma experiência mais flexível e poderosa. Ele permite que você trabalhe com múltiplos documentos e painéis em uma única interface, facilitando a organização do seu trabalho.

Este guia irá orientá-lo no processo de transformar seu Raspberry Pi 3 em um servidor de desenvolvimento para ciência de dados e Python, acessível de qualquer computador na sua rede.

#### **1\. Entendendo os Recursos: JupyterLab vs. Notebook Clássico**

Antes de instalar, é importante entender a diferença de consumo de recursos no hardware limitado do Raspberry Pi 3 (1 GB de RAM).

* **Jupyter Notebook (Clássico):**  
  * **Descrição:** A interface original, mais simples e focada em um documento por vez.  
  * **Recursos:** É **significativamente mais leve**. Consome menos RAM e CPU, resultando em uma experiência mais fluida e responsiva no RPi 3\.  
  * **Recomendação:** **Ideal para o Raspberry Pi 3**, pois deixa mais memória livre para o seu código (Pandas, NumPy, etc.), evitando lentidão.  
* **JupyterLab:**  
  * **Descrição:** A interface moderna, que funciona como um mini-ambiente de desenvolvimento (IDE) no navegador, com abas, painéis e terminal integrado.  
  * **Recursos:** É **mais pesado**. Utiliza mais RAM e CPU devido à sua arquitetura complexa. A inicialização é mais lenta e a interface pode parecer menos fluida.  
  * **Recomendação:** Use com cautela no RPi 3, ciente de que o desempenho pode ser impactado.

| Característica | JupyterLab | Jupyter Notebook (Clássico) |
| :---- | :---- | :---- |
| **Uso de RAM (Base)** | Médio a Alto | **Baixo** |
| **Uso de CPU (Interface)** | Médio | **Baixo** |
| **Funcionalidades** | **Muito Altas (IDE)** | Básicas (Editor de Notebook) |
| **Recomendação para RPi 3** | Cautelosa | **Fortemente Recomendado** |

A estratégia a seguir instalará **ambos**, permitindo que você escolha o mais adequado para cada tarefa.

#### **2\. Roteiro de Instalação (Passo a Passo)**

**Pré-requisitos**

* Raspberry Pi 3 conectado à sua rede.  
* Acesso ao terminal do RPi (via SSH ou direto com monitor/teclado).

**Passo 1: Instalar o Jupyter (Ambas as Interfaces)**

Este comando único instala o ambiente Jupyter completo, incluindo o Lab e o Notebook clássico.

```bash
pip3 install jupyterlab
```
**Solução de Problema Comum:** Se o sistema não encontrar o comando jupyter após a instalação, adicione o diretório de instalação ao PATH do seu sistema com os comandos abaixo:
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc  
source ~/.bashrc
```
#### **Passo 2: Encontrar o Endereço IP do Raspberry Pi**

Você precisará deste IP para se conectar a partir de outro computador.
```bash
hostname -I
```
Anote o endereço que aparecer (ex: 192.168.1.42).

#### **3\. Utilização Básica (Acesso Remoto)**

Agora que tudo está instalado, você pode iniciar o servidor. Escolha uma das opções abaixo.

##### **Opção A: Iniciando o Jupyter Notebook (Clássico e Leve)**

1. No terminal do RPi, execute:  
   ```bash
   jupyter notebook --ip=0.0.0.0 \--no-browser
   ```
    Onde: 
   * `--ip=0.0.0.0`: Permite conexões de qualquer dispositivo na rede.  
   * `--no-browser`: Impede que ele tente abrir um navegador no próprio RPi.  
2. O terminal exibirá uma saída com um link. Copie a URL que contém o token:
    ```bash  
   http://127.0.0.1:8888/?token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  
   ```
3. No navegador do seu computador desktop, cole a URL, mas substitua 127.0.0.1 pelo IP do seu Raspberry Pi:  
   ```bash
   http://192.168.1.42:8888/?token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
##### **Opção B: Iniciando o JupyterLab (Moderno e Completo)**

1. O processo é idêntico, mudando apenas o comando. No terminal do RPi, execute:  
   ```bash
   jupyter lab --ip=0.0.0.0 --no-browser
    ```
2. Copie a URL com o token da saída do terminal.  
3. No navegador do seu computador desktop, cole a URL, substituindo a parte inicial pelo IP do seu Raspberry Pi:  
   ```
   http://192.168.1.42:8888/lab?token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

#### **4\. Dica: Configurando uma Senha Fixa (Recomendado)**

Para não precisar copiar e colar o token toda vez, configure uma senha permanente.

1. Pare o servidor Jupyter se ele estiver rodando (Ctrl \+ C no terminal).  
2. Execute o seguinte comando para gerar os arquivos de configuração:  
   ```bash  
   jupyter server --generate-config
   ```
3. Agora, crie sua senha. O comando pedirá que você digite e confirme a senha desejada:  
   ```bash
   jupyter server password
   ```
   
Pronto\! Da próxima vez que você iniciar o jupyter notebook ou jupyter lab, basta acessar `http://<IP_DO_SEU_PI>:8888` e a interface pedirá a senha que você acabou de criar.

---
### VSCode (opcional)
O Visual Studio Code (VSCode) é um editor de código-fonte leve, mas poderoso, desenvolvido pela Microsoft. Ele é amplamente utilizado por desenvolvedores devido à sua versatilidade, suporte a várias linguagens de programação e uma vasta gama de extensões que aumentam sua funcionalidade. Para utilizar o VSCode remotamente no Raspberry Pi, siga os passos abaixo:
#### Passo 1: Instalar o VSCode no computador pessoal
1. Acesse o site oficial do [Visual Studio Code](https://code.visualstudio.com/).
2. Baixe a versão apropriada para o seu sistema operacional (Windows, macOS ou Linux).
3. Siga as instruções de instalação fornecidas no site.
#### Passo 2: Instalar a extensão "Remote - SSH"
1. Abra o VSCode no seu computador pessoal.
2. Vá para a aba de extensões clicando no ícone de quadrado no lado esquerdo ou pressionando `Ctrl+Shift+X`.
3. Na barra de pesquisa, digite "Remote - SSH".
4. Clique em "Install" para instalar a extensão.
#### Passo 3: Configurar a conexão SSH
1. Pressione `F1` ou `Ctrl+Shift+P` para abrir a paleta de comandos.
2. Digite "Remote-SSH: Connect to Host..." e selecione essa opção.
3. Clique em "Add New SSH Host...".
4. Insira o comando SSH para se conectar ao seu Raspberry Pi, por exemplo:
    ```bash
    ssh pi@rpi1.local
    ```
5. Escolha o arquivo de configuração SSH (geralmente `~/.ssh/config`).
6. Após adicionar o host, selecione-o na lista para se conectar.
7. A primeira vez que você se conectar, pode ser solicitado que você aceite a chave do host. Digite "yes" e pressione `Enter`.
8. Insira a senha do usuário do Raspberry Pi quando solicitado.
#### Passo 4: Abrir uma pasta no Raspberry Pi
1. Após a conexão, você verá uma nova janela do VSCode.
2. Vá para `File > Open Folder...` e navegue até o diretório no Raspberry Pi onde você deseja trabalhar.
3. Clique em "OK" para abrir a pasta.
#### Passo 5: **Para liberar mais recursos no RPi ao utilizar o VSCode** (RECOMENDADO)
O VSCode é uma aplicação relativamente pesada, e o Raspberry Pi 3B tem recursos limitados. Aqui estão algumas dicas para melhorar o desempenho ao usar o VSCode remotamente:
1. Execute o Raspberry Pi em Modo Totalmente `Headless` (sem *Graphical User Interphace*-GUI):  
Esta é, de longe, a melhoria mais significativa que você pode fazer. Se você só usa o RPi via SSH, a interface gráfica (GUI) pode estar desperdiçando centenas de megabytes de RAM.  
   * **Como fazer:**  
     a. Abra o terminal (via SSH) e digite:
     ```bash
     sudo raspi-config  
     ```
     b. Vá para `System Options -> Boot / Auto Login`.  
     c. Selecione a opção `Console (Autologin)`. Isso fará com que o RPi inicie diretamente na linha de comando, sem carregar o ambiente de desktop.  
   * **Resultado:** Isso libera cerca de 200-400 MB de RAM que agora estarão disponíveis para o VS Code Server, tornando a análise de código e a resposta do editor muito mais rápidas.  
2. Otimize as Configurações do Workspace no VS Code:  
O VS Code Server "monitora" a todas as pastas e arquivos do seu projeto para detectar mudanças, o que consome muita CPU. Você pode instruí-lo a ignorar diretórios que não precisam ser monitorados.  
   * **Como fazer:** Dentro do seu projeto no VS Code, crie uma pasta .vscode e dentro dela um arquivo settings.json. Adicione o seguinte conteúdo:

   ```json  
    {
    "files.watcherExclude": {
        "**/.git/objects/**": true,
        "**/.git/subtree-cache/**": true,
        "**/node_modules/*/**": true,
        "**/.venv/**": true,
        "**/__pycache__/**": true,
        "**/build/**": true,
        "**/dist/**": true
    },
    "search.exclude": {
        "**/node_modules": true,
        "**/bower_components": true,
        "**/*.code-search": true,
        "**/.venv": true,
        "**/build": true,
        "**/dist": true
    }
    }
    ```
   * **O que isso faz?** Impede que o VS Code gaste recursos monitorando e indexando pastas de dependências (`node_modules`, `.venv`), cache (`__pycache__`) ou de compilação (`build`, `dist`). A diferença na responsividade é considerável, especialmente ao abrir grandes projetos.  
3. Desative Extensões Pesadas ou Desnecessárias (no Remote):  
   Lembre-se: as extensões rodam no RPi, não no seu computador pessoal. Extensões de temas e de interface rodam localmente, mas as de linguagem (Python, C++, Docker) rodam remotamente.  
   * **Como fazer:**  
     1. Com a sessão remota conectada, vá para a aba de Extensões.  
     2. Você verá seções `Local` e `SSH: o_seu_rpi`  
     3. Desabilite no ambiente remoto (`Disable (Workspace)`) qualquer extensão que não seja absolutamente essencial para o projeto atual. O `Pylance`, por exemplo, é poderoso mas consome muita memória. Para edições rápidas, você pode desabilitá-lo temporariamente.
