# construir_grafo.py

import csv
import os
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# Constantes
PERSONAGENS_CSV = "data/personagens.csv"
RELACOES_CSV = "data/relacoes.csv"
IMAGENS_DIR = ""  # Caminho já está completo no CSV personagens, então não precisa usar diretório fixo aqui
OUTPUT_DIR = "outputs/"
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

def carregar_imagem(caminho, zoom=0.15):
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

def desenhar_grafo_com_imagens(G, pos, imagens, titulo="", nome_arquivo="grafo.png"):
    fig, ax = plt.subplots(figsize=FIGSIZE)

    # Desenhar as arestas com cor e largura conforme tipo e peso
    for u, v, data in G.edges(data=True):
        cor = 'green' if data['tipo'] == 'aliado' else 'red'
        largura = max(0.5, data['peso'])  # evitar linha muito fina
        ax.plot(
            [pos[u][0], pos[v][0]],
            [pos[u][1], pos[v][1]],
            color=cor,
            linewidth=largura,
            alpha=0.7
        )
    
    # Desenhar os nós com imagens ou texto
    for node in G.nodes():
        if node in imagens:
            ab = AnnotationBbox(imagens[node], pos[node], frameon=False)
            ax.add_artist(ab)
        else:
            ax.text(*pos[node], node, fontsize=8, ha='center')

    # Legenda manual
    import matplotlib.patches as mpatches
    aliado_patch = mpatches.Patch(color='green', label='Aliado')
    inimigo_patch = mpatches.Patch(color='red', label='Inimigo')
    plt.legend(handles=[aliado_patch, inimigo_patch], loc='best')

    ax.set_title(titulo, fontsize=16)
    ax.set_axis_off()
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, nome_arquivo))
    plt.show()

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    imagens_path = carregar_imagens_personagens(PERSONAGENS_CSV)
    relacoes = carregar_relacoes(RELACOES_CSV)

    # Grafo geral
    G_geral = construir_grafo_por_saga(relacoes)
    imprimir_metricas(G_geral, "Grafo Geral Dragon Ball")
    pos = nx.spring_layout(G_geral, seed=42)
    imagens = {}
    for node in G_geral.nodes():
        caminho_img = imagens_path.get(node)
        if caminho_img:
            img = carregar_imagem(caminho_img)
            if img:
                imagens[node] = img
    desenhar_grafo_com_imagens(G_geral, pos, imagens, "Grafo Geral Dragon Ball", "grafo_geral.png")

    # Grafos por saga
    sagas = set(r['saga'] for r in relacoes)
    for saga in sagas:
        G_saga = construir_grafo_por_saga(relacoes, saga)
        imprimir_metricas(G_saga, f"Grafo Saga {saga}")
        pos_saga = nx.spring_layout(G_saga, seed=42)
        imagens_saga = {}
        for node in G_saga.nodes():
            caminho_img = imagens_path.get(node)
            if caminho_img:
                img = carregar_imagem(caminho_img)
                if img:
                    imagens_saga[node] = img
        nome_arquivo = f"grafo_saga_{saga.lower().replace(' ', '_')}.png"
        desenhar_grafo_com_imagens(G_saga, pos_saga, imagens_saga, f"Grafo Saga {saga}", nome_arquivo)

if __name__ == "__main__":
    main()
