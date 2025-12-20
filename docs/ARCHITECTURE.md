# ShadowSec Toolkit – Documentação de Arquitetura e Diretrizes

## 1. Visão Geral

O **ShadowSec Toolkit** evoluiu de um conjunto de scripts isolados para um **framework modular de cibersegurança**, com carregamento dinâmico de módulos, separação clara de responsabilidades e base preparada para expansão futura (desktop, mobile e interfaces gráficas).

Este documento registra:
- As **alterações arquiteturais realizadas**
- O **estado atual do projeto**
- As **regras e diretrizes** que devem ser seguidas daqui em diante

---

## 2. Problema Original

Antes das alterações, o projeto apresentava:
- Importações manuais de módulos
- Execução acoplada ao `main.py`
- Falta de padronização entre módulos
- Dificuldade para escalar (mobile, UI, API)
- Falta de controle sobre onde cada módulo pode rodar

---

## 3. Solução Arquitetural Adotada

### 3.1 Núcleo (Core)

O diretório `core/` passou a concentrar **toda a lógica estrutural do framework**:

- `BaseModule` – contrato obrigatório para todos os módulos
- `ModuleResult` – resultado padronizado de execução
- `ModuleScope` – define onde o módulo pode rodar
- `module_loader.py` – carregamento dinâmico automático

Isso transforma o ShadowSec em um **sistema orientado a plugins**.

---

### 3.2 BaseModule (Contrato Obrigatório)

Todo módulo **DEVE** herdar de `BaseModule`.

Requisitos mínimos:
```python
class BaseModule(ABC):
    name: str
    scope: ModuleScope

    @abstractmethod
    def run(self) -> ModuleResult:
        pass
```

Isso garante:
- Interface uniforme
- Execução previsível
- Compatibilidade com qualquer frontend futuro

---

### 3.3 ModuleScope (Classificação de Plataforma)

Cada módulo agora declara explicitamente **onde pode ser executado**:

```python
class ModuleScope(Enum):
    DESKTOP_ONLY = auto()
    SHARED = auto()
    MOBILE_ONLY = auto()
```

Exemplo:
```python
scope = ModuleScope.DESKTOP_ONLY
```

Isso permite:
- Filtrar menus
- Evitar execução inválida em mobile
- Planejar migração futura sem retrabalho

---

## 4. Carregamento Dinâmico de Módulos

### 4.1 Estrutura Obrigatória

```
modules/
├── firewall/
│   ├── __init__.py
│   ├── firewall_apply.py
│   └── firewall_audit.py
├── syscheckup/
├── limpeza/
└── __init__.py
```

Cada subpasta é tratada como um **package de módulos**.

---

### 4.2 Module Loader

O carregamento é feito via reflexão:

```python
modules = load_modules("modules")
```

O loader:
- Importa automaticamente todos os subpackages
- Identifica subclasses de `BaseModule`
- Instancia apenas módulos válidos

Nenhum módulo deve ser importado manualmente no `main.py`.

---

## 5. Estrutura do Main

O `main.py` agora tem responsabilidades claras:

- Inicialização visual (banner)
- Carregamento de módulos
- Renderização de menu
- Execução controlada

Ele **não contém lógica de segurança**.

Isso garante:
- Código limpo
- Facilidade de manutenção
- Substituição futura por UI gráfica ou mobile

---

## 6. Padrão de Resultado (ModuleResult)

Todo módulo retorna um `ModuleResult`:

Campos principais:
- `module`
- `status`
- `severity`
- `summary`
- `data`
- `recommendations`
- `platform`

Isso garante:
- Logs estruturados
- Relatórios consistentes
- Integração futura com dashboards

---

## 7. Diretrizes para Novos Módulos

### Obrigatório
- Herdar de `BaseModule`
- Declarar `name` e `scope`
- Retornar sempre `ModuleResult`
- Não usar `print()` fora do contexto controlado

### Recomendado
- Separar **audit** e **apply**
- Não assumir privilégios sem checagem
- Detectar plataforma antes de executar

---

## 8. Preparação para Mobile (Flutter)

Decisão arquitetural:

- **Python continua sendo o motor**
- Flutter será apenas interface
- Nenhuma lógica de segurança será reescrita em Kotlin

Possíveis integrações futuras:
- API local (FastAPI)
- Execução via subprocess
- Comunicação por socket local

---

## 9. Estado Atual do Projeto

Atualmente o ShadowSec:
- Possui arquitetura modular sólida
- Suporta expansão controlada
- Está pronto para UI, mobile e automação
- Pode ser usado como base profissional

---

## 10. Regra Final

> Nenhuma funcionalidade nova deve quebrar a arquitetura existente.

Se quebrar:
- O módulo está errado
- Não o core

---

🛡️ ShadowSec Toolkit

Luciano Valadão
16/12/2025
