# ...existing code...
import networkx as nx
import matplotlib.pyplot as plt

def plot_graph(num_islands, num_bridges, bridge_start, bridge_end, bridge_capacity, used_bridges):
    # Criar lista de arestas usadas (tuplas)
    used_edges = list(used_bridges) if used_bridges else []

    # Se não houver pontes de interesse, salvar figura vazia/informativa e sair
    if not used_edges:
        plt.figure()
        plt.title("Nenhuma ponte de interesse")
        plt.savefig('graph.png')
        return

    # obter conjunto de nós que aparecem nas arestas de interesse
    nodes_of_interest = set()
    for u, v in used_edges:
        nodes_of_interest.add(u)
        nodes_of_interest.add(v)

    # criar grafo auxiliar apenas com essas arestas/nós para layout e desenho
    H = nx.Graph()
    H.add_nodes_from(nodes_of_interest)
    H.add_edges_from(used_edges)

    pos = nx.spring_layout(H)  # layout baseado apenas nos nós/arestas de interesse

    # Desenhar apenas os nós que ligam as pontes de interesse e as arestas em vermelho
    nx.draw_networkx_nodes(H, pos, nodelist=list(nodes_of_interest), node_color='lightblue', node_size=500)
    nx.draw_networkx_labels(H, pos, labels={n: str(n) for n in nodes_of_interest}, font_size=10, font_weight='bold')
    nx.draw_networkx_edges(H, pos, edgelist=used_edges, edge_color='red', width=3)

    plt.title("Pontes de Interesse (em vermelho) — nós conectores mostrados")
    plt.tight_layout()
    plt.savefig('graph.png')
# ...existing code...