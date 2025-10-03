import networkx as nx
import matplotlib.pyplot as plt

def plot_graph(num_islands, num_bridges, bridge_start, bridge_end, bridge_capacity, used_bridges):
    G = nx.Graph()
    G.add_nodes_from(range(1, num_islands + 1))
    
    # Adicionar todas as arestas
    for i in range(num_bridges):
        G.add_edge(bridge_start[i], bridge_end[i], weight=bridge_capacity[i])
    
    pos = nx.spring_layout(G)
    
    # Desenhar nós
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold')
    
    # Desenhar arestas normais (cinza)
    nx.draw_networkx_edges(G, pos, edge_color='gray', width=2)
    
    # Desenhar arestas de interesse (vermelho)
    if used_bridges:
        used_edges = list(used_bridges)
        nx.draw_networkx_edges(G, pos, edgelist=used_edges, edge_color='red', width=4)
    
    # Rótulos das arestas
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels)
    
    plt.title("Grafo das Ilhas e Pontes (Pontes de Interesse em Vermelho)")
    
    # Salvar imagem
    plt.savefig('graph.png')
    