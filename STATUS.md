# 🛡️ ShadowSec Toolkit — Migration Status ©

Este documento descreve o **estado atual da migração** do ShadowSec Toolkit
para o novo **Core modular plugin-based**, bem como o progresso dos módulos
existentes.

Seu objetivo é fornecer **visibilidade clara, objetiva e atualizada**
sobre o que já foi adaptado, o que está em andamento e o que ainda será migrado.

---

## 🧠 Visão Geral da Migração

O ShadowSec Toolkit está passando por uma **reestruturação arquitetural completa**,
evoluindo de um conjunto de scripts isolados para um **framework modular com Core
totalmente desacoplado da lógica de segurança**.

Durante este processo:

- Nenhum módulo é migrado sem aderir integralmente às diretrizes arquiteturais
- Funcionalidades legadas são revisadas, refatoradas e padronizadas
- Estabilidade, previsibilidade e segurança têm prioridade sobre velocidade

---

## ✅ Módulos Já Adaptados ao Novo Core

### 🔥 Firewall
- Firewall Audit (UFW) — **Concluído**
- Firewall Apply / Hardening (UFW) — **Concluído**

Status:
- Compatível com `BaseModule`
- Retorno padronizado via `ModuleResult`
- Logs estruturados em JSON
- Execução controlada por `ModuleScope`
- Execução mínima como root

---

### 🌐 Web
- Slow HTTP Audit (RUDY-like) — **Concluído**

Status:
- Auditoria passiva
- Nenhum tráfego agressivo gerado
- Compatível com ambientes restritos e offline
- Sem impacto operacional

---

## 🚧 Módulos em Planejamento / Migração Futura

Os módulos abaixo existem em versões anteriores do projeto
ou em formato experimental, e serão **gradualmente reescritos**
para o novo padrão arquitetural:

- Net Scan — mapeamento básico de rede (wrapper Nmap)
- Maldet — análise local com ClamAV + assinaturas adicionais
- ShadowSec RootKit Scan — auditoria e detecção de rootkits em sistemas Linux
- Permission Audit — auditoria de permissões suspeitas
- Idle Suspend Check — verificação e hardening de suspensão automática
- Dork Scanner — buscas automatizadas com dorks personalizadas
- ShadowSec Auditor — checklist automatizado de segurança do sistema
- ShadowSec Net Diag — diagnóstico de rede (IP, conflitos, conectividade)
- System Audit — análise de logs, usuários e permissões

---

## 🧱 Core — Estado Atual

O Core do ShadowSec encontra-se **estável e funcional**, servindo como base
para todas as evoluções futuras.

Estado atual:

- ✔️ Loader dinâmico de módulos
- ✔️ Isolamento total entre Core e lógica de segurança
- ✔️ Escopos de execução bem definidos (`ModuleScope`)
- ✔️ Logger estruturado em JSON (auditável / SIEM-ready)
- ✔️ Detecção de privilégios em runtime
- ✔️ Execução mínima como root (least privilege)

---

## 🧭 Diretrizes para Migração

Todo módulo migrado para o novo Core **deve obrigatoriamente**:

- Herdar de `BaseModule`
- Declarar `name`, `scope` e metadados relevantes
- Retornar exclusivamente um `ModuleResult`
- Não conter lógica de orquestração ou UI
- Gerar logs próprios, estruturados e auditáveis

Pull Requests que violem estas diretrizes **serão recusados**.

---

## 📅 Última Atualização

- Data: **26/12/2025**
- Versão do Core: **v0.5.0-dev**
- Base estável: **v0.4.0-core**
- Status geral: **Migração ativa**
