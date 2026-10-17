"""Linha de comando: python -m relatorio dados/vendas.csv --saida relatorio.html"""
import argparse
import sys
from pathlib import Path

from .indicadores import calcular
from .leitura import ErroDeEntrada, ler_csv
from .limpeza import limpar
from .saida import gerar_html


def criar_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="relatorio",
        description="Gera um relatório de vendas em HTML a partir de um CSV.",
    )
    p.add_argument("entrada", help="caminho do CSV (separador ';', UTF-8)")
    p.add_argument("--saida", default="relatorio.html",
                   help="arquivo HTML de saída (padrão: relatorio.html)")
    p.add_argument("--titulo", default="Relatório de vendas")
    return p


def main(argv=None) -> int:
    """Devolve 0 se deu certo e 1 se o problema está no arquivo de entrada."""
    args = criar_parser().parse_args(argv)
    try:
        bruto = ler_csv(args.entrada)
        limpo, resumo = limpar(bruto)
        if limpo.empty:
            raise ErroDeEntrada("Nenhuma linha válida depois da limpeza.")
        html = gerar_html(calcular(limpo), resumo, titulo=args.titulo)
    except ErroDeEntrada as erro:
        print(f"Erro: {erro}", file=sys.stderr)
        return 1

    caminho_saida = Path(args.saida)
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    caminho_saida.write_text(html, encoding="utf-8")
    
    print(f"{resumo.linhas_lidas} linhas lidas, {resumo.descartadas} descartadas, "
          f"{resumo.linhas_usadas} usadas.")
    print(f"Relatório salvo em {args.saida}")
    return 0

