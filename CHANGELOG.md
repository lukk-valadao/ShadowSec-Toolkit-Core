# 📜 Changelog — ShadowSec Toolkit Core

Todas as mudanças relevantes neste projeto serão documentadas neste arquivo.

O formato segue o padrão **Keep a Changelog**
e este projeto adota **Versionamento Semântico (SemVer)**.

---

## [Unreleased]

### Added
- Documento `STATUS.md` para acompanhamento da migração
- Detecção de privilégios em runtime com orientação ao usuário
- Padronização de execução mínima como root

### Changed
- Estrutura do projeto reorganizada para Core modular
- Execução de módulos agora totalmente desacoplada do Core
- Logs padronizados em JSON para auditoria e SIEM

---

## [0.2.0] — 2025-12-19

### Added
- Core plugin-based com carregamento dinâmico de módulos
- Sistema de escopo (`ModuleScope`)
- Estrutura padrão de retorno (`ModuleResult`)
- Logger central estruturado
- Módulos de Firewall (Audit / Apply) compatíveis com o Core
- Módulo Web: Slow HTTP Audit

### Changed
- Refatoração do `main.py` para atuar apenas como orquestrador
- Remoção de lógica de segurança do Core
- Execução controlada e previsível dos módulos

### Security
- Execução mínima como root
- Nenhuma elevação automática de privilégio
- Auditorias passivas por padrão

---

## [0.1.0] — 2025-11-XX

### Added
- Primeiros scripts e ferramentas do ShadowSec Toolkit
- Módulos isolados sem Core unificado

### Notes
- Esta versão representa o estado **pré-Core**
- Código mantido apenas como referência histórica

---

## 🔗 Referências

- https://keepachangelog.com/en/1.1.0/
- https://semver.org/

