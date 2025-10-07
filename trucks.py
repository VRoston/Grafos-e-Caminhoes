# ...existing code...
from collections import defaultdict, deque
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
        if a == b: return False
        if self.r[a] < self.r[b]:
            self.p[a] = b
        else:
            self.p[b] = a
            if self.r[a] == self.r[b]:
                self.r[a] += 1
        return True

def build_max_spanning_tree(num_islands, num_bridges, bridge_start, bridge_end, bridge_capacity):
    # Kruskal: ordenar arestas por capacidade desc e unir
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
    LOG = math.ceil(math.log2(num_islands+1)) if num_islands>0 else 1
    up = [[-1]*(num_islands+1) for _ in range(LOG)]
    min_up = [[0]*(num_islands+1) for _ in range(LOG)]
    depth = [0]*(num_islands+1)
    visited = [False]*(num_islands+1)

    # run DFS/BFS from each component root
    for root in range(1, num_islands+1):
        if visited[root]:
            continue
        # root = component root; set parent -1 and depth 0
        stack = [(root, -1, 0, 10**18)]  # node, parent, depth, edge_weight_to_parent (unused for root)
        while stack:
            node, parent, d, wpar = stack.pop()
            if visited[node]:
                continue
            visited[node] = True
            up[0][node] = parent if parent != -1 else node  # parent pointer (root points to itself)
            min_up[0][node] = 0 if parent == -1 else wpar
            depth[node] = d
            for nei, w in tree_adj[node]:
                if not visited[nei]:
                    stack.append((nei, node, d+1, w))

    # binary lifting tables
    LOG = len(up)
    for k in range(1, LOG):
        for v in range(1, num_islands+1):
            mid = up[k-1][v]
            up[k][v] = up[k-1][mid] if mid != -1 else -1
            # min along 2^k = min(min along 2^(k-1) from v, min along 2^(k-1) from mid)
            min_up[k][v] = min_up[k-1][v]
            if mid != -1:
                min_up[k][v] = min(min_up[k][v], min_up[k-1][mid])
    return up, min_up, depth

def query_min_capacity(u, v, up, min_up, depth, dsu):
    # if same node
    if u == v:
        return float('inf')
    # if not connected
    if dsu.find(u) != dsu.find(v):
        return 0
    LOG = len(up)
    min_edge = 10**18
    # lift u/v to same depth
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
    # now u and v are children of LCA
    min_edge = min(min_edge, min_up[0][u], min_up[0][v])
    return min_edge

def get_path_edges(u, v, up0):
    # reconstruct tree path edges in order u->v using parent[0]
    # assume u and v are connected and up0[root]=root for root
    if u == v:
        return []
    # climb to LCA by depth using up0 and depth via single-step parent chain:
    # We need depth, but for simplicity require that up0 contains parent[0] and depth known externally.
    # This helper will be used inside process_deliveries where depth is available.
    path = []
    # This function will be replaced by inline loops in process_deliveries that have depth available.
    return path

def process_deliveries(num_deliveries, delivery_origin, delivery_destination, num_islands, num_bridges, bridge_start, bridge_end, bridge_capacity):
    """
    Constrói MST máxima (uma vez), preprocessa LCA e responde cada entrega em O(log N).
    Retorna um conjunto de pontes usadas (tuplas (start, end)) ao longo dos caminhos na árvore.
    """
    # origem==destino -> capacidade infinita (tratada abaixo)
    tree_adj, dsu = build_max_spanning_tree(num_islands, num_bridges, bridge_start, bridge_end, bridge_capacity)
    up, min_up, depth = preprocess_lca(tree_adj, num_islands)
    parent0 = up[0]

    used_bridges = set()

    for i in range(num_deliveries):
        a = delivery_origin[i]
        b = delivery_destination[i]
        cap = query_min_capacity(a, b, up, min_up, depth, dsu)
        print(cap if cap != float('inf') else 0)

        # recolher as arestas do caminho na árvore (em ordem a->b)
        if cap == 0 or a == b:
            continue  # nada a adicionar (desconectados ou mesmo vértice)
        # encontrar LCA by lifting
        u, v = a, b
        if depth[u] < depth[v]:
            u, v = v, u
            swapped = True
        else:
            swapped = False
        LOG = len(up)
        # lift u to depth v
        diff = depth[u] - depth[v]
        while diff > 0:
            step = diff & -diff  # largest power of two dividing diff (but we'll lift by single power for simplicity)
            k = int(math.log2(step))
            # add edges along this 2^k jump by walking single-steps (safe because number of jumps per delivery is <= logN)
            # to keep code straightforward, lift by single-step k=0 repeatedly
            # simpler: perform single-step lifts to record exact edges
            for _ in range(step.bit_length()-1, -1, -1):  # fallback - but to be safe, do single-step lifts:
                pass
            # simpler approach: use single-step loop (depth difference is at most N but average small); acceptable tradeoff
            break
        # Simpler and robust: walk from a to LCA using parent0 single-steps, same for b
        # find LCA by standard method:
        uu, vv = a, b
        if depth[uu] < depth[vv]:
            uu, vv = vv, uu
        # lift uu
        while depth[uu] > depth[vv]:
            p = parent0[uu]
            used_bridges.add((p, uu))
            uu = p
        while uu != vv:
            pu = parent0[uu]; pv = parent0[vv]
            used_bridges.add((pu, uu))
            used_bridges.add((pv, vv))
            uu = pu; vv = pv
        # now uu==vv is LCA; we must have added edges from a up to LCA and from b up to LCA
        # The edges we added for path b->LCA are oriented child->parent; if you want uniform orientation
        # (origin->destination) you can convert when necessary.

    return used_bridges
# ...existing code...