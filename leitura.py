"""Leitura e validação do arquivo de entrada."""
from pathlib import Path

import pandas as pd

COLUNAS_OBRIGATORIAS = [
    "data", "produto", "regiao", "vendedor",
    "quantidade", "preco_unitario", "desconto",
]


class ErroDeEntrada(Exception):
    """Problema no arquivo de entrada que a pessoa usuária pode corrigir."""


def ler_csv(caminho) -> pd.DataFrame:
    """Lê o CSV (separador ';') com tudo como texto e confere as colunas.

    Ler tudo como texto é de propósito: a conversão para número e data
    acontece em um só lugar (limpeza.py), com regras explícitas.
    """
    caminho = Path(caminho)
    if not caminho.exists():
        raise ErroDeEntrada(f"Arquivo não encontrado: {caminho}")
    try:
        df = pd.read_csv(caminho, sep=";", dtype=str, encoding="utf-8")
    except pd.errors.EmptyDataError:
        raise ErroDeEntrada(f"O arquivo está vazio: {caminho}") from None
    except UnicodeDecodeError:
        raise ErroDeEntrada(
            f"Não consegui ler {caminho}. Salve o arquivo como UTF-8."
        ) from None

    df.columns = [str(c).strip().lower() for c in df.columns]
    faltando = [c for c in COLUNAS_OBRIGATORIAS if c not in df.columns]
    if faltando:
        raise ErroDeEntrada(f"Faltam colunas no arquivo: {', '.join(faltando)}")
    if df.empty:
        raise ErroDeEntrada("O arquivo tem o cabeçalho, mas nenhuma linha de dados.")
    return df[COLUNAS_OBRIGATORIAS]