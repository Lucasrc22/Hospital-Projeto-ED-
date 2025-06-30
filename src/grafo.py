from utils import carregar_imagens_personagens, carregar_relacoes, carregar_imagem, construir_grafo_por_saga, imprimir_metricas, desenhar_grafo_com_imagens
import os
import networkx as nx

PERSONAGENS_CSV = "data/personagens.csv"
RELACOES_CSV = "data/relacoes.csv"
OUTPUT_DIR = "outputs/"


def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    imagens_path = carregar_imagens_personagens(PERSONAGENS_CSV)
    relacoes = carregar_relacoes(RELACOES_CSV)

    chefes_finais = {
        "saiyajin": "Vegeta (saga Saiyajin)",
        "freeza": "Freeza",
        "cell": "Cell",
        "majin buu": "Majin Buu"
    }

    sagas = set(r['saga'].lower() for r in relacoes)
    for saga in sagas:
        G_saga = construir_grafo_por_saga(relacoes, saga)
        imprimir_metricas(G_saga, f"Grafo Saga {saga}")

        chefe = None
        for chave in chefes_finais.keys():
            if chave in saga:
                chefe = chefes_finais[chave]
                break

        if chefe and chefe in G_saga.nodes():
            pos_init = {chefe: [0, 0]}
            pos_saga = nx.spring_layout(G_saga, seed=42, k=2.0, fixed=[chefe], pos=pos_init)
        else:
            pos_saga = nx.spring_layout(G_saga, seed=42, k=2.0)

        imagens_saga = {}
        for node in G_saga.nodes():
            caminho_img = imagens_path.get(node)
            if caminho_img:
                img = carregar_imagem(caminho_img)
                if img:
                    imagens_saga[node] = img

        nome_arquivo = f"grafo_saga_{saga.replace(' ', '_')}.png"
        desenhar_grafo_com_imagens(
            G_saga, pos_saga, imagens_saga,
            f"Grafo Saga {saga}",
            nome_arquivo,
            saga=saga
        )





if __name__ == "__main__":
    main()