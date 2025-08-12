# **Roteiro de Laboratório: Ingestão de Dados com o Edge Impulse Data Forwarder**

## **1\. Objetivo**

Este roteiro ensina a usar a ferramenta edge-impulse-data-forwarder para capturar dados de um microcontrolador (como Arduino) e enviá-los em tempo real para seu projeto no Edge Impulse Studio.

## **2\. O que é o Data Forwarder?**

Pense no **Data Forwarder** como uma ponte universal entre seu dispositivo físico e a plataforma Edge Impulse.

Sua principal vantagem é a simplicidade: você não precisa implementar protocolos de comunicação complexos no seu microcontrolador. Basta que seu dispositivo escreva os dados do sensor na porta serial em um formato simples, e o Data Forwarder se encarrega do resto:

* Detecta a porta serial.  
* Autentica-se com segurança no seu projeto Edge Impulse.  
* Encaminha os dados para a plataforma, prontos para a coleta.

É a forma mais rápida de iniciar a ingestão de dados de praticamente qualquer placa de desenvolvimento.

## **3\. Pré-requisitos**

1. **Edge Impulse CLI instalado:** Se não tiver, instale com o comando: npm install \-g edge-impulse-cli.  
2. **Microcontrolador:** Um dispositivo como Arduino, ESP32, etc., conectado ao computador via USB.  
3. **Código no Microcontrolador:** Um script carregado no seu dispositivo que lê os sensores e imprime os dados na porta serial, seguindo o protocolo descrito no Passo 1\.

---

## **4\. Passo a Passo**

### **Passo 1: Preparar o código do dispositivo**

O *Data Forwarder* exige que os dados cheguem em um formato específico. Carregue no seu dispositivo o código que você desenvolveu na Parte 2 do [Roteiro de Laboratório: Leitura e Serialização de Dados do MPU-6050](../arduino_imu_comm/arduino_imu_comm.md).
Lembre-se que o protocolo é muito simples. O dispositivo deve enviar dados na taxa de transmissão de 115.200 bps com uma linha por leitura, e os dados individuais do sensor devem ser divididos com uma `,` ou um `TAB`. Por exemplo, esses são os dados de um acelerômetro de 3 eixos:
 ```bash
 -0.12,-6.20,7.90
-0.13,-6.19,7.91
-0.14,-6.20,7.92
-0.13,-6.20,7.90
-0.14,-6.20,7.91
 ```
Posteriormente o encaminhador de dados determinará automaticamente a taxa de amostragem e o número de sensores com base na saída. Se você carregar um novo aplicativo em que a frequência de amostragem ou o número de eixos seja alterado, o encaminhador de dados será reconfigurado automaticamente.

### **Passo 2: Iniciar o Data Forwarder**

Com o código rodando no dispositivo, abra um terminal no seu computador e execute o comando:

```bash
edge-impulse-data-forwarder
```
### **Passo 3: Configuração Interativa**

O terminal pedirá suas credenciais e as informações do projeto. Preencha os campos conforme solicitado.

```bash
Edge Impulse data forwarder v1.5.0
? What is your user name or e-mail address (edgeimpulse.com)? jan@edgeimpulse.com
? What is your password? [hidden]
Endpoints:
    Websocket: wss://remote-mgmt.edgeimpulse.com
    API:       https://studio.edgeimpulse.com
    Ingestion: https://ingestion.edgeimpulse.com

[SER] Connecting to /dev/tty.usbmodem401203
[SER] Serial is connected
[WS ] Connecting to wss://remote-mgmt.edgeimpulse.com
[WS ] Connected to wss://remote-mgmt.edgeimpulse.com
? To which project do you want to add this device? accelerometer-demo-1
? 3 sensor axes detected. What do you want to call them? Separate the names with ',': accX, accY, accZ
? What name do you want to give this device? Jan's DISCO-L475VG
[WS ] Authenticated
```
**Observação:** Suas credenciais são usadas apenas para obter um token de autenticação e nunca são armazenadas.

### **Passo 4: Coletar os Dados**

Com o *data forwarder* em execução, vá para o seu projeto no **Edge Impulse Studio**. Na aba **Data acquisition**, seu dispositivo aparecerá listado e pronto para a coleta de novas amostras.

---

## **5\. Comandos Adicionais Úteis**

* **Limpar a configuração anterior:** Se precisar se conectar a outro projeto ou resetar as configurações.  
```bash
  edge-impulse-data-forwarder --clean
```
* **Forçar uma frequência de amostragem:** Caso o forwarder não a detecte corretamente. (Valor em Hz).  
```bash
  edge-impulse-data-forwarder --frequency 100
```
* **Alterar a taxa de comunicação (baud rate):** Se seu dispositivo usa uma taxa diferente de 115200\.  
```bash
  edge-impulse-data-forwarder --baud-rate 9600
```
## **6\. Referência**

Para mais detalhes, consulte a documentação oficial: [Edge Impulse CLI Data Forwarder](https://docs.edgeimpulse.com/docs/tools/edge-impulse-cli/cli-data-forwarder)