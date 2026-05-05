# AGENTS

## Missão

Manter o projeto Aurora Finance Intelligence estável, reproduzível, apresentável para banca e coerente com a proposta premium free.

## Prioridades

- não quebrar `python -m src.pipeline`
- manter compatibilidade com Windows e PowerShell
- manter o frontend estático e sem backend obrigatório
- não adicionar serviços cloud pagos obrigatórios
- preservar a arquitetura AWS-ready com baixo risco de cobrança

## Regras obrigatórias

- usar `src/` como fonte de verdade da lógica analítica
- preservar reprodutibilidade com `seed = 42`
- manter os JSONs exportados em `app/public/data/`
- manter `threshold_analysis.json` sincronizado com `dados/outputs/threshold_analysis.csv`
- não remover artefatos importantes como `modelo/model.pkl` e `dados/outputs/predicoes_churn.csv`
- sempre refletir mudanças relevantes em `README.md` e `docs/`

## Quando alterar o modelo

Sempre atualizar:

- `dados/outputs/metricas_modelo.json`
- `dados/outputs/feature_importance.csv`
- `dados/outputs/classification_report.json`
- `dados/outputs/threshold_analysis.csv`, quando aplicável
- documentação sobre threshold, recall, precision e defesa do modelo

## Quando alterar o frontend

Sempre validar:

1. `npm install` se houver mudança de dependência
2. `npm run build`

## Quando alterar o pipeline

Sempre validar:

1. `python -m src.pipeline`
2. geração de arquivos em `dados/outputs/`
3. geração de arquivos em `app/public/data/`
4. consistência entre `summary.json` e a origem de dados ativa

## O que evitar

- não adicionar backend obrigatório
- não depender de banco cloud para a demo
- não introduzir complexidade desnecessária como serviços pagos ou overengineering de ML
- não documentar métricas fixas como se fossem permanentes; apontar sempre para os artefatos gerados

## Regra final

Toda mudança importante deve deixar o projeto mais claro para três públicos ao mesmo tempo:

- banca
- GitHub
- manutenção futura
