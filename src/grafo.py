# construir_grafo.py

import csv
import os
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

RELACOES_CSV = "data/relacoes.csv"
IMAGENS_DIR = "imagens/personagens/"

FIGSIZE = (16, 9)

def carregar_relacoes(path):
    relacoes = []
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            relacoes.append({
                "origem": row["origem"],
                "destino": row["destino"],
                "tipo": row["tipo"],
                "saga": row["saga"],
                "peso": int(row["peso"])
            })
    return relacoes

def carregar_imagem(caminho, zoom=0.15):
    try:
        imagem = Image.open(caminho)
        return OffsetImage(imagem, zoom=zoom)
    except FileNotFoundError:
        print(f"Imagem não encontrada: {caminho}")
        return None

def desenhar_grafo_com_imagens(G, pos, imagens):
    fig, ax = plt.subplots(figsize=FIGSIZE)
    
    for u, v, data in G.edges(data=True):
        cor = 'green' if data['tipo'] == 'aliado' else 'red'
        ax.plot(
            [pos[u][0], pos[v][0]],
            [pos[u][1], pos[v][1]],
            color=cor,
            linewidth=data['peso']
        )

    for node in G.nodes():
        if node in imagens:
            ab = AnnotationBbox(imagens[node], pos[node], frameon=False)
            ax.add_artist(ab)
        else:
            ax.text(*pos[node], node, fontsize=8, ha='center')

    ax.set_axis_off()
    plt.tight_layout()
    plt.savefig("outputs/grafo_geral.png")
    plt.show()

def main():
    relacoes = carregar_relacoes(RELACOES_CSV)

    G = nx.Graph()

    for r in relacoes:
        G.add_node(r["origem"])
        G.add_node(r["destino"])
        G.add_edge(
            r["origem"],
            r["destino"],
            tipo=r["tipo"],
            saga=r["saga"],
            peso=r["peso"]
        )

    pos = nx.spring_layout(G, seed=42) 

    imagens = {}
    for node in G.nodes():
        nome_arquivo = node.lower().replace(" ", "_").replace("(", "").replace(")", "") + ".png"
        caminho_img = os.path.join(IMAGENS_DIR, nome_arquivo)
        img = carregar_imagem(caminho_img)
        if img:
            imagens[node] = img

    desenhar_grafo_com_imagens(G, pos, imagens)

if __name__ == "__main__":
    main()
