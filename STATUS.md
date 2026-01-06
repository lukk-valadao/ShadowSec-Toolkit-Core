# 🛡️ ShadowSec Toolkit — Migration Status

Este documento descreve o **estado atual da migração** do ShadowSec Toolkit
para o novo **Core modular plugin-based**, bem como o progresso real dos módulos
já adaptados.

Seu objetivo é fornecer **visibilidade clara, objetiva e auditável**
sobre o que está pronto, o que está estável e o que ainda será migrado.

---

## 🧠 Visão Geral da Migração

O ShadowSec Toolkit está passando por uma **reestruturação arquitetural profunda**,
evoluindo de scripts isolados para um **framework modular**, com:

- Core fixo e estável
- Módulos carregados dinamicamente
- Separação rigorosa entre auditoria e aplicação de mudanças
- Execução com **mínimo privilégio necessário**

Nenhum módulo é considerado “migrado” sem aderir **integralmente**
às diretrizes arquiteturais do Core.

---

## ✅ Módulos Já Adaptados ao Novo Core

### 🔥 Firewall
- Firewall Audit (UFW) — **Concluído**
- Firewall Apply / Hardening (UFW) — **Concluído**

Status:
- Compatível com `BaseModule`
- Retorno padronizado via `ModuleResult`
- Logs estruturados em JSON (SIEM-ready)
- Execução controlada por `ModuleScope`
- Execução mínima como root

---

### 🌐 Web
- Slow HTTP Audit (RUDY-like) — **Concluído**

Status:
- Auditoria totalmente passiva
- Nenhum tráfego agressivo gerado
- Compatível com ambientes restritos e offline
- Sem impacto operacional

---

### 🧹 System Cleanup
- System Cleanup Audit — **Concluído**
- System Cleanup Apply — **Concluído**

Status:
- Separação rigorosa entre auditoria e aplicação
- Limpeza de pacotes, cache APT e journal
- Limpeza explícita da lixeira do usuário alvo
- Apply executado apenas quando necessário
- Execução mínima como root
- Logs estruturados e auditáveis

---

### 🔄 System Updates
- System Updates Audit (APT) — **Concluído**
- System Updates Apply (APT) — **Concluído**

Status:
- Auditoria não intrusiva
- Apply explícito e controlado
- Nenhuma elevação automática de privilégios
- Compatível com ambientes de produção

---

## 🚧 Módulos em Planejamento / Migração Futura

Os módulos abaixo existem em versões anteriores do projeto
ou em estado conceitual, e serão **gradualmente reescritos**
para o novo padrão arquitetural:

- Scan de vírus (ClamAV / Defender)
- Pacotes órfãos avançados
- Diretórios de backup e resíduos
- Usuários com privilégios sudo / administradores
- Serviços ativos
- Espaço em disco
- Conexões de rede
- Integridade de pacotes do sistema
- Net Scan — mapeamento básico de rede (wrapper Nmap)
- Maldet — análise local com ClamAV + assinaturas adicionais
- ShadowSec RootKit Scan — auditoria e detecção de rootkits em Linux
- Permission Audit — permissões suspeitas
- Idle Suspend Check — suspensão automática por inatividade
- Dork Scanner — buscas automatizadas com dorks
- ShadowSec Auditor — checklist automatizado de segurança
- ShadowSec Net Diag — diagnóstico de rede
- System Audit — análise de logs, usuários e permissões

---

## 🧱 Core — Estado Atual

O Core do ShadowSec Toolkit encontra-se **estável, funcional e consolidado**,
servindo como base definitiva para todas as evoluções futuras.

Estado atual do Core:

- ✔️ Loader dinâmico de módulos
- ✔️ Isolamento total entre Core e lógica de segurança
- ✔️ Escopos de execução bem definidos (`ModuleScope`)
- ✔️ Logger estruturado em JSON
- ✔️ Serialização resiliente de dados complexos
- ✔️ Detecção de privilégios em runtime
- ✔️ Execução mínima como root (least privilege)
- ✔️ Nenhuma elevação automática de privilégios

---

## 🧭 Diretrizes para Migração

Todo módulo migrado para o novo Core **deve obrigatoriamente**:

- Herdar de `BaseModule`
- Declarar `name`, `scope` e metadados
- Retornar exclusivamente um `ModuleResult`
- Não conter lógica de orquestração ou UI
- Gerar logs estruturados e auditáveis
- Respeitar o princípio de mínimo privilégio

Pull Requests que violem estas diretrizes **serão recusados**.

---

## 📅 Última Atualização

- Data: **06/01/2026**
- Versão do Core: **v1.0.0-stable**
- Status geral: **Migração ativa**
