import streamlit as st
import pandas as pd
import unicodedata


def carregar_dados():
    return pd.read_csv("data/group_standings_1930-2026_com_indices.csv")

def remover_acentos(texto):
    texto = str(texto).lower().strip()
    texto_normalizado = unicodedata.normalize("NFD", texto)

    return "".join(
        caractere
        for caractere in texto_normalizado
        if unicodedata.category(caractere) != "Mn"
    )

st.set_page_config(
    page_title="Analisador de Subsequência",
    page_icon="⚽",
    layout="wide"
)

st.title("Seleções em Copas do Mundo (1930-2026)")
st.markdown("##### A evolução das seleções na fase de grupos das Copas do Mundo")

st.info(
    """
    **Informações relevantes:**

    - A análise de evolução das seleções considera apenas o desempenho na **fase de grupos** das Copas do Mundo, não considerando mata-mata, semifinais, finais e outros.
    - A trajetória das seleções, ao longo das edições em que participaram da fase de grupos, é calculada por um **índice de desempenho** (`índice de desempenho = pontos * 2 + saldo de gols`).
    - As Copas de **1934** e **1938** não foram consideradas na análise, pois essas edições não tiveram fase de grupos, sendo disputadas em formato eliminatório.
    - As Copas de **1942** e **1946** também não aparecem na base de dados, pois não foram realizadas devido à Segunda Guerra Mundial.
    - Em algumas edições, como **1950**, **1974**, **1978** e **1982**, a Copa do Mundo teve formatos diferentes, incluindo fases posteriores em formato de grupos, logo, para manter a comparação justa entre as seleções, o trabalho considera apenas a **primeira fase de grupos**.
    - O uso da **Maior Subsequência Crescente** permite identificar períodos em que uma seleção apresentou crescimento no índice de desempenho ao longo das Copas analisadas.
    - Portanto, o projeto busca observar a evolução histórica das seleções na etapa inicial da competição, sem determinar qual é a melhor seleção da história das Copas (embora saibamos que seja o Brasil).
    """
)

st.divider()

dados = carregar_dados()

selecoes = sorted(
    dados["selecao"].unique(),
    key=remover_acentos
)

selecao = st.selectbox("Escolha uma seleção:", selecoes)

dados_selecao = dados[dados["selecao"] == selecao].copy()
dados_selecao = dados_selecao.sort_values("ano")

registros = dados_selecao.to_dict("records")

st.write(f"## Dados {selecao}")

tabela = dados_selecao[
    [
        "ano",
        "selecao",
        "sigla_selecao",
        "jogos",
        "vitorias",
        "empates",
        "derrotas",
        "gols_marcados",
        "gols_sofridos",
        "saldo_de_gols",
        "pontos",
        "indice_desempenho",
        "avancou"
    ]
]

st.dataframe(tabela, use_container_width=True)

st.divider()

st.write("## Gráfico de Evolução")

grafico = dados_selecao.set_index("ano")[["indice_desempenho"]]

st.line_chart(grafico)
