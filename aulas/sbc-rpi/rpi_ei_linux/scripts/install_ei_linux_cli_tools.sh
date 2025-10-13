#!/bin/bash

# Script para automatizar a instalação do Edge Impulse Linux CLI e SDK
# com base no documento rpi_ei_linux.md

echo "----------------------------------------------------"
echo "Passo 2: Atualizando o Sistema..."
echo "----------------------------------------------------"
sudo apt update -y

echo "----------------------------------------------------"
echo "Passo 3: Instalando Node.js e dependências..."
echo "----------------------------------------------------"
# Adiciona o repositório do Node.js v22.x
echo "Adicionando repositório do Node.js..."
curl -sL https://deb.nodesource.com/setup_22.x | sudo -E bash -

# Instala o Node.js e outras dependências
echo "Instalando Node.js, GCC, G++, Make, SOX e GStreamer..."
sudo apt install -y gcc g++ make build-essential nodejs sox gstreamer1.0-tools gstreamer1.0-plugins-good gstreamer1.0-plugins-base gstreamer1.0-plugins-base-apps

# Verifica a versão do Node.js
echo "Verificando a versão do Node.js..."
node -v

echo "----------------------------------------------------"
echo "Configurando o diretório global do NPM..."
echo "----------------------------------------------------"
# Cria o diretório e configura o prefixo para o npm
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'

# Adiciona o novo diretório ao PATH no .profile para que os comandos fiquem disponíveis
# A verificação 'grep' evita que a linha seja adicionada múltiplas vezes
if ! grep -q "export PATH=~/.npm-global/bin:\$PATH" ~/.profile; then
  echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.profile
  echo "Diretório NPM adicionado ao seu ~/.profile."
else
  echo "O diretório NPM já está no seu ~/.profile."
fi

# Exporta o PATH para a sessão atual, para que os próximos comandos funcionem
export PATH=~/.npm-global/bin:$PATH
echo "PATH atualizado para a sessão atual."

echo "----------------------------------------------------"
echo "Passo 4: Instalando o Edge Impulse CLI..."
echo "----------------------------------------------------"
# Instala a CLI principal do Edge Impulse
npm install edge-impulse-cli -g --unsafe-perm

echo "----------------------------------------------------"
echo "Passo 5: Instalando o Edge Impulse para Linux..."
echo "----------------------------------------------------"
# Instala as ferramentas de inferência para Linux
npm install edge-impulse-linux -g --unsafe-perm

echo "----------------------------------------------------"
echo "Instalação concluída com sucesso!"
echo ""
echo "Para garantir que as alterações de PATH sejam permanentes,"
echo "feche e reabra seu terminal ou execute o comando:"
echo "source ~/.profile"
echo ""
echo "Depois, você pode verificar a instalação com os comandos:"
echo "edge-impulse-data-forwarder --clean"
echo "edge-impulse-linux --clean"
echo "----------------------------------------------------"