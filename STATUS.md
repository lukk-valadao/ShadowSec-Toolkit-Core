# 🛡️ ShadowSec Toolkit — Migration Status

Este documento descreve o **estado atual da migração** do ShadowSec Toolkit para o novo **Core modular plugin-based**, bem como o progresso dos módulos existentes.

O objetivo é fornecer **visibilidade clara e objetiva** sobre o que já foi adaptado, o que está em andamento e o que ainda será migrado.

---

## 🧠 Visão Geral da Migração

O ShadowSec Toolkit está passando por uma **reestruturação arquitetural completa**, migrando de scripts isolados para um **framework modular com Core desacoplado**.

Durante este processo:
- Nenhum módulo é migrado sem aderir integralmente às diretrizes arquiteturais
- Funcionalidades antigas são revisadas, refatoradas e padronizadas
- Compatibilidade e segurança têm prioridade sobre velocidade de migração

---

## ✅ Módulos Já Adaptados ao Novo Core

### 🔥 Firewall
- Firewall Audit (UFW) — **Concluído**
- Firewall Apply / Hardening (UFW) — **Concluído**

Status:
- Compatível com `BaseModule`
- Retorno via `ModuleResult`
- Logs estruturados em JSON
- Execução controlada por `ModuleScope`

---

### 🌐 Web
- Slow HTTP Audit (RUDY-like) — **Concluído**

Status:
- Auditoria passiva
- Sem tráfego agressivo
- Compatível com ambientes restritos

---

## 🚧 Módulos em Planejamento / Migração Futura

- Net Scan: mapeamento básico de rede (Nmap wrapper)
- Maldet: análise local usando ClamAV + assinaturas extras
- ShadowSec RootKit Scan: auditoria e detecção de rootkits para sistemas Linux - assinaturas dedicadas + detecção estendida
- Permission Audit: auditoria de permissões suspeitas
- Idle Suspend Check: verificação e hardening de suspensão automática
- Dork Scanner: buscas automatizadas com dorks personalizadas
- ShadowSec Auditor: checklist automatizado de segurança do sistema
- ShadowSec Net Diag: diagnóstico de Rede, conflito de ip, para sistemas Debian-based e Windows
- System Audit (logs, usuários, permissões)

> Estes módulos existem em versões anteriores do projeto ou em formato experimental, e serão **gradualmente reescritos** para o novo padrão.

---

## 🧱 Core — Estado Atual

- ✔️ Loader dinâmico de módulos
- ✔️ Isolamento entre Core e lógica de segurança
- ✔️ Escopos de execução bem definidos
- ✔️ Logger estruturado (JSON)
- ✔️ Detecção de privilégios em runtime
- ✔️ Execução mínima como root

---

## 🧭 Diretrizes para Migração

Todo módulo migrado deve:
- Herdar de `BaseModule`
- Declarar `name`, `scope` e metadados
- Retornar exclusivamente `ModuleResult`
- Não conter lógica de orquestração
- Gerar logs próprios e auditáveis

Pull Requests que violem estas regras **serão recusados**.

---

## 📅 Última Atualização

- Data: 26/12/2025
- Status geral: **Migração ativa**

