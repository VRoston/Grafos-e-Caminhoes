from collections import deque
import math

class DSU:
    def __init__(self, n):
        self.p = list(range(n+1))
        self.r = [0]*(n+1)

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        a = self.find(a); b = self.find(b)
        if a == b:
            return False
        if self.r[a] < self.r[b]:
            self.p[a] = b
        else:
            self.p[b] = a
            if self.r[a] == self.r[b]:
                self.r[a] += 1
        return True

def build_max_spanning_tree(num_islands, num_bridges, bridge_start, bridge_end, bridge_capacity):
    edges = [(bridge_capacity[i], bridge_start[i], bridge_end[i]) for i in range(num_bridges)]
    edges.sort(reverse=True, key=lambda x: x[0])
    dsu = DSU(num_islands)
    tree_adj = [[] for _ in range(num_islands+1)]
    for w,u,v in edges:
        if dsu.union(u,v):
            tree_adj[u].append((v,w))
            tree_adj[v].append((u,w))
    return tree_adj, dsu

def preprocess_lca(tree_adj, num_islands):
    # prepara up[k][v] (2^k ancestor) e min_up[k][v] (min edge ao longo do salto)
    LOG = max(1, math.ceil(math.log2(num_islands+1)))
    up = [[0]*(num_islands+1) for _ in range(LOG)]
    min_up = [[10**18]*(num_islands+1) for _ in range(LOG)]
    depth = [0]*(num_islands+1)
    visited = [False]*(num_islands+1)

    # BFS/DFS em cada componente para preencher up[0], min_up[0], depth
    for root in range(1, num_islands+1):
        if visited[root]:
            continue
        stack = [(root, root, 0, 10**18)]  # node, parent, depth, edge_weight_to_parent
        while stack:
            node, parent, d, wpar = stack.pop()
            if visited[node]:
                continue
            visited[node] = True
            up[0][node] = parent  # para raiz parent == root
            min_up[0][node] = 0 if node == parent else wpar
            depth[node] = d
            for nei, w in tree_adj[node]:
                if not visited[nei]:
                    stack.append((nei, node, d+1, w))

    # preencher níveis superiores
    for k in range(1, LOG):
        for v in range(1, num_islands+1):
            mid = up[k-1][v]
            up[k][v] = up[k-1][mid]
            min_up[k][v] = min(min_up[k-1][v], min_up[k-1][mid])

    return up, min_up, depth

def lca(u, v, up, depth):
    if u == v:
        return u
    if depth[u] < depth[v]:
        u, v = v, u
    LOG = len(up)
    # subir u até a mesma profundidade de v
    diff = depth[u] - depth[v]
    for k in range(LOG):
        if diff & (1<<k):
            u = up[k][u]
    if u == v:
        return u
    for k in reversed(range(LOG)):
        if up[k][u] != up[k][v]:
            u = up[k][u]
            v = up[k][v]
    return up[0][u]

def query_min_capacity(u, v, up, min_up, depth, dsu):
    # retorna 0 se desconectados, inf se u==v (tratado como 0 na impressão)
    if dsu.find(u) != dsu.find(v):
        return 0
    if u == v:
        return float('inf')
    LOG = len(up)
    min_edge = 10**18
    if depth[u] < depth[v]:
        u, v = v, u
    diff = depth[u] - depth[v]
    for k in range(LOG):
        if diff & (1<<k):
            min_edge = min(min_edge, min_up[k][u])
            u = up[k][u]
    if u == v:
        return min_edge
    for k in reversed(range(LOG)):
        if up[k][u] != up[k][v]:
            min_edge = min(min_edge, min_up[k][u], min_up[k][v])
            u = up[k][u]
            v = up[k][v]
    min_edge = min(min_edge, min_up[0][u], min_up[0][v])
    return min_edge

def collect_path_edges(node, ancestor, parent0, collector):
    # adiciona arestas (parent, child) do node até ancestor (exclusive ancestor)
    while node != ancestor:
        parent = parent0[node]
        # parent pode ser igual a node se node for raiz; proteger contra loop infinito
        if parent == node:
            break
        collector.add((parent, node))
        node = parent

def process_deliveries(num_deliveries, delivery_origin, delivery_destination, num_islands, num_bridges, bridge_start, bridge_end, bridge_capacity):
    tree_adj, dsu = build_max_spanning_tree(num_islands, num_bridges, bridge_start, bridge_end, bridge_capacity)
    up, min_up, depth = preprocess_lca(tree_adj, num_islands)
    parent0 = up[0]
    used_bridges = set()

    for i in range(num_deliveries):
        a = delivery_origin[i]
        b = delivery_destination[i]
        cap = query_min_capacity(a, b, up, min_up, depth, dsu)
        # imprimir conforme comportamento anterior: mesma ilha => 0, desconexo => 0
        print(0 if cap == float('inf') or cap == 0 else int(cap))

        if cap == 0 or a == b:
            continue

        anc = lca(a, b, up, depth)
        # coletar arestas de a->LCA e b->LCA (em orientação parent->child)
        collect_path_edges(a, anc, parent0, used_bridges)
        collect_path_edges(b, anc, parent0, used_bridges)

    return used_bridges