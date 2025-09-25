from variables_input import read_input
from trucks import process_deliveries
from plot_graphs import plot_graph

# Ler entrada
num_islands, num_bridges, num_deliveries, bridge_start, bridge_end, bridge_capacity, delivery_origin, delivery_destination = read_input()

# Processar entregas
process_deliveries(num_deliveries, delivery_origin, delivery_destination, num_islands, num_bridges, bridge_start, bridge_end, bridge_capacity)

# Plotar grafo (opcional)
plot_graph(num_islands, num_bridges, bridge_start, bridge_end, bridge_capacity)