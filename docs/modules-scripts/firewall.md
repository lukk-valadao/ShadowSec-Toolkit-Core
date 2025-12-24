# 🔥 Módulos de Firewall — UFW (Audit & Hardening)

O conjunto de módulos de Firewall do ShadowSec Toolkit implementa uma separação clara entre auditoria e aplicação de hardening, seguindo rigorosamente os princípios arquiteturais do framework (plugin-based, core agnóstico, resultados padronizados e logs estruturados).

Ambos os módulos utilizam o UFW (Uncomplicated Firewall) como backend no Linux e operam exclusivamente em ambientes Desktop/Linux, conforme declarado via ModuleScope.

## 🧪 Firewall Audit (UFW)
### 📄 Descrição Técnica

O módulo Firewall Audit (UFW) é responsável por realizar uma verificação passiva do estado do firewall, sem aplicar alterações no sistema. Ele valida a presença do UFW, coleta seu status detalhado e retorna um resultado estruturado para consumo pelo core e por interfaces futuras.

Nenhuma regra é criada, removida ou modificada durante a execução deste módulo.

## ⚙️ Funcionamento Interno

O módulo executa as seguintes etapas:

### Detecção de Plataforma

Verifica o sistema operacional via platform.system()

Retorna NOT_APPLICABLE caso não seja Linux

### Validação de Dependência

Confirma a existência do binário ufw usando shutil.which

Retorna falha crítica se o firewall não estiver instalado

### Auditoria do Estado

Executa ufw status verbose

Analisa se o firewall está ativo ou inativo

Coleta o output completo para registro

### Registro de Auditoria

Gera log estruturado em JSON via log_json_audit

Inclui metadados de execução e plataforma

## 📦 Resultado Gerado

O módulo retorna um ModuleResult contendo:

Status do firewall (ativo ou inativo)

Severidade apropriada

Output completo do UFW

Plataforma detectada

Log persistente para rastreabilidade

## 🔐 Características de Segurança

Execução não intrusiva

Nenhuma modificação no sistema

Ideal para diagnósticos iniciais e compliance checks

Seguro para ambientes produtivos

## 🛠️ Firewall Hardening (UFW)
### 📄 Descrição Técnica

O módulo Firewall Hardening (UFW) é responsável por aplicar hardening ativo no firewall do sistema, redefinindo regras, estabelecendo políticas seguras padrão e habilitando logging.

Este módulo altera o estado do sistema e deve ser executado conscientemente, preferencialmente após uma auditoria prévia.

## ⚙️ Funcionamento Interno

O processo de hardening segue uma sequência controlada e auditável:

###Validação de Plataforma

Restrito a Linux (ModuleScope.DESKTOP_ONLY)

### Verificação de Dependência

Confirma se o UFW está instalado

Bloqueia execução se ausente

### Criação de Backup

Salva o estado atual das regras (ufw status numbered)

Backup versionado por timestamp

### Reset Controlado

Executa ufw --force reset

Remove regras antigas de forma previsível

### Aplicação de Políticas Padrão

deny incoming

allow outgoing

### Liberação de Portas Essenciais

SSH (porta configurável)

HTTP (80/TCP)

HTTPS (443/TCP)

### Ativação de Logging

Habilita logs do UFW

Ativa o firewall de forma forçada

### Auditoria Pós-Ação

Gera log JSON detalhado com:

Usuário executor

Host

Plataforma

Alterações aplicadas

## 📦 Resultado Gerado

O módulo retorna um ModuleResult contendo:

Lista completa de alterações realizadas

Status de execução

Severidade informativa

Metadados de ambiente

Registro de auditoria persistente

## 🔐 Características de Segurança

Backup automático antes de qualquer alteração

Política de negação por padrão

Logging ativo para análise forense

Execução explícita (nunca automática)

## 🧩 Arquitetura e Boas Práticas

### Ambos os módulos:

Herdam de BaseModule

Declararam explicitamente ModuleScope

Retornam sempre ModuleResult

Utilizam logs estruturados em JSON

Não contêm lógica de interface

Não violam o core do framework

### Essa separação permite:

Uso independente (audit vs apply)

Criação futura de submenus

Integração com UI, API ou mobile

Auditoria clara e rastreável


Luciano Valadão
