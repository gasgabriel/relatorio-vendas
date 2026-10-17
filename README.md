# Relatório automático de vendas

![testes](https://github.com/gasgabriel/relatorio-vendas/actions/workflows/tests.yml/badge.svg)

Lê uma planilha de vendas (CSV), limpa os dados, calcula os indicadores principais
e gera um relatório em HTML com **um único comando**. O relatório também mostra quantas linhas foram descartadas e por quê.


**[Ver um relatório de exemplo](https://gasgabriel.github.io/relatorio-vendas/relatorio.html)** (dados fictícios)

## Como usar

```bash
python -m relatorio dados/vendas.csv --saida relatorio.html
```

Abra `relatorio.html` no navegador. Opções:

| Opção | O que faz |
|---|---|
| `--saida` | arquivo de saída (padrão: `relatorio.html`) |
| `--titulo` | título do relatório |

## Instalação

```bash
git clone https://github.com/gasgabriel/relatorio-vendas.git
cd relatorio-vendas
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python gerar_dados.py            # cria dados/vendas.csv (dados fictícios)
```

## Formato do CSV

Separador `;`, codificação UTF-8, com estas colunas:

| Coluna | Exemplo | Observação |
|---|---|---|
| data | `15/03/2026` ou `2026-03-15` | os dois formatos são aceitos |
| produto, regiao, vendedor | `Caneta` | espaços e caixa são padronizados |
| quantidade | `2` | inteiro maior que zero |
| preco_unitario | `3,50` | vírgula ou ponto |
| desconto | `10` | em %, de 0 a 100; vazio vale 0 |

## O que é descartado

Linhas repetidas e linhas com data, quantidade, preço ou desconto inválidos.
O relatório mostra a contagem de cada motivo.

## Indicadores

- **Receita** de uma venda = quantidade × preço × (1 − desconto/100)
- **Ticket médio** = receita total ÷ número de vendas
- Receita por mês, região e vendedor, e os 5 produtos com maior receita

## Testes

```bash
python -m pytest
```

## Estrutura

```
relatorio/
  leitura.py       lê o CSV e confere as colunas
  limpeza.py       regras de limpeza e resumo do que foi descartado
  indicadores.py   cálculo dos números
  saida.py         HTML do relatório (gráfico em SVG, sem bibliotecas)
  cli.py           linha de comando
tests/             testes automáticos
gerar_dados.py     gera uma planilha fictícia e "suja"
```

## Decisões e limitações

- O CSV é lido como texto e convertido em um único lugar (`limpeza.py`), com regras explícitas.
- Valores em dinheiro usam `float`. Para um sistema financeiro de verdade, o correto seria `Decimal` ou centavos inteiros.
- O relatório é estático: não atualiza sozinho (o agendamento vem do `cron`).
- Dados são fictícios.

## Próximos passos

Veja as [issues abertas](https://github.com/gasgabriel/relatorio-vendas/issues): salvar as linhas descartadas em um CSV, filtrar por período e trocar `float` por `Decimal`.

## Autores

gasgabriel & taleticia