import networkx as nx
import matplotlib.pyplot as plt

def plot_graph(num_islands, num_bridges, bridge_start, bridge_end, bridge_capacity):
    G = nx.Graph()
    G.add_nodes_from(range(1, num_islands + 1))
    
    for i in range(num_bridges):
        G.add_edge(bridge_start[i], bridge_end[i], weight=bridge_capacity[i])
    
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels)
    plt.title("Grafo das Ilhas e Pontes")
    
    # Salvar imagem em vez de mostrar (evita erro em ambientes sem display)
    plt.savefig('graph.png')
    print("Grafo salvo como 'graph.png'")
    # plt.show()  # Comente ou remova se quiser salvar apenas