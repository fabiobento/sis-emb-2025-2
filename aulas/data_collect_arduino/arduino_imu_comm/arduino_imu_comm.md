# Roteiro de Laboratório - Serialização de Dados de Sensor

## Comunicação básica do Arduino com o MPU-6050
A listagem abaixo é um código básico para leitura de sensor do sensor MPU6050 com o Arduino UNO. Carregue [esse script](./leitura_basica/leitura_basica.ino) no Arduino, e observe os resultados no monitor serial do Arduino IDE. 

```bash
#include <Wire.h>
#include <MPU6050.h> // Biblioteca para comunicação com o sensor MPU6050

#define CONVERT_G_TO_MS2    9.80665f // Fator de conversão de 'g' para m/s²

MPU6050 mpu; // Instância do objeto MPU6050 para acessar o sensor

/**
 * Função de configuração inicial do Arduino.
 * 
 * - Inicializa a comunicação serial para envio dos dados ao computador.
 * - Inicializa a comunicação I2C (Wire) para comunicação com o sensor MPU6050.
 * - Inicializa o sensor MPU6050.
 */
void setup() {
  Serial.begin(9600); // Inicializa a comunicação serial a 9600 bps
  Wire.begin();       // Inicializa a comunicação I2C
  mpu.initialize();   // Inicializa o sensor MPU6050
} 
 

/**
 * Loop principal do Arduino para leitura dos dados do acelerômetro e giroscópio via MPU.
 * 
 * - Lê os valores brutos dos sensores (ax, ay, az para acelerômetro; gx, gy, gz para giroscópio).
 * - Converte os valores do acelerômetro para unidades de gravidade (g) e depois para m/s².
 * - Converte os valores do giroscópio para graus por segundo.
 * - Imprime os valores convertidos no monitor serial, organizando por tipo de sensor.
 * - Aguarda 1 segundo antes de realizar uma nova leitura.
 */
void loop() {
  // Ler os dados do acelerômetro e giroscópio
  int16_t ax, ay, az, gx, gy, gz;
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
  
  // Converter valores brutos do acelerômetro para 'g' e depois para m/s²
  float accelX_g = ax / 16384.0; // valor em múltiplos de g
  float accelY_g = ay / 16384.0;
  float accelZ_g = az / 16384.0;
  float accelX = accelX_g * CONVERT_G_TO_MS2; // valor em m/s²
  float accelY = accelY_g * CONVERT_G_TO_MS2;
  float accelZ = accelZ_g * CONVERT_G_TO_MS2;

  // Converter valores brutos do giroscópio para graus por segundo
  float gyroX = gx / 131.0;   // valor em graus/s
  float gyroY = gy / 131.0;
  float gyroZ = gz / 131.0;

  // Imprimir os valores convertidos no monitor serial
  Serial.print("Acelerômetro (g): ");
  Serial.print(accelX);
  Serial.print(", ");
  Serial.print(accelY);
  Serial.print(", ");
  Serial.println(accelZ);
  
  Serial.print("Giroscópio (graus/s): ");
  Serial.print(gyroX);
  Serial.print(", ");
  Serial.print(gyroY);
  Serial.print(", ");
  Serial.println(gyroZ);
  
  Serial.println("-------------------");
  
  delay(1000); // Aguarda 1 segundo antes da próxima leitura
}

```
Se tudo correu bem, você observou algo parecido com isso aqui:

```bash
-------------------
Acelerômetro (g): 6.91, -0.38, -7.69
Giroscópio (graus/s): -1.08, -1.55, 1.13
-------------------
Acelerômetro (g): 6.94, -0.42, -7.70
Giroscópio (graus/s): -1.12, -1.66, 1.28
-------------------
Acelerômetro (g): 6.90, -0.46, -7.64
Giroscópio (graus/s): -0.96, -1.84, 1.50
-------------------
Acelerômetro (g): 6.86, -0.42, -7.67
Giroscópio (graus/s): -0.93, -1.66, 1.48
-------------------
```

## Preparação dos dados para o aprendizado de máquina: Serialização 
Para que essas informações possam ser utilizados em modelos de aprendizado de máquina precisamos **serializar** os dados lidos. Esse procedimento também é chamado de [*Data Ingestion*](https://docs.edgeimpulse.com/reference/data-ingestion/ingestion-api).

**Serialização** ds dados é o ato de converter os dados lidos para o formato especificado por um **protocolo**. Em nosso contexto, você estará formatando os dados dos sensores em uma string, separando os valores por vírgula ou TAB, e enviando cada conjunto de dados como uma linha única pela comunicação serial.

## Protocolo
O protocolo requerido pelos nossos modelos de aprendizado de máquina é muito simples. O dispositivo deve:
1. enviar dados na taxa de transmissão de 115.200 bps
2. com uma linha por leitura, e
3. os dados individuais do sensor devem ser divididos com uma `,` ou um caractere TAB (`\t`).
Por exemplo, esse seria o formato adequado para os dados de um acelerômetro de 3 eixos:
 ```bash
-0.12,-6.20,7.90
-0.13,-6.19,7.91
-0.14,-6.20,7.92
-0.13,-6.20,7.90
-0.14,-6.20,7.91
```

## Agora é com você!
Modifique o código básico para leitura de sensor para que os estados estejam no formato requerido pelo protocolo de comunicação.
