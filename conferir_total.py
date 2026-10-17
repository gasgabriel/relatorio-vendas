"""Conferência independente: recalcula a receita total SEM pandas.

Se o número daqui bater com o do relatório, os dois caminhos concordam.
Uso: python conferir_total.py dados/vendas.csv
"""
import csv
import sys

vistos = set()
total = 0.0
for linha in csv.DictReader(open(sys.argv[1], encoding="utf-8"), delimiter=";"):
    chave = tuple((k, (v or "").strip().lower()) for k, v in linha.items())
    if chave in vistos:
        continue
    vistos.add(chave)
    try:
        qtd = int(linha["quantidade"])
        preco = float(linha["preco_unitario"].replace(",", "."))
        desc = float(linha["desconto"] or 0)
    except ValueError:
        continue
    if qtd <= 0 or preco <= 0 or not 0 <= desc <= 100:
        continue
    total += qtd * preco * (1 - desc / 100)

print(f"Receita total (conferência): {total:.2f}")