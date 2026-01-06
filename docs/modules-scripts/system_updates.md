# Update Module

## Descrição

O módulo **Update** é responsável por auditar e aplicar atualizações do sistema
baseadas no gerenciador **APT**, mantendo o sistema **atualizado, previsível e seguro**.

Ele foi construído para evitar atualizações cegas ou automáticas sem visibilidade prévia.

---

## Funcionalidades

### 🔍 System Updates Audit (APT)

Executa uma auditoria segura que identifica:

- Quantidade de pacotes atualizáveis
- Presença de atualizações de segurança
- Estado geral do sistema em relação ao repositório

Nenhuma alteração é feita no sistema durante esta etapa.

Saída inclui:
- Status
- Severidade
- Resumo
- Lista ou contagem de pacotes pendentes

---

### 🔄 System Updates Apply (APT)

Aplica atualizações de forma controlada:

- Atualiza índices (`apt update`)
- Aplica upgrades (`apt upgrade`)
- Mantém rastreabilidade da execução

⚠️ Requisitos:
- Necessita privilégios elevados
- Verificação de privilégio ocorre antes da execução
- Caso não esteja elevado, o módulo solicita elevação

---

## Estrutura do Módulo

```text
modules/update/
├── __init__.py
├── update_audit.py
└── update_apply.py

```
## Boas Práticas
Este módulo foi desenhado para incentivar:

Auditoria antes da aplicação

Consciência do impacto das atualizações

Separação clara entre verificação e execução

Integração
Totalmente integrado ao menu principal do ShadowSec Toolkit Core,
seguindo o mesmo padrão de:

Status

Severidade

Relatórios estruturados

Luciano Valadão
