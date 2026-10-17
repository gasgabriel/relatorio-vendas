"""Cálculo dos indicadores a partir dos dados já limpos."""
from dataclasses import dataclass

import pandas as pd


@dataclass
class Indicadores:
    receita_total: float
    num_vendas: int
    itens_vendidos: int
    ticket_medio: float          # receita média por venda (por linha)
    desconto_medio: float        # em %, média simples das vendas
    primeira_data: pd.Timestamp
    ultima_data: pd.Timestamp
    por_mes: pd.Series           # índice "aaaa-mm"
    top_produtos: pd.Series      # 5 maiores por receita
    por_regiao: pd.Series
    por_vendedor: pd.Series


def _receita_por(df: pd.DataFrame, coluna) -> pd.Series:
    return df.groupby(coluna)["receita"].sum().sort_values(ascending=False)


def calcular(df: pd.DataFrame) -> Indicadores:
    """Calcula os números do relatório. Espera dados já limpos e não vazios."""
    if df.empty:
        raise ValueError("Não há vendas válidas para calcular indicadores.")
    por_mes = df.groupby(df["data"].dt.strftime("%Y-%m"))["receita"].sum().sort_index()
    return Indicadores(
        receita_total=float(df["receita"].sum()),
        num_vendas=len(df),
        itens_vendidos=int(df["quantidade"].sum()),
        ticket_medio=float(df["receita"].mean()),
        desconto_medio=float(df["desconto"].mean()),
        primeira_data=df["data"].min(),
        ultima_data=df["data"].max(),
        por_mes=por_mes,
        top_produtos=_receita_por(df, "produto").head(5),
        por_regiao=_receita_por(df, "regiao"),
        por_vendedor=_receita_por(df, "vendedor"),
    )
