# 📜 Changelog — ShadowSec Toolkit Core ©

Todas as mudanças relevantes neste projeto são documentadas neste arquivo.

O formato segue o padrão **Keep a Changelog**
(https://keepachangelog.com/en/1.1.0/)
e o projeto adota **Versionamento Semântico (SemVer)**
(https://semver.org/).

---

## [v0.5.0-dev] — Em desenvolvimento

Esta versão representa a fase atual de evolução do ShadowSec Toolkit,
com o **Core já estável** e os **módulos sendo migrados gradualmente**
para o novo formato arquitetural.

### Added
- Documento `STATUS.md` para acompanhamento do progresso da migração
- Detecção de privilégios em runtime com orientação explícita ao usuário
- Execução mínima como root, sem elevação automática de privilégios
- Utilitário centralizado para verificação de privilégios

### Changed
- Estrutura do projeto reorganizada em torno de um Core modular
- Execução de módulos totalmente desacoplada do Core
- Logs padronizados em JSON, preparados para auditoria e integração com SIEM
- Ajustes nos módulos de Firewall para aderência total ao novo Core

### Notes
- Esta versão marca a consolidação do Core e o início da migração progressiva
  dos módulos legados.
- Quebras arquiteturais não são permitidas a partir deste ponto.

---

## [v0.4.0-core] — 2025-12-19

Primeira versão **estável** do Core modular do ShadowSec Toolkit.

### Added
- Core plugin-based com carregamento dinâmico de módulos
- Contrato obrigatório via `BaseModule`
- Sistema de escopo de execução (`ModuleScope`)
- Estrutura padronizada de retorno (`ModuleResult`)
- Logger central estruturado em JSON
- Módulos de Firewall (Audit / Apply) compatíveis com o novo Core
- Módulo Web: Slow HTTP Audit (RUDY-like)

### Changed
- Refatoração completa do `main.py`, agora atuando apenas como orquestrador
- Remoção total de lógica de segurança do Core
- Execução de módulos de forma isolada, previsível e controlada

### Security
- Execução mínima como root
- Nenhuma elevação automática de privilégios
- Auditorias passivas por padrão
- Alterações aplicadas de forma explícita e auditável

### Notes
- Esta versão estabelece a base arquitetural definitiva do ShadowSec Toolkit.
- Todas as versões futuras devem respeitar o contrato definido pelo Core.

---

## [v0.1.0] — 2025-11-XX

Versão inicial do projeto, anterior à introdução do Core modular.

### Added
- Primeiros scripts e ferramentas do ShadowSec Toolkit
- Módulos isolados sem padronização ou Core unificado

### Notes
- Esta versão representa o estado **pré-Core**
- O código é mantido apenas como referência histórica
- Não deve ser usado como base para novos desenvolvimentos

---

## 🔗 Referências

- Keep a Changelog — https://keepachangelog.com/en/1.1.0/
- Semantic Versioning — https://semver.org/
