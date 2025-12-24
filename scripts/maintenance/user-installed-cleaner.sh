#!/usr/bin/env bash

# ============================
# ShadowSec – User Installed Cleaner v2.1
# ============================

# Cores
RED='\e[91m'
GREEN='\e[92m'
YELLOW='\e[93m'
CYAN='\e[96m'
WHITE='\e[97m'
GRAY='\e[90m'
RESET='\e[0m'

LOG="/var/log/shadowsec-user-cleaner.log"

log() {
  echo "$(date '+%F %T') | $1" >> "$LOG"
}

# ----------------------------
# Verificação de root
# ----------------------------
if [[ "$EUID" -ne 0 ]]; then
  echo -e "${RED}[✗] Este script precisa ser executado como root.${RESET}"
  exit 1
fi

log "Script iniciado por $(whoami) em $(hostname)"

echo -e "${CYAN}[+] Coletando pacotes instalados manualmente...${RESET}"

# ----------------------------
# Coleta de pacotes
# ----------------------------
manual_pkgs=$(apt-mark showmanual)
auto_pkgs=$(apt-mark showauto)

user_pkgs=$(comm -23 <(echo "$manual_pkgs" | sort) <(echo "$auto_pkgs" | sort))

filtered_pkgs=$(echo "$user_pkgs" | grep -Ei \
'chrome|hydrogen|gimp|nmap|ncdu|vlc|kdenlive|audacity|libreoffice|telegram|obs|gparted|htop|yt-dlp|nemo|wine|q4wine|protonvpn|clamav|stellarium|playonlinux' \
| sort -u)

if [[ -z "$filtered_pkgs" ]]; then
  echo -e "${YELLOW}[!] Nenhum pacote relevante encontrado.${RESET}"
  log "Nenhum pacote relevante encontrado"
  exit 0
fi

# ----------------------------
# Proteção de pacotes sensíveis
# ----------------------------
protected_pkgs="clamav clamav-daemon ufw openssh-server network-manager"

echo -e "${GREEN}[+] Pacotes identificados:${RESET}"

count=1
declare -A pkg_map

while IFS= read -r pkg; do
  size=$(dpkg-query -W --showformat='${Installed-Size}\n' "$pkg" 2>/dev/null)
  size_mb=$(awk "BEGIN {printf \"%.1f\", ${size:-0}/1024}")

  tag="OUTRO"
  case "$pkg" in
    nmap|htop|ncdu) tag="CLI" ;;
    vlc|kdenlive|audacity|obs) tag="MÍDIA" ;;
    libreoffice*) tag="OFFICE" ;;
    clamav*) tag="SEGURANÇA" ;;
  esac

  echo -e "  ${WHITE}$count)${RESET} ${CYAN}$pkg${RESET} - ${YELLOW}${size_mb} MB${RESET} [${tag}]"
  pkg_map[$count]=$pkg
  ((count++))
done <<< "$filtered_pkgs"

echo -e "${GRAY}===========================${RESET}"

# ----------------------------
# Dry-run
# ----------------------------
read -p $'\e[96mDeseja SIMULAR a remoção antes? (s/n): \e[0m' dryrun
DRYRUN=false
if [[ "$dryrun" == "s" ]]; then
  DRYRUN=true
  log "Modo DRY-RUN ativado"
else
  log "Modo REMOÇÃO REAL selecionado"
fi

read -p $'\e[96mDeseja remover algum destes pacotes? (s/n): \e[0m' resposta
if [[ "$resposta" != "s" ]]; then
  echo -e "${GRAY}Nenhuma alteração feita.${RESET}"
  log "Operação cancelada pelo usuário"
  log "Script finalizado"
  exit 0
fi

read -p $'\e[96mDigite os números dos pacotes (separados por espaço): \e[0m' -a indices
log "Índices selecionados: ${indices[*]}"

# ----------------------------
# Remoção controlada
# ----------------------------
for i in "${indices[@]}"; do
  pkg="${pkg_map[$i]}"

  if [[ -z "$pkg" ]]; then
    echo -e "${YELLOW}[x] Índice inválido: $i${RESET}"
    log "Índice inválido informado: $i"
    continue
  fi

  log "Analisando pacote: $pkg"
  echo -e "${CYAN}[*] Pacote selecionado: $pkg${RESET}"

  echo -e "${GRAY}Dependências afetadas:${RESET}"
  apt-cache rdepends --installed "$pkg" | sed '1d'

  if echo "$protected_pkgs" | grep -qw "$pkg"; then
    echo -e "${RED}[!] ATENÇÃO: $pkg é um pacote sensível.${RESET}"
    read -p "Confirmar remoção mesmo assim? (s/n): " confirm
    if [[ "$confirm" != "s" ]]; then
      log "Pacote protegido ignorado: $pkg"
      continue
    fi
  fi

  if $DRYRUN; then
    echo -e "${YELLOW}[DRY-RUN] Simulando remoção de $pkg...${RESET}"
    apt remove --purge --simulate "$pkg"
    log "Simulação executada para: $pkg"
  else
    echo -e "${RED}[!] Removendo $pkg...${RESET}"
    apt remove --purge -y "$pkg"
    log "Pacote removido: $pkg"
  fi
done

log "Script finalizado"
echo -e "${GREEN}[✓] Operação concluída.${RESET}"
