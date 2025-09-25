def find_max_capacity(origin, destination, num_islands, num_bridges, bridge_start, bridge_end, bridge_capacity):
    if origin == destination:
        return float('inf'), []
    
    max_cap = [0] * (num_islands + 1)
    max_cap[origin] = float('inf')
    visited = [False] * (num_islands + 1)
    predecessor = [-1] * (num_islands + 1)  # Para rastrear o caminho
    
    for _ in range(num_islands):
        current = -1
        for i in range(1, num_islands + 1):
            if not visited[i] and (current == -1 or max_cap[i] > max_cap[current]):
                current = i
        
        if current == -1 or max_cap[current] == 0:
            break
            
        visited[current] = True
        
        if current == destination:
            # Reconstruir caminho
            path = []
            node = destination
            while node != origin:
                prev = predecessor[node]
                if prev == -1:
                    break
                path.append((prev, node))
                node = prev
            path.reverse()
            return max_cap[destination], path
        
        for i in range(num_bridges):
            neighbor = -1
            bridge_cap = 0
            
            if bridge_start[i] == current:
                neighbor = bridge_end[i]
                bridge_cap = bridge_capacity[i]
            elif bridge_end[i] == current:
                neighbor = bridge_start[i]
                bridge_cap = bridge_capacity[i]
            
            if neighbor != -1 and not visited[neighbor]:
                new_capacity = min(max_cap[current], bridge_cap)
                if new_capacity > max_cap[neighbor]:
                    max_cap[neighbor] = new_capacity
                    predecessor[neighbor] = current
    
    return max_cap[destination], []

def process_deliveries(num_deliveries, delivery_origin, delivery_destination, num_islands, num_bridges, bridge_start, bridge_end, bridge_capacity):
    used_bridges = set()  # Conjunto de pontes usadas (tuplas (start, end))
    
    for i in range(num_deliveries):
        result, path = find_max_capacity(delivery_origin[i], delivery_destination[i], num_islands, num_bridges, bridge_start, bridge_end, bridge_capacity)
        print(result if result != float('inf') else 0)
        
        # Adicionar pontes do caminho ao conjunto
        for edge in path:
            used_bridges.add(edge)
    
    return used_bridges