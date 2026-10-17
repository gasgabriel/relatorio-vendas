"""Geração do relatório em HTML (um único arquivo, sem dependências externas)."""
from html import escape

from .indicadores import Indicadores
from .limpeza import ResumoLimpeza

MESES = ["jan", "fev", "mar", "abr", "mai", "jun",
         "jul", "ago", "set", "out", "nov", "dez"]

CSS = """
:root{--ink:#1b2430;--muted:#5b6675;--line:#dde2e8;--bg:#f5f7f9;--card:#fff;--accent:#0c7c80}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 system-ui,sans-serif}
main{max-width:860px;margin:0 auto;padding:24px 16px 48px}
h1{margin:0 0 4px;font-size:28px}
h2{margin:32px 0 8px;font-size:20px}
.sub{color:var(--muted);margin:0}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin-top:20px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px}
.card span{display:block;color:var(--muted);font-size:13px}
.card b{font-size:22px}
table{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden}
th,td{padding:8px 12px;text-align:left;border-bottom:1px solid var(--line)}
td.n,th.n{text-align:right}
tr:last-child td{border-bottom:0}
.chart{width:100%;height:auto;background:var(--card);border:1px solid var(--line);border-radius:12px}
.qualidade{background:#fff8e8;border:1px solid #ecd9a6;border-radius:12px;padding:12px 16px}
@media print{body{background:#fff}.card,table,.chart{break-inside:avoid}}
"""


def brl(valor: float) -> str:
    """1234.5 -> 'R$ 1.234,50'"""
    texto = f"{valor:,.2f}"
    return "R$ " + texto.replace(",", "X").replace(".", ",").replace("X", ".")


def inteiro(valor: int) -> str:
    return f"{valor:,}".replace(",", ".")


def rotulo_mes(aaaa_mm: str) -> str:
    ano, mes = aaaa_mm.split("-")
    return f"{MESES[int(mes) - 1]}/{ano[2:]}"


def data_br(ts) -> str:
    return ts.strftime("%d/%m/%Y")


def _abreviar(valor: float) -> str:
    if valor >= 1000:
        return f"{valor / 1000:.1f}".replace(".", ",") + " mil"
    return f"{valor:.0f}"


def grafico_barras(rotulos, valores, largura=640, altura=240) -> str:
    """Gráfico de barras em SVG puro (sem bibliotecas)."""
    margem_baixo, margem_topo = 34, 24
    n = len(valores)
    maximo = max(valores) or 1
    area = altura - margem_baixo - margem_topo
    passo = largura / n
    larg_barra = passo * 0.6
    partes = [f'<svg class="chart" viewBox="0 0 {largura} {altura}" role="img" '
              f'aria-label="Receita por mês">']
    for i, (rot, val) in enumerate(zip(rotulos, valores)):
        h = area * val / maximo
        x = i * passo + (passo - larg_barra) / 2
        y = altura - margem_baixo - h
        partes.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{larg_barra:.1f}" '
                      f'height="{h:.1f}" rx="3" fill="#0c7c80"/>')
        partes.append(f'<text x="{x + larg_barra / 2:.1f}" y="{y - 6:.1f}" '
                      f'font-size="11" text-anchor="middle" fill="#5b6675">'
                      f'{escape(_abreviar(val))}</text>')
        partes.append(f'<text x="{x + larg_barra / 2:.1f}" y="{altura - 12}" '
                      f'font-size="12" text-anchor="middle" fill="#1b2430">'
                      f'{escape(rot)}</text>')
    partes.append("</svg>")
    return "".join(partes)


def _tabela(serie, titulo_coluna: str) -> str:
    linhas = "".join(
        f"<tr><td>{escape(str(nome))}</td><td class='n'>{brl(valor)}</td></tr>"
        for nome, valor in serie.items()
    )
    return (f"<table><thead><tr><th>{escape(titulo_coluna)}</th>"
            f"<th class='n'>Receita</th></tr></thead><tbody>{linhas}</tbody></table>")


def _bloco_qualidade(r: ResumoLimpeza) -> str:
    return f"""
<h2>Qualidade dos dados</h2>
<div class="qualidade">
<p>Foram lidas <b>{inteiro(r.linhas_lidas)}</b> linhas e usadas
<b>{inteiro(r.linhas_usadas)}</b>. Descartadas: <b>{inteiro(r.descartadas)}</b>.</p>
<ul>
<li>Linhas repetidas: {inteiro(r.duplicadas)}</li>
<li>Data inválida: {inteiro(r.data_invalida)}</li>
<li>Quantidade vazia, negativa ou inválida: {inteiro(r.quantidade_invalida)}</li>
<li>Preço inválido: {inteiro(r.preco_invalido)}</li>
<li>Desconto inválido: {inteiro(r.desconto_invalido)}</li>
</ul>
<p class="sub">Uma mesma linha pode ter mais de um problema, por isso a soma
pode passar do total de descartadas.</p>
</div>"""


def gerar_html(ind: Indicadores, resumo: ResumoLimpeza, titulo="Relatório de vendas") -> str:
    """Devolve o relatório completo como texto HTML."""
    cartoes = [
        ("Receita total", brl(ind.receita_total)),
        ("Vendas", inteiro(ind.num_vendas)),
        ("Itens vendidos", inteiro(ind.itens_vendidos)),
        ("Ticket médio", brl(ind.ticket_medio)),
    ]
    html_cartoes = "".join(
        f'<div class="card"><span>{escape(nome)}</span><b>{escape(valor)}</b></div>'
        for nome, valor in cartoes
    )
    rotulos = [rotulo_mes(m) for m in ind.por_mes.index]
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(titulo)}</title>
<style>{CSS}</style>
</head>
<body>
<main>
<h1>{escape(titulo)}</h1>
<p class="sub">Período: {data_br(ind.primeira_data)} a {data_br(ind.ultima_data)}</p>
<div class="cards">{html_cartoes}</div>
<h2>Receita por mês</h2>
{grafico_barras(rotulos, list(ind.por_mes.values))}
<h2>Top 5 produtos</h2>
{_tabela(ind.top_produtos, "Produto")}
<h2>Receita por região</h2>
{_tabela(ind.por_regiao, "Região")}
<h2>Receita por vendedor</h2>
{_tabela(ind.por_vendedor, "Vendedor")}
{_bloco_qualidade(resumo)}
</main>
</body>
</html>
"""
