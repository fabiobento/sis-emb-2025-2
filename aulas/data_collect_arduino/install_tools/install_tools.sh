#!/bin/bash

# ... (toda a parte inicial do seu script continua igual) ...

# Adiciona ~/.npm-global ao PATH (opcional, para que comandos npm estejam disponíveis no terminal)
if ! grep -q 'export PATH=~/.npm-global/bin:$PATH' ~/.bashrc; then
    echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
    source ~/.bashrc
    echo "O PATH foi atualizado para incluir ~/.npm-global/bin."
else
    echo "O PATH já inclui ~/.npm-global/bin."
fi

# =================================================================
# CORREÇÃO AQUI: Instala o edge-impulse-cli SEM SUDO
echo "Instalando edge-impulse-cli globalmente..."
npm install -g edge-impulse-cli --force

# CORREÇÃO AQUI: Instala o edge-impulse-linux SEM SUDO
echo "Instalando edge-impulse-linux..."
npm install -g edge-impulse-linux --force
# =================================================================


# Garante que os scripts instalados possam ser executados
chmod +x ~/.npm-global/bin/*
echo "Permissões de execução aplicadas aos comandos do Edge Impulse."

# Instala os pacotes necessários para o PyAudio
echo "Instalando dependências do PyAudio..."
sudo apt-get install -y portaudio19-dev

# Instala o OpenCV para Python
echo "Instalando OpenCV para Python..."
pip install opencv-python

# Instala a biblioteca do Edge Impulse Linux SDK for Python e PyAudio
echo "Instalando Edge Impulse Linux SDK for Python e PyAudio..."
pip install pyaudio edge_impulse_linux

# Instala o pacote six
echo "Instalando pacote six..."
pip install six

# Instala o pacote psutil
echo "Instalando pacote psutil..."
pip install psutil

# Instala novamente portaudio19-dev (pode ser redundante)
echo "Instalando novamente portaudio19-dev..."
sudo apt-get install portaudio19-dev

# Instala a biblioteca libstdc++6
echo "Instalando libstdc++6..."
sudo apt install libstdc++6

echo "Instalação concluída!"
