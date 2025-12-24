# 🔍 Slow HTTP Audit (RUDY-like)

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)

![License](https://img.shields.io/badge/license-MIT-green.svg)

Autor: Luciano Valadão.

## Descrição técnica

O módulo Slow HTTP Audit (RUDY-like) é um componente de auditoria passiva do ShadowSec Toolkit, projetado para identificar padrões anômalos de requisições HTTP lentas compatíveis com ataques do tipo Slow HTTP / RUDY (R-U-Dead-Yet).

Este módulo não executa testes ativos, não envia tráfego e não interfere no funcionamento do servidor, operando exclusivamente por meio da análise de logs existentes de servidores web, como Nginx e Apache.

## Objetivo

Detectar comportamentos que indiquem possíveis tentativas de esgotamento de recursos do servidor web por meio de requisições POST deliberadamente lentas, caracterizadas por:

conexões mantidas abertas por longos períodos;

envio extremamente lento do corpo da requisição;

baixo volume total de dados transmitidos;

repetição do padrão a partir de um mesmo endereço IP.

## Metodologia de detecção

A detecção é baseada em heurísticas seguras e conservadoras, reduzindo a probabilidade de falsos positivos:

análise de requisições HTTP do tipo POST;

tempo de requisição superior a um limiar configurável (ex.: ≥ 60s);

volume de dados transmitidos inferior a um limite mínimo (ex.: ≤ 1 KB);

recorrência do padrão a partir do mesmo IP.

Somente quando múltiplos indicadores são observados simultaneamente o comportamento é classificado como suspeito.

## Fontes de dados

O módulo analisa passivamente os arquivos de log de acesso do servidor web, incluindo, mas não se limitando a:

/var/log/nginx/access.log

/var/log/apache2/access.log

Caso nenhum log compatível seja encontrado no sistema, o módulo retorna o status NOT_APPLICABLE, indicando que a auditoria não se aplica ao host analisado.

## Comportamento operacional

✔️ Execução totalmente passiva

✔️ Nenhuma alteração no sistema

✔️ Nenhum bloqueio de IP

✔️ Nenhuma mitigação automática

✔️ Geração de eventos estruturados em JSON

Os resultados são registrados no log de auditoria central do ShadowSec, com identificação única (event_id), permitindo integração com SIEMs, pipelines de análise ou correlação entre módulos.

## Classificação de severidade

A severidade reportada reflete risco potencial, não incidente confirmado:

Situação detectada	Severidade
Nenhum padrão suspeito	INFO
Comportamento anômalo consistente	MEDIUM

O módulo nunca eleva a severidade para CRITICAL, pois se trata de um mecanismo de auditoria e não de resposta a incidentes.

## Recomendações típicas

Quando padrões suspeitos são identificados, o módulo pode recomendar:

revisão de timeouts de leitura de requisições HTTP;

ativação de proteções contra slow requests no servidor web;

monitoramento contínuo dos IPs envolvidos;

correlação com módulos de firewall e hardening.

## Integração no ShadowSec Toolkit

Tipo de módulo: Audit

Escopo: Desktop / Server

Execução: sob demanda via menu

Log: JSON estruturado (audit log compartilhado)

Dependências externas: nenhuma

## Considerações de segurança e conformidade

Este módulo foi projetado para:

manter conformidade legal e ética;

evitar qualquer forma de teste intrusivo;

operar com mínima superfície de risco;

fornecer visibilidade sem impacto operacional.

