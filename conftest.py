import pandas as pd
import pytest

COLUNAS = ["data", "produto", "regiao", "vendedor",
           "quantidade", "preco_unitario", "desconto"]


@pytest.fixture
def linha_ok():
    """Uma venda válida, como o CSV entrega: tudo texto."""
    return {"data": "15/03/2026", "produto": "Caneta", "regiao": "Sul",
            "vendedor": "Ana", "quantidade": "2", "preco_unitario": "3,5",
            "desconto": "10"}


@pytest.fixture
def fazer_df():
    """Monta um DataFrame de texto a partir de uma lista de dicionários."""
    def _fazer(linhas):
        return pd.DataFrame(linhas, columns=COLUNAS, dtype=str)
    return _fazer


@pytest.fixture
def escrever_csv(tmp_path):
    """Escreve um CSV de teste e devolve o caminho."""
    def _escrever(linhas, nome="vendas.csv"):
        caminho = tmp_path / nome
        cabecalho = ";".join(COLUNAS)
        corpo = "\n".join(";".join(str(l[c]) for c in COLUNAS) for l in linhas)
        caminho.write_text(cabecalho + "\n" + corpo + "\n", encoding="utf-8")
        return caminho
    return _escrever