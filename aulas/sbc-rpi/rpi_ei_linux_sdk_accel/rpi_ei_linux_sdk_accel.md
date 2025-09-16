# **Roteiro de Laboratório: Classificação de Dados de Aceleração em Tempo Real usando bibliotecas Python no RPi**

## **1\. Objetivo**

Neste roteiro de laboratório, você vai executar no Raspberry Pi (RPi) os códigos Python desenvolvidos em roteiros anteriores. O objetivo é fazer funcionar, em um sistema embarcado (o RPi), as soluções para comunicação serial, extração de características, implementação de janela deslizante e classificação de dados de aceleração em tempo real usando a plataforma Edge Impulse.

## **2\. Pré-requisitos**

Para este laboratório, o Raspberry Pi e o Arduino já devem estar configurados e com os códigos e ferramentas necessários:

* **Raspberry Pi (RPi) Configurado:** O RPi deve ter sido preparado nos seguintes roteiros:  
  * [**"Instalação do Sistema Operacional"**](../rpi_basic_config/rpi_basic_config.md): O Raspberry Pi OS (preferencialmente a versão Legacy 32-bit baseada em Debian Bullseye) deve estar instalado no cartão SD. O RPi deve estar acessível remotamente via SSH e VNC, e o módulo de câmera deve estar configurado.  
  * [**"Instalação do Edge Impulse Linux CLI e SDK no Raspberry Pi"**](../rpi_ei_linux/rpi_ei_linux.md): As ferramentas do Edge Impulse CLI (como `edge-impulse-data-forwarder`) e o Edge Impulse para Linux (como `edge-impulse-linux-runner`) devem estar instaladas e configuradas no RPi. O Node.js v16.x+ também deve ter sido instalado.  
  * [**"Instalação de Bibliotecas Python para o RPi"**](../rpi_ei_linux_sdk/rpi_ei_linux_sdk.md): O Python 3 (versão 3.7 ou superior), a biblioteca `pyserial` e o `OpenCV` devem estar instalados no RPi. As permissões para acesso à porta serial (`dialout` group) também devem estar configuradas, exigindo a reinicialização do RPi.  
* **Arduino UNO com Código de Serialização:** O Arduino UNO com o sensor MPU-6050 deve estar executando o código desenvolvido no roteiro [**"Roteiro de Laboratório: Leitura e Serialização de Dados do MPU-6050"**](../../data_collect_arduino/arduino_imu_comm/arduino_imu_comm.md). Este código deve enviar os dados de aceleração (accX, accY, accZ) em uma única linha, separados por vírgulas, a uma taxa de 115200 bps. Essa serialização de dados é muito importante para que as informações possam ser utilizadas em modelos de aprendizado de máquina.

## **3\. Materiais Necessários**

* Raspberry Pi 3 (ou superior) com cartão microSD.  
* Fonte de alimentação para o Raspberry Pi.  
* Arduino UNO com sensor MPU-6050 conectado.  
* Cabo USB para conectar o Arduino ao Raspberry Pi.  
* Um computador desktop para acesso remoto ao RPi (via VNC ou SSH).

## **4\. Procedimento Detalhado**

### **Parte 1: Comunicação Serial Básica do RPi com o Arduino**

*(Baseado no ["Roteiro de Laboratório: Comunicação básica de seu computador com o Arduino"](../../edge_inference/pc_arduino_comm/pc_arduino_comm.md))*

**Objetivo:** Validar que o Raspberry Pi consegue se comunicar corretamente com o Arduino via porta serial e ler os dados de aceleração.

1. **Conectar o Arduino ao RPi:**  
   * Com o Arduino UNO já com o código de serialização de dados do acelerômetro carregado e executando, conecte-o a uma das portas USB do Raspberry Pi.  
2. **Acessar o Terminal do RPi:**  
   * Abra uma sessão de terminal no seu RPi. Isso pode ser feito via SSH a partir do seu computador desktop (ex: `ssh pi@rpi<seu_hostname>.local`) ou através do VNC Viewer, abrindo o aplicativo Terminal no ambiente gráfico do RPi.  
3. **Identificar a Porta Serial do Arduino no RPi:**

No terminal do RPi, execute um dos seguintes comandos para listar as portas seriais disponíveis. A porta do Arduino geralmente aparece como `/dev/ttyACM*` ou `/dev/ttyUSB*`.  
```bash 
ls /dev/ttyACM\*  
ls /dev/ttyUSB\*
```
  * Anote o nome da porta identificada (ex: `/dev/ttyUSB0` ou `/dev/ttyACM0`).  
4. **Criar o Script Python `leitor_serial.py`:**  
   * No RPi, crie um novo arquivo Python chamado `leitor_serial.py` (você pode usar um editor de texto como `nano` ou `vim` no terminal, ou um IDE se estiver via ssh ou VNC).  
   * Copie e cole o código-fonte fornecido no ["Roteiro de Laboratório: Comunicação básica de seu computador com o Arduino"](../../edge_inference/pc_arduino_comm/pc_arduino_comm.md).  
   * **Ajuste a variável `PORTA_SERIAL`** no início do código Python com o nome da porta que você identificou no passo anterior. Certifique-se também que o `baudrate` está configurado para `115200`, conforme o protocolo do Arduino.  
   * Salve o arquivo.  
5. **Executar o Script:**  
   * No terminal do RPi, navegue até a pasta onde salvou o arquivo `leitor_serial.py`.

