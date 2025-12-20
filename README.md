# 🛡️ ShadowSec Toolkit • Core

![OS Compatibility](https://img.shields.io/badge/OS-Linux%20|%20Windows-blueviolet.svg)

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)

![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)

![License](https://img.shields.io/badge/license-MIT-green.svg)

## Framework Modular de Cibersegurança, para Auditoria, Hardening e Monitoramento local, com foco em arquitetura sólida, extensibilidade e operação controlada.

Autor: Luciano Valadão (Lukk)
Projeto: ShadowSec Offensive & Defensive Tools

## Documentação de arquitetura:

docs/ARCHITECTURE.md


## Visão Geral

O ShadowSec evoluiu de um conjunto de scripts isolados para um framework orientado a módulos (plugin-based), capaz de carregar dinamicamente funcionalidades de segurança sem acoplamento ao núcleo da aplicação.

### O projeto foi concebido para:

Analistas de cibersegurança

Profissionais de TI

Administradores de sistemas

Ambientes corporativos ou pessoais

Cenários offline ou restritos

Nenhuma funcionalidade é executada sem contexto explícito.

## Objetivos do Core

Padronizar execução e retorno de módulos

Garantir previsibilidade e segurança estrutural

Facilitar expansão (CLI, GUI, Mobile, API)

Servir como base profissional para ferramentas ShadowSec

Separar orquestração de lógica de segurança

## Princípios Arquiteturais

🔹 Arquitetura orientada a plugins

🔹 Módulos independentes e autocontidos

🔹 Core sem lógica de segurança

🔹 Resultados padronizados (ModuleResult)

🔹 Logs estruturados em JSON (auditáveis / SIEM-ready)

🔹 Nenhuma importação manual de módulos

## Estrutura do Projeto
```
ShadowSec-Toolkit/
├── main.py
├── README.md
├── __pycache__/
│
├── core/
│   ├── base_module.py
│   ├── module_loader.py
│   ├── module_result.py
│   └── module_scope.py
│
├── data_signatures/
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── SECURITY_TARGET.md
│   ├── THREAT_MODEL.md
│   └── modules/
│
├── logs/
│
├── modules/
│   ├── firewall/
│   │   ├── __init__.py
│   │   ├── firewall_apply.py
│   │   └── firewall_audit.py
│   │
│   ├── web/
│   │   ├── __init__.py
│   │   └── slow_http_audit.py
│   │
│   └── __init__.py
│
├── scripts/
│
└── utils/
    ├── cyber_banner.py
    ├── logger.py
    └── platform.py
```
## ⚙️ Instalação

### 1️⃣ Clonar o repositório
git clone https://github.com/lukk-valadao/ShadowSec-Toolkit-Core.git
cd ShadowSec-Toolkit

### 2️⃣ Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

### Uso

Execução principal
```
sudo python3 main.py
```

O Core:

Detecta módulos automaticamente

Filtra por ModuleScope

Exibe menu dinâmico

Executa módulos de forma isolada

## Sistema de Módulos

Tipos de módulos

Audit: apenas leitura / verificação

Apply: aplicação de mudanças (hardening)

Híbridos (planejado): audit + apply via submenu

### Exemplos atuais

Firewall Hardening (UFW)

Firewall Audit (UFW)

Slow HTTP Audit (RUDY-like)

Cada módulo:

herda de BaseModule

declara name e scope

retorna sempre ModuleResult

gera seus próprios logs

## Logs e Auditoria

Logs em formato JSON estruturado

Arquivo único de auditoria

## Cada evento possui:

event_id único

contexto do host

usuário executor

dados do módulo

## Pronto para:

SIEM

correlação futura

relatórios automatizados

## 📚 Documentação

ARCHITECTURE.md — arquitetura e diretrizes

SECURITY_TARGET.md — objetivos de segurança

THREAT_MODEL.md — modelo de ameaças

docs/modules/ — documentação específica de cada módulo

## 🔐 Segurança e Boas Práticas

Execução mínima como root

Nenhum tráfego ativo sem necessidade

Auditorias passivas por padrão

Configurações revertíveis

Compatível com ambientes offline

## 🧭 Roadmap

Submenus por categoria (Firewall, Web, System)

Relatórios estruturados (HTML / JSON)

Integração futura com CVEs (NVD / Vulners)

Interface gráfica (Flutter como frontend)

Execução remota controlada

ShadowSec Cloud Scanner (pesquisa)

## 🤝 Contribuindo

Fork do projeto

Crie uma branch

Siga as diretrizes arquiteturais

Envie um Pull Request bem documentado

Se quebrar a arquitetura, o PR será recusado.

## 📜 Licença

Distribuído sob licença MIT.

Uso, modificação e redistribuição são permitidos, desde que mantidos os créditos.

## 📧 Contato: lukk.valadao@gmail.com

## 🛡️ ShadowSec Toolkit

### Autor: Luciano Valadão

19/12/2025

