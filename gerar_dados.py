"""Gera dados/vendas.csv: uma planilha de vendas fictícia e propositalmente suja."""
import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)  # mesma planilha toda vez: resultados reproduzíveis

PRODUTOS = {
    "Camiseta": 49.99,
    "Bermuda": 69.99,
    "Moletom": 119.99,
    "Regata": 49.99,
    "Jaqueta": 159.99,
    "Vestido": 79.99,
    "Saia": 69.99,
    "Shorts": 89.99,
    "Blusa": 79.99,
    "Meias": 19.99,
    "Bone": 39.99,
    "Cinto": 29.99
}
REGIOES = ["Norte", "Sul", "Centro-Oeste", "Sudeste", "Nordeste"]
VENDEDORES = ["Ana", "Bruno", "Carla", "Diego", "João"]


def gerar_linhas(n=1000):
    linhas = []
    for i in range(n):
        dia = date(2026, 1, 1) + timedelta(days=random.randint(0, 300))
        produto = random.choice(list(PRODUTOS))
        linhas.append({
            # alguns em outro formato de data
            "data": dia.strftime("%d/%m/%Y") if i % 17 else dia.isoformat(),
            # alguns com espaço e caixa diferente
            "produto": f" {produto.lower()} " if i % 29 == 0 else produto,
            "regiao": random.choice(REGIOES),
            "vendedor": random.choice(VENDEDORES),
            # alguns vazios, um negativo, um com texto
            "quantidade": ("" if i % 23 == 0 else "-1" if i == 101
                           else "dois" if i == 202
                           else random.randint(1, 10)),
            "preco_unitario": str(PRODUTOS[produto]).replace(".", ","),
            "desconto": random.choice([0, 0, 0, 5, 10]),
        })
    linhas += random.sample(linhas, 24)  # linhas repetidas
    return linhas


if __name__ == "__main__":
    Path("dados").mkdir(exist_ok=True)
    linhas = gerar_linhas()
    with open("dados/vendas.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0]), delimiter=";")
        w.writeheader()
        w.writerows(linhas)
    print(f"{len(linhas)} linhas gravadas em dados/vendas.csv")