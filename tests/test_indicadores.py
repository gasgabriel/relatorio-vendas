import pytest

from relatorio.indicadores import calcular
from relatorio.limpeza import limpar


@pytest.fixture
def limpo(fazer_df, linha_ok):
    """3 vendas com total calculado À MÃO:
    2 x 10,00 sem desconto           = 20,00
    1 x 50,00 com 10% de desconto    = 45,00
    3 x  5,50 sem desconto           = 16,50   -> total 81,50
    """
    linhas = [
        dict(linha_ok, data="05/01/2026", produto="A", quantidade="2", preco_unitario="10,00", desconto="0"),
        dict(linha_ok, data="20/01/2026", produto="B", quantidade="1", preco_unitario="50,00", desconto="10"),
        dict(linha_ok, data="02/02/2026", produto="A", quantidade="3", preco_unitario="5,50", desconto="0"),
    ]
    df, _ = limpar(fazer_df(linhas))
    return df


def test_totais_batem_com_o_calculo_manual(limpo):
    ind = calcular(limpo)
    assert ind.receita_total == pytest.approx(81.50)
    assert ind.num_vendas == 3
    assert ind.itens_vendidos == 6
    assert ind.ticket_medio == pytest.approx(81.50 / 3)


def test_receita_por_mes(limpo):
    ind = calcular(limpo)
    assert list(ind.por_mes.index) == ["2026-01", "2026-02"]
    assert ind.por_mes["2026-01"] == pytest.approx(65.00)
    assert ind.por_mes["2026-02"] == pytest.approx(16.50)


def test_produtos_ordenados_da_maior_para_a_menor_receita(limpo):
    ind = calcular(limpo)
    assert list(ind.top_produtos.index) == ["B", "A"]
    assert ind.top_produtos["A"] == pytest.approx(36.50)


def test_a_soma_das_partes_e_igual_ao_total(limpo):
    ind = calcular(limpo)
    assert ind.por_mes.sum() == pytest.approx(ind.receita_total)
    assert ind.por_regiao.sum() == pytest.approx(ind.receita_total)
    assert ind.por_vendedor.sum() == pytest.approx(ind.receita_total)


def test_sem_vendas_validas_da_erro_claro(fazer_df):
    df, _ = limpar(fazer_df([]))
    with pytest.raises(ValueError):
        calcular(df)
