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

### **Passo 1: Preparar o Código do Dispositivo (Exemplo Arduino)**

O Data Forwarder exige que os dados cheguem em um formato específico. Carregue no seu dispositivo o código que você desenvolveu na Parte 2 do [Roteiro de Laboratório: Leitura e Serialização de Dados do MPU-6050](./arduino_imu_comm/arduino_imu_comm.md)

### **Passo 2: Iniciar o Data Forwarder**

Com o código rodando no dispositivo, abra um terminal no seu computador e execute o comando:

```bash
edge-impulse-data-forwarder
```
### **Passo 3: Configuração Interativa**

O terminal pedirá suas credenciais e as informações do projeto. Preencha os campos conforme solicitado.

```bash
Edge Impulse data forwarder v1.18.0  
? What is your user name or e-mail address? seu-email@provedor.com  
? What is your password? \[hidden\]

\[SER\] Connecting to /dev/tty.usbmodem1234  \<-- Detectou seu dispositivo  
\[SER\] Serial is connected  
\[WS \] Connecting to wss://remote-mgmt.edgeimpulse.com  
\[WS \] Connected to wss://remote-mgmt.edgeimpulse.com

? To which project do you want to add this device? meu-projeto-acelerometro  
? 3 sensor axes detected. What do you want to call them? Separate the names with ',': accX, accY, accZ  
? What name do you want to give this device? Arduino Nano 33  
\[WS \] Authenticated. Go to https://studio.edgeimpulse.com/studio/ID\_PROJETO/acquisition/training to collect data.
```
**Observação:** Suas credenciais são usadas apenas para obter um token de autenticação e nunca são armazenadas.

### **Passo 4: Coletar os Dados**

Com o forwarder em execução, vá para o seu projeto no **Edge Impulse Studio**. Na aba **Data acquisition**, seu dispositivo aparecerá listado e pronto para a coleta de novas amostras.

---

## **5\. Comandos Adicionais Úteis**

* **Limpar a configuração anterior:** Se precisar se conectar a outro projeto ou resetar as configurações.  
  Bash  
  edge-impulse-data-forwarder \--clean

* **Forçar uma frequência de amostragem:** Caso o forwarder não a detecte corretamente. (Valor em Hz).  
  Bash  
  edge-impulse-data-forwarder \--frequency 100

* **Alterar a taxa de comunicação (baud rate):** Se seu dispositivo usa uma taxa diferente de 115200\.  
  Bash  
  edge-impulse-data-forwarder \--baud-rate 9600

## **6\. Referência**

Para mais detalhes, consulte a documentação oficial: [Edge Impulse CLI Data Forwarder](https://docs.edgeimpulse.com/docs/tools/edge-impulse-cli/cli-data-forwarder)