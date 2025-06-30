# src/utils.py

import csv
import os
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

FIGSIZE = (16, 9)

def carregar_imagens_personagens(path):
    imagens_personagens = {}
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            imagens_personagens[row['nome']] = row['imagem']
    return imagens_personagens

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

def carregar_imagem(caminho, zoom=0.25):
    try:
        imagem = Image.open(caminho)
        return OffsetImage(imagem, zoom=zoom)
    except FileNotFoundError:
        print(f"Imagem não encontrada: {caminho}")
        return None

def construir_grafo_por_saga(relacoes, saga_nome=None):
    G = nx.Graph()
    for r in relacoes:
        if saga_nome is None or r["saga"].lower() == saga_nome.lower():
            G.add_node(r["origem"])
            G.add_node(r["destino"])
            G.add_edge(
                r["origem"],
                r["destino"],
                tipo=r["tipo"],
                peso=r["peso"]
            )
    return G

def imprimir_metricas(G, nome_grafo):
    print(f"\nMétricas do grafo: {nome_grafo}")
    graus = dict(G.degree())
    print("Grau dos nós:")
    for k, v in graus.items():
        print(f"  {k}: {v}")

    centralidade = nx.betweenness_centrality(G)
    print("\nCentralidade (betweenness):")
    for k, v in centralidade.items():
        print(f"  {k}: {v:.3f}")

    componentes = nx.number_connected_components(G)
    print(f"\nComponentes conectados: {componentes}")

    if nx.is_connected(G):
        diametro = nx.diameter(G)
        print(f"Diâmetro da rede: {diametro}")
    else:
        print("Grafo desconexo, não tem diâmetro definido")

def desenhar_grafo_com_imagens(G, pos, imagens, titulo="", nome_arquivo="grafo.png", saga=None):
    fig, ax = plt.subplots(figsize=FIGSIZE)

    # Fundo por saga
    if saga:
        saga_normalizada = saga.strip().lower()
        mapa_arquivo = None

        if "saiyajin" in saga_normalizada:
            mapa_arquivo = "mapaSagaSayajin.png"
        elif "freeza" in saga_normalizada:
            mapa_arquivo = "mapaNamekZ.png"
        elif "cell" in saga_normalizada:
            mapa_arquivo = "arenaCell.png"
        elif "majin" in saga_normalizada:
            mapa_arquivo = "PlanetaSenhorKaioshin.png"

        if mapa_arquivo:
            caminho_mapa = os.path.join("imagens", "mapas", mapa_arquivo)
            if os.path.exists(caminho_mapa):
                try:
                    img = Image.open(caminho_mapa)
                    x_vals = [p[0] for p in pos.values()]
                    y_vals = [p[1] for p in pos.values()]
                    ax.imshow(img, extent=[min(x_vals)-1, max(x_vals)+1, min(y_vals)-1, max(y_vals)+1], aspect='auto', alpha=0.8)
                except Exception as e:
                    print(f"Erro ao carregar plano de fundo da saga {saga}: {e}")

    # Arestas
    for u, v, data in G.edges(data=True):
        cor = 'green' if data['tipo'] == 'aliado' else 'red'
        largura = max(0.5, data['peso'])
        ax.plot(
            [pos[u][0], pos[v][0]],
            [pos[u][1], pos[v][1]],
            color=cor,
            linewidth=largura,
            alpha=0.7
        )

    # Nós
    for node in G.nodes():
        if node in imagens:
            ab = AnnotationBbox(imagens[node], pos[node], frameon=False)
            ax.add_artist(ab)
        else:
            ax.text(*pos[node], node, fontsize=8, ha='center')

    import matplotlib.patches as mpatches
    aliado_patch = mpatches.Patch(color='green', label='Aliado')
    inimigo_patch = mpatches.Patch(color='red', label='Inimigo')
    plt.legend(handles=[aliado_patch, inimigo_patch], loc='best')

    ax.set_title(titulo, fontsize=16)
    ax.set_axis_off()
    plt.tight_layout()
    plt.savefig(os.path.join("outputs", nome_arquivo))
    plt.show()