Execute o script Python com o comando:  
```bash
python3 leitor_serial.py
```
  * **Resultado Esperado:** O terminal do RPi deverá começar a exibir o fluxo de dados de aceleração (X, Y, Z) enviados pelo Arduino, com cada linha contendo os três valores separados por vírgula. Se ocorrer um erro de permissão, revise a configuração do grupo `dialout` e a reinicialização do RPi, conforme o roteiro [**"Instalação de Bibliotecas Python para o RPi"**](../rpi_ei_linux_sdk/rpi_ei_linux_sdk.md).  
  * Pressione `Ctrl+C` para encerrar o script de forma segura.

### **Parte 2: Extração de Features de Aceleração via Comunicação Serial no RPi**

*(Baseado no "[Roteiro de Laboratório: Extração de Features de Aceleração via Comunicação Serial](../../edge_inference/features_collect/features_collect.py)")*

**Objetivo:** Adaptar o script para extrair e atribuir corretamente as características de aceleração a variáveis nomeadas, lidando com o processamento e validação dos dados da porta serial. A **extração de características** é crucial para transformar dados brutos em informações mais significativas e concisas para o modelo de ML, reduzindo a complexidade computacional.

1. **Criar o Script Python `extrai_features.py`:**  
   * No RPi, crie um novo arquivo Python chamado `extrai_features.py`.  
   * Copie o código que você desenvolveu no roteiro "[Roteiro de Laboratório: Extração de Features de Aceleração via Comunicação Serial](../../edge_inference/features_collect/features_collect.py)").  
   * Salve o arquivo.  
2. **Executar o Script:**
Execute o script no terminal do RPi:  
```bash
 python3 extrai_features.py
```
   
  * **Resultado Esperado:** O script deve exibir de forma organizada os valores de aceleração para cada eixo (acc\_x, acc\_y, acc\_z) no console, indicando que as características foram extraídas com sucesso.  
  * Pressione `Ctrl+C` para encerrar.

### **Parte 3: Janela Deslizante para Análise de Dados de Acelerômetro com Python no RPi**

*(Baseado no "[Roteiro de Laboratório: Janela Deslizante para Análise de Dados de Acelerômetro com Python"](../../edge_inference/sliding_window/sliding_window.py))*

**Objetivo:** Implementar o conceito de **janela deslizante (sliding window)** para agrupar os dados de aceleração coletados, simulando um processamento em blocos. A janela deslizante permite analisar um "pedaço" de tempo dos dados, crucial para entender o contexto do movimento, ao invés de amostras isoladas.

1. **Criar o Script Python `janela_deslizante.py`:**  
   * No RPi, crie um novo arquivo Python chamado `janela_deslizante.py`.  
   * Copie o código que você desenvolveu no roteiro "[Roteiro de Laboratório: Janela Deslizante para Análise de Dados de Acelerômetro com Python"](../../edge_inference/sliding_window/sliding_window.py)".  
   * Salve o arquivo.  
2. **Executar o Script:**

Execute o script no terminal do RPi:  
```bash
 python3 janela\_deslizante.py
```
  * **Resultado Esperado:** O script deverá imprimir os "blocos" de dados de aceleração, representando as janelas completas, à medida que são coletadas e "processadas". Isso demonstra que os dados estão sendo acumulados e preparados para inferência.  
  * Pressione `Ctrl+C` para encerrar.

### **Parte 4: Implementação de Classificação de Dados de Aceleração em Tempo Real Usando Edge Impulse no RPi**

*(Baseado no "[Roteiro de Laboratório: Implementação de Classificação de Dados de Aceleração em Tempo Real usando Edge Impulse"](../../edge_inference/inference/inference.md))*

**Objetivo:** Utilizar um modelo de Machine Learning treinado na plataforma Edge Impulse para classificar os dados de aceleração em tempo real diretamente no RPi. Este passo integra o pipeline completo de ML embarcado, onde o modelo, antes treinado na nuvem, é implantado e executado localmente no dispositivo para fazer inferências rápidas e autônomas.

1. **Contexto do Modelo Edge Impulse:**  
   * O Edge Impulse permite criar sistemas de **reconhecimento de gestos**. Assume-se que você já treinou um modelo de classificação (um "impulso") no Edge Impulse Studio, utilizando dados de acelerômetro para reconhecer diferentes movimentos (ex: "updown", "snake", "wave", "idle"). O pipeline de ML (impulso) inclui blocos de **processamento de sinal** (como Análise Espectral) e um **bloco de aprendizado** (como Classificação de Rede Neural).  
2. **Baixar o Modelo `.eim` para o RPi:**

No terminal do RPi, use o comando fornecido no roteiro para baixar o modelo treinado do seu projeto Edge Impulse para o RPi. O arquivo será salvo como `modelfile.eim` no diretório atual. O `edge-impulse-linux-runner` é a ferramenta focada na implantação e execução de modelos `.eim` otimizados para a arquitetura do Linux.  
 edge-impulse-linux-runner \--clean \--download modelfile.eim

*   
  * Certifique-se de que a conexão à internet do RPi esteja ativa para o download.  
3. **Crie um Script Python `classifica_aceleracao.py`:**  
   * Cole no script o código que você desenvolveu no roteiro "[Roteiro de Laboratório: Implementação de Classificação de Dados de Aceleração em Tempo Real usando Edge Impulse"](../../edge_inference/inference/inference.md)".
   * Salve o arquivo.  
4. **Executar o Script:**
No terminal do RPi, execute o script Python, passando o modelo `.eim` como argumento:  
```bash
python3 classifica\_aceleracao.py modelfile.eim
```
  * **Resultado Esperado:** O script deverá exibir no terminal as classificações em tempo real dos movimentos detectados pelo acelerômetro (ex: "idle", "updown", "snake", "wave"), juntamente com a probabilidade associada a cada gesto e o tempo necessário para realizar a inferência (classificação). Isso demonstra que o modelo de ML está funcionando localmente no RPi.  
  * Pressione `Ctrl+C` para encerrar.
