# Grafos e Caminhões

Este projeto resolve o problema de encontrar a capacidade máxima de carga que um caminhão pode transportar entre ilhas conectadas por pontes, considerando as limitações de peso das pontes. Ele usa algoritmos de grafos para calcular o caminho com maior capacidade mínima entre origem e destino de cada entrega.

## Funcionalidades
- Leitura de entrada com ilhas, pontes e entregas
- Cálculo da capacidade máxima para cada entrega
- Visualização do grafo das ilhas e pontes (com destaque para pontes usadas)
- Modularização em arquivos separados para melhor organização

## Como Executar

### Pré-requisitos
- Python 3.6 ou superior
- Sistema Linux (ou similar, com suporte a ambientes virtuais)

### Passos para Execução

1. **Clone ou navegue para o diretório do projeto:**
   ```bash
   cd ./Grafos-e-Caminhoes
   ```

2. **Crie um ambiente virtual:**
   ```bash
   python3 -m venv venv
   ```

3. **Ative o ambiente virtual:**
   ```bash
   source venv/bin/activate
   ```

4. **Instale as dependências:**
   ```bash
   pip install networkx matplotlib
   ```

5. **Execute o programa:**
   - Para entrada via terminal:
     ```bash
     python3 main.py
     ```
     Digite a entrada no formato esperado (exemplo abaixo).

   - Para entrada via arquivo:
     ```bash
     python3 main.py < entrada.txt
     ```

## Visão geral do funcionamento

O objetivo do trabalho é, para cada entrega (origem, destino), determinar a máxima carga que um caminhão pode atravessar entre duas ilhas considerando as capacidades máximas das pontes. Em vez de rodar um algoritmo de caminho mais largo (variante de Dijkstra) para cada consulta, a solução usa uma abordagem mais eficiente em instâncias grandes:

1. Construção de uma Árvore Geradora Máxima (Maximum Spanning Tree, MST máxima) com Kruskal:
   - Ordena todas as pontes por capacidade decrescente e aplica DSU (Union-Find) para montar a árvore.
   - Complexidade: O(E log E) para ordenar as arestas.

2. Preprocessamento LCA (Lowest Common Ancestor) com binary lifting:
   - Roda uma DFS/BFS na(s) componente(s) para preencher parent[0], depth e o peso da aresta até o pai.
   - Constrói tabelas de subida (up[k][v]) e o mínimo de aresta ao longo do salto (min_up[k][v]).
   - Complexidade: O(N log N) memória e tempo para preenchimento das tabelas.

3. Resposta a cada entrega:
   - A resposta (capacidade máxima mínima ao longo do caminho) é exatamente o mínimo das arestas no caminho entre os dois vértices na MST máxima. Isso decorre da propriedade que a MST máxima preserva os melhores caminhos "bottleneck" entre pares de vértices.
   - Usa binary lifting para subir os nós até o LCA e obter o mínimo ao longo do caminho em O(log N) por consulta.
   - Se os vértices não estiverem conectados, a resposta é 0; se for o mesmo vértice, a resposta é 0 (tratada como infinito internamente).

Resumo de complexidades:
- Construção da MST: O(E log E)
- Preprocessamento LCA: O(N log N)
- Cada consulta: O(log N)
Essa abordagem é muito vantajosa quando há muitas consultas (entregas), pois evita rodar Dijkstra por entrega.

## Formato da entrada / saída

Formato de entrada (padrão):
- Primeira linha: N M Q
  - N = número de ilhas (vértices)
  - M = número de pontes (arestas)
  - Q = número de entregas (consultas)
- Próximas M linhas: u v w (ponte entre u e v com capacidade w)
- Próximas Q linhas: a b (origem e destino das entregas)

Saída:
- Uma linha por entrega com a capacidade máxima (inteiro).
- Exemplo esperado:

## Estrutura dos Arquivos
- `main.py`: Ponto de entrada do programa
- `variables_input.py`: Função para ler entrada
- `trucks.py`: Algoritmo para calcular capacidades e processar entregas
- `plot_graphs.py`: Função para plotar o grafo
- `README.md`: Este arquivo

## Observações
- O grafo é salvo como `graph.png` após a execução
- Pontes de interesse (usadas nas entregas) são destacadas em vermelho no plot
- Para desativar o ambiente virtual: `deactivate`
</markdown>