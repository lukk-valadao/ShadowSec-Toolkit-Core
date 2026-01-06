# Cleanup Module

## Descrição

O módulo **Cleanup** é responsável por auditar e aplicar rotinas básicas de limpeza no sistema,
com foco em **higiene operacional**, **economia de espaço em disco** e **redução de artefatos esquecidos**.

Ele foi projetado para operar de forma **segura**, separando claramente:
- auditoria (sem impacto no sistema)
- aplicação (com impacto controlado)

Nenhuma ação destrutiva é executada sem privilégios elevados.

---

## Funcionalidades

### 🔍 System Cleanup Audit

Realiza uma análise não intrusiva dos seguintes pontos:

- Pacotes órfãos (`apt autoremove --dry-run`)
- Tamanho do cache do APT
- Uso de disco do journal (`journalctl`)
- Espaço ocupado pela lixeira do usuário

Saída padronizada:
- Status
- Severidade
- Resumo
- Detalhes técnicos

---

### 🧹 System Cleanup Apply

Executa **apenas ações seguras e previsíveis**, exigindo privilégios elevados quando necessário.

Atualmente implementado:
- Limpeza completa da lixeira do usuário (`~/.local/share/Trash`)

⚠️ Importante:
- O módulo **verifica privilégios**
- Caso não esteja em modo elevado, solicita elevação de forma controlada
- Nenhuma ação roda silenciosamente como root

---

## Estrutura do Módulo

```text
modules/cleanup/
├── __init__.py
├── cleanup_audit.py
└── cleanup_apply.py

```
## Filosofia de Segurança
Este módulo segue três princípios:

Auditoria primeiro

Ações mínimas necessárias

Separação total entre análise e execução

O objetivo não é “limpar agressivamente”, mas reduzir ruído operacional sem risco.

## Integração
Este módulo é integrado ao menu principal do ShadowSec Toolkit Core
e segue o mesmo padrão de status e severidade adotado pelos demais módulos.

Luciano Valadão
