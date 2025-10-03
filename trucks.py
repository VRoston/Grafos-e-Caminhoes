def find_max_capacity(origin, destination, num_islands, num_bridges, bridge_start, bridge_end, bridge_capacity):
    """
    Calcula a capacidade máxima de carga entre origem e destino usando uma variação do algoritmo de Dijkstra.
    Retorna a capacidade máxima e o caminho usado (lista de tuplas (start, end)).
    """
    if origin == destination:
        return float('inf'), []  # Capacidade infinita se origem e destino forem iguais
    
    # Inicializa arrays para capacidades máximas, visitação e predecessores
    max_cap = [0] * (num_islands + 1)  # Capacidade máxima para chegar em cada ilha
    max_cap[origin] = float('inf')     # Origem tem capacidade infinita
    visited = [False] * (num_islands + 1)  # Marca ilhas já processadas
    predecessor = [-1] * (num_islands + 1)  # Rastreia o caminho (predecessor de cada ilha)
    
    # Loop principal: processa cada ilha (até num_islands vezes)
    for _ in range(num_islands):
        # Encontra a ilha não visitada com a maior capacidade máxima
        current = -1
        for i in range(1, num_islands + 1):
            if not visited[i] and (current == -1 or max_cap[i] > max_cap[current]):
                current = i
        
        # Se não há ilha válida ou capacidade zero, para
        if current == -1 or max_cap[current] == 0:
            break
            
        visited[current] = True  # Marca ilha como visitada
        
        # Se chegou ao destino, reconstrói o caminho
        if current == destination:
            path = []
            node = destination
            while node != origin:
                prev = predecessor[node]
                if prev == -1:
                    break  # Caminho inválido
                path.append((prev, node))  # Adiciona aresta ao caminho
                node = prev
            path.reverse()  # Inverte para ordem origem -> destino
            return max_cap[destination], path
        
        # Atualiza capacidades dos vizinhos via pontes
        for i in range(num_bridges):
            neighbor = -1
            bridge_cap = 0
            
            # Verifica se a ponte conecta a ilha atual
            if bridge_start[i] == current:
                neighbor = bridge_end[i]
                bridge_cap = bridge_capacity[i]
            elif bridge_end[i] == current:
                neighbor = bridge_start[i]
                bridge_cap = bridge_capacity[i]
            
            # Se há vizinho não visitado, calcula nova capacidade
            if neighbor != -1 and not visited[neighbor]:
                new_capacity = min(max_cap[current], bridge_cap)  # Capacidade limitada pela ponte mais fraca
                if new_capacity > max_cap[neighbor]:
                    max_cap[neighbor] = new_capacity
                    predecessor[neighbor] = current  # Atualiza predecessor
    
    # Retorna capacidade e caminho vazio se não encontrou caminho
    return max_cap[destination], []

def process_deliveries(num_deliveries, delivery_origin, delivery_destination, num_islands, num_bridges, bridge_start, bridge_end, bridge_capacity):
    """
    Processa todas as entregas, calcula capacidades e coleta pontes usadas.
    Retorna um conjunto de pontes de interesse (tuplas (start, end)).
    """
    used_bridges = set()  # Conjunto para armazenar pontes usadas (evita duplicatas)
    
    # Para cada entrega
    for i in range(num_deliveries):
        # Calcula capacidade e caminho para a entrega
        result, path = find_max_capacity(delivery_origin[i], delivery_destination[i], num_islands, num_bridges, bridge_start, bridge_end, bridge_capacity)
        print(result if result != float('inf') else 0)  # Imprime capacidade (0 se infinita)
        
        # Adiciona pontes do caminho ao conjunto de pontes usadas
        for edge in path:
            used_bridges.add(edge)
    
    return used_bridges