import pandas as pd


def calcular_indices(
    caminho_entrada="data/group_standings_1930-2026.csv",
    caminho_saida="data/group_standings_1930-2026_com_indices.csv"
):
    dados = pd.read_csv(caminho_entrada)

    dados["indice_desempenho"] = (
        dados["pontos"] * 2 + dados["saldo_de_gols"]
    )

    dados.to_csv(caminho_saida, index=False)

    return dados


if __name__ == "__main__":
    calcular_indices()
    print("Arquivo com índice de desempenho gerado com sucesso.")
