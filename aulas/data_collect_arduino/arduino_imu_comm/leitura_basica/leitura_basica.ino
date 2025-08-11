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
