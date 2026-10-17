import pytest

from relatorio.leitura import ErroDeEntrada, ler_csv


def test_le_csv_valido(escrever_csv, linha_ok):
    df = ler_csv(escrever_csv([linha_ok]))
    assert len(df) == 1
    assert df["preco_unitario"].iloc[0] == "3,5"   # continua texto


def test_arquivo_inexistente(tmp_path):
    with pytest.raises(ErroDeEntrada, match="não encontrado"):
        ler_csv(tmp_path / "nao_existe.csv")


def test_arquivo_vazio(tmp_path):
    vazio = tmp_path / "vazio.csv"
    vazio.write_text("", encoding="utf-8")
    with pytest.raises(ErroDeEntrada, match="vazio"):
        ler_csv(vazio)


def test_coluna_faltando(tmp_path):
    arq = tmp_path / "ruim.csv"
    arq.write_text("data;produto\n01/01/2026;Caneta\n", encoding="utf-8")
    with pytest.raises(ErroDeEntrada, match="Faltam colunas"):
        ler_csv(arq)


def test_so_cabecalho(tmp_path):
    arq = tmp_path / "so_cabecalho.csv"
    arq.write_text("data;produto;regiao;vendedor;quantidade;preco_unitario;desconto\n",
                   encoding="utf-8")
    with pytest.raises(ErroDeEntrada, match="nenhuma linha"):
        ler_csv(arq)


def test_aceita_cabecalho_em_maiusculas_e_com_espacos(tmp_path):
    arq = tmp_path / "caixa.csv"
    arq.write_text(" DATA ;Produto;REGIAO;vendedor;quantidade;preco_unitario;desconto\n"
                   "01/01/2026;Caneta;Sul;Ana;1;3,5;0\n", encoding="utf-8")
    assert len(ler_csv(arq)) == 1
