# 🛡️ ShadowSec – User Installed Cleaner

Script de manutenção defensiva para identificação, auditoria e remoção controlada de pacotes instalados manualmente em sistemas Debian/Ubuntu.

Este módulo não automatiza decisões críticas: ele fornece contexto técnico para que o operador escolha com segurança o que remover.

## 📌 Visão Geral

O user-installed-cleaner.sh foi projetado para:

Identificar pacotes marcados como manuais pelo APT

Filtrar softwares tipicamente instalados pelo usuário

Exibir tamanho em disco, categoria funcional e dependências afetadas

Oferecer simulação (dry-run) antes de qualquer remoção

Proteger pacotes sensíveis contra remoção acidental

Registrar ações em log auditável

⚠️ O script não remove nada automaticamente.

## 🧠 Conceitos Técnicos Utilizados
🔹 apt-mark showmanual

Lista pacotes considerados manuais pelo gerenciador de pacotes.

“Manual” ≠ “instalado conscientemente pelo usuário”
Significa apenas que o pacote não é dependência automática.

🔹 Exclusão de pacotes automáticos
comm -23 <(manual) <(auto)


Garante que dependências não apareçam como candidatas.

🔹 Filtro explícito

Somente softwares de interesse comum ao usuário final são exibidos, reduzindo risco de remoção de componentes do sistema.

## ⚙️ Funcionalidades
### ✔️ Verificação de privilégios

O script exige root:

if [[ "$EUID" -ne 0 ]]; then
  exit 1
fi

### ✔️ Classificação funcional dos pacotes

Cada pacote recebe uma tag:

Tag	Descrição
CLI	Ferramentas de linha de comando
MÍDIA	Áudio, vídeo, edição
OFFICE	Suítes de escritório
SEGURANÇA	Ferramentas de proteção
OUTRO	Não classificado

Exemplo:

3) nmap - 4.3 MB [CLI]

### ✔️ Cálculo de espaço ocupado

Utiliza:

dpkg-query -W --showformat='${Installed-Size}'


Resultado convertido para MB.

### ✔️ Visualização de dependências afetadas

Antes da remoção:

apt-cache rdepends --installed pacote


Permite avaliar impacto real no sistema.

### ✔️ Modo Dry-Run (Simulação)

Simula a remoção sem alterar o sistema:

apt remove --purge --simulate pacote


Recomendado sempre antes da remoção real.

### ✔️ Proteção de pacotes sensíveis

Pacotes críticos exigem confirmação extra:

clamav
clamav-daemon
ufw
openssh-server
network-manager


Isso evita perda de acesso remoto, firewall ou proteção ativa.

### ✔️ Log auditável

Arquivo:

/var/log/shadowsec-user-cleaner.log


Registra:

data e hora

hostname

usuário

pacotes removidos

Exemplo:

2025-12-24 19:42:11 | REMOVIDO: vlc

## 🧪 O que o script não faz

🚫 Não remove dependências automaticamente

🚫 Não gerencia Snap ou Flatpak

🚫 Não executa limpeza sem confirmação

🚫 Não decide o que é “seguro” remover

Ele informa, o operador decide.

## 🖥️ Requisitos

Debian / Ubuntu / derivados

bash

apt, apt-mark, dpkg-query

Execução como root

## ▶️ Uso
chmod +x user-installed-cleaner.sh
sudo ./user-installed-cleaner.sh


Fluxo:

Coleta de pacotes

Exibição com tamanho e categoria

Opção de simulação

Seleção por índice

Remoção controlada (opcional)

## 🔒 Considerações de Segurança

Este script foi projetado com foco em:

Prevenção de erro humano

Transparência operacional

Auditabilidade

Controle manual

Ideal para:

ambientes pessoais

hardening pós-instalação

auditorias leves

manutenção consciente

### ⚠️ Aviso

Remover pacotes pode impactar o sistema.
Use este script apenas se você entende o que está removendo.

### 📈 Histórico de Versões
v1.0

Listagem básica de pacotes manuais

Remoção direta por seleção

v2.0

Modo dry-run

Proteção de pacotes sensíveis

Visualização de dependências

Classificação funcional

Log persistente

Refatoração de segurança


