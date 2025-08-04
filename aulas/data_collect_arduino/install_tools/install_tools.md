# Instalação das ferramentas de desenvolvimento

## Instalação do Arduino IDE:

1. As instruções completas para Linux estão no site: [Downloading and installing the Arduino IDE 2](https://docs.arduino.cc/software/ide-v2/tutorials/getting-started/ide-v2-downloading-and-installing/)  
2. Configurações pós-instalação:  
    - Liberar porta serial:
   ```bash
    sudo usermod -a -G dialout $USER
   ```
    - Eliminar conflito com brltty:
    ```bash
    sudo apt remove brltty
    ```

## Instalação da biblioteca do acelerômetro MPU6050

- Referência no site oficial do Arduino:  
    - [https://www.arduino.cc/reference/en/libraries/mpu6050/](https://www.arduino.cc/reference/en/libraries/mpu6050/)  
- Repositório:  
    - [https://github.com/ElectronicCats/mpu6050](https://github.com/ElectronicCats/mpu6050)  
- Documentação:  
    - [https://github.com/ElectronicCats/mpu6050/wiki](https://github.com/ElectronicCats/mpu6050/wiki)  
- Como instalar:  
    - [https://support.arduino.cc/hc/en-us/articles/5145457742236-Add-libraries-to-Arduino-IDE](https://support.arduino.cc/hc/en-us/articles/5145457742236-Add-libraries-to-Arduino-IDE)

## Instalação do Edge Impulse CLI e  Linux Python SDK

- Referência   
    - [https://docs.edgeimpulse.com/docs/tools/edge-impulse-cli/cli-installation](https://docs.edgeimpulse.com/docs/edge-impulse-cli/cli-installation)  
    - [https://github.com/edgeimpulse/linux-sdk-python](https://github.com/edgeimpulse/linux-sdk-python)  
    - [https://docs.edgeimpulse.com/docs/tools/edge-impulse-for-linux/linux-python-sdk](https://docs.edgeimpulse.com/docs/tools/edge-impulse-for-linux/linux-python-sdk)  
- Faça o download do seguinte script para instalação das ferramentas do Edge Impulse:
    ```bash
     wget https://fabiobento.github.io/sis-emb-2025-2/aulas/data_collect_arduino/install_tools/install_tools.sh
    ```    
- Conceda permissão de execução e, então,  execute o script install_tools.sh:
    ```bash
    chmod +x install_tools.sh ./install_tools.sh
    ```
- Baixar o modelo de seu projeto com

    ```bash
    edge-impulse-linux-runner --download modelfile.eim 
    ```
