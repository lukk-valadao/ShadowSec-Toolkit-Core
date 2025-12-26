# 🛡️ ShadowSec Toolkit ©

Documentação de Arquitetura e Diretrizes

Autor: Luciano Valadão
Data: 16/12/2025

## 1. Visão Geral

O ShadowSec Toolkit evoluiu de um conjunto de scripts isolados para um framework modular de cibersegurança, orientado a plugins, com:

Carregamento dinâmico de módulos

Separação clara de responsabilidades

Contrato de execução e retorno padronizado

Base sólida para expansão futura (Desktop, Mobile, GUI, API)

Este documento define o estado oficial da arquitetura, bem como regras obrigatórias para qualquer evolução do projeto.

## 2. Problema Original

Antes da reestruturação, o projeto apresentava:

Importações manuais de módulos

Execução fortemente acoplada ao main.py

Ausência de padrão entre módulos

Dificuldade de expansão (UI, Mobile, API)

Falta de controle sobre onde cada módulo poderia rodar

## 3. Solução Arquitetural Adotada
### 3.1 Núcleo (Core)

O diretório core/ concentra toda a lógica estrutural do framework.

Componentes principais:

BaseModule – contrato obrigatório de todos os módulos

ModuleResult – padrão único de retorno

ModuleScope – definição explícita de plataforma

module_loader.py – carregamento dinâmico automático

O ShadowSec passa a operar como um sistema orientado a plugins, desacoplado da interface.

## 4. BaseModule – Contrato Obrigatório

Todo módulo DEVE herdar de BaseModule.

Contrato mínimo:
class BaseModule(ABC):
    name: str
    scope: ModuleScope

    @abstractmethod
    def run(self) -> ModuleResult:
        pass

Garantias fornecidas:

Interface uniforme

Execução previsível

Compatibilidade com qualquer frontend (CLI, Desktop, Mobile, API)

## 5. ModuleScope – Classificação de Plataforma

Cada módulo DEVE declarar explicitamente onde pode ser executado.

class ModuleScope(Enum):
    DESKTOP_ONLY = auto()
    SHARED = auto()
    MOBILE_ONLY = auto()

Exemplo:
scope = ModuleScope.DESKTOP_ONLY

Benefícios:

Filtro automático de menus

Prevenção de execução inválida em mobile

Planejamento de migração futura sem retrabalho

## 6. Carregamento Dinâmico de Módulos
### 6.1 Estrutura Obrigatória
modules/
├── firewall/
│   ├── __init__.py
│   ├── firewall_apply.py
│   └── firewall_audit.py
├── syscheckup/
├── limpeza/
└── __init__.py


Cada subdiretório representa um package de módulos.

### 6.2 Module Loader

O carregamento é feito via reflexão:

modules = load_modules("modules")


O loader:

Importa automaticamente todos os subpackages

Identifica subclasses válidas de BaseModule

Instancia apenas módulos compatíveis

🚫 Nenhum módulo deve ser importado manualmente no main.py.

## 7. Estrutura do Main

O main.py possui responsabilidades estritamente definidas:

Inicialização visual (banner)

Carregamento de módulos

Renderização de menu

Execução controlada

🚫 O main.py não contém lógica de segurança.

Benefícios:

Código limpo

Fácil manutenção

Substituição futura por GUI ou mobile sem refatoração

## 8. Contrato de Interface – ModuleResult (OBRIGATÓRIO)

Todo módulo DEVE retornar um objeto ModuleResult, seguindo exatamente este contrato.

### 8.1 Estrutura Oficial do ModuleResult
module: string
    Nome único do módulo

status: enum
    Valores possíveis:
    - success
    - warning
    - error
    - skipped

severity: enum
    Valores possíveis:
    - info
    - low
    - medium
    - high
    - critical

summary: string
    Descrição curta e humana do resultado

data: dict
    Dados técnicos estruturados
    (NUNCA texto solto ou logs)

recommendations: list[string]
    Ações sugeridas ao usuário

platform: enum
    - desktop
    - mobile
    - shared

timestamp: string (ISO-8601)

### 8.2 Regras para Interfaces (CLI, GUI, Mobile, API)

A interface NÃO executa lógica de segurança

A interface NÃO interpreta texto livre

Toda visualização é baseada apenas em:

status

severity

dados estruturados

Qualquer frontend deve consumir apenas ModuleResult

Isso garante compatibilidade com:

Flutter

Web dashboards

APIs REST

Automação e relatórios

## 9. Diretrizes para Novos Módulos
Obrigatório

Herdar de BaseModule

Declarar name e scope

Retornar sempre ModuleResult

Não usar print() fora do contexto controlado

Recomendado

Separar audit e apply

Não assumir privilégios sem checagem

Detectar plataforma antes da execução

## 9.1 Módulos Apply devem sempre:

- Checar privilégios

- Registrar mudanças

- Permitir rollback quando possível

## 10. Preparação para Mobile (Flutter)

Decisão Arquitetural

Python permanece como motor de segurança

Flutter será apenas interface

Nenhuma lógica será reescrita em Kotlin ou Dart

Integrações futuras possíveis:

API local (FastAPI)

Execução via subprocess

Comunicação via socket local

## 11. Estado Atual do Projeto

Atualmente, o ShadowSec Toolkit:

Possui arquitetura modular sólida

Está preparado para UI, mobile e automação

Permite crescimento sem refatoração estrutural

Pode ser utilizado como base profissional

## 12. Regra Final (INQUEBRÁVEL)

Nenhuma funcionalidade nova deve quebrar esta arquitetura.

Se quebrar:

❌ O módulo está errado

✅ O core está certo

---

# Arquitetura antes de funcionalidade.

---
🛡️ ShadowSec Toolkit ©
Autor: Luciano Valadão
16/12/2025
