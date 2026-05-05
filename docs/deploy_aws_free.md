# Deploy AWS Free

## Objetivo

Publicar a experiência web da Aurora com o menor risco possível de cobrança.

## Estratégia recomendada

Como o app consome JSONs estáticos gerados localmente, o caminho mais seguro é publicar somente o frontend.

### Opção 1. Amazon S3 Static Website Hosting

Fluxo:

1. rodar `python -m src.pipeline`
2. rodar `npm run build` em `app/`
3. publicar o conteúdo de `app/dist/`

### Opção 2. AWS Amplify Hosting

Fluxo:

1. conectar o repositório
2. configurar o build do frontend estático
3. publicar sem backend adicional

## Serviços a evitar para não gerar cobrança

Para este projeto, evitar criar sem necessidade:

- Amazon EC2
- Amazon RDS
- API Gateway
- AWS Lambda
- ECS
- EKS
- Redshift
- OpenSearch

## Por que esta abordagem é segura

Porque:

- não exige banco cloud
- não exige API
- não exige autenticação para demo
- não exige processamento online

## Recomendação prática para a banca

Se houver necessidade de demonstrar AWS, a melhor defesa é:

**“A solução já está pronta para hosting estático em S3 ou Amplify. Optamos por não usar recursos dinâmicos para manter custo zero ou risco mínimo de cobrança.”**
