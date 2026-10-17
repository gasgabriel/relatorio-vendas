from relatorio.cli import main


def test_fluxo_completo_gera_o_html(escrever_csv, linha_ok, tmp_path, capsys):
    entrada = escrever_csv([linha_ok, dict(linha_ok, produto="Caderno", quantidade="1")])
    saida = tmp_path / "r.html"

    codigo = main([str(entrada), "--saida", str(saida)])

    assert codigo == 0
    html = saida.read_text(encoding="utf-8")
    assert "Receita total" in html
    assert "Caderno" in html
    assert "2 linhas lidas" in capsys.readouterr().out


def test_arquivo_inexistente_devolve_1_e_explica(tmp_path, capsys):
    codigo = main([str(tmp_path / "nada.csv"), "--saida", str(tmp_path / "r.html")])
    assert codigo == 1
    assert "não encontrado" in capsys.readouterr().err
    assert not (tmp_path / "r.html").exists()


def test_nenhuma_linha_valida_devolve_1(escrever_csv, linha_ok, tmp_path, capsys):
    entrada = escrever_csv([dict(linha_ok, quantidade="abc")])
    codigo = main([str(entrada), "--saida", str(tmp_path / "r.html")])
    assert codigo == 1
    assert "Nenhuma linha válida" in capsys.readouterr().err


def test_html_escapa_texto_vindo_do_csv(escrever_csv, linha_ok, tmp_path):
    entrada = escrever_csv([dict(linha_ok, produto="<script>alert(1)</script>")])
    saida = tmp_path / "r.html"
    main([str(entrada), "--saida", str(saida)])
    html = saida.read_text(encoding="utf-8")
    # a limpeza padroniza a caixa (<Script>), então conferimos nas duas formas
    assert "<script>" not in html.lower()
    assert "&lt;Script&gt;" in html


def test_titulo_personalizado(escrever_csv, linha_ok, tmp_path):
    entrada = escrever_csv([linha_ok])
    saida = tmp_path / "r.html"
    main([str(entrada), "--saida", str(saida), "--titulo", "Vendas de Março"])
    assert "Vendas de Março" in saida.read_text(encoding="utf-8")