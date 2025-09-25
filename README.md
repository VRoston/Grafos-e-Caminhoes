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
   cd /home/victor/puc/Grafos-e-Caminhoes
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

### Exemplo de Entrada
```
4 5 4
1 2 9
1 3 0
2 3 8
2 4 7
3 4 4
1 4
2 1
3 1
4 3
```

### Exemplo de Saída
```
7
9
8
7
Grafo salvo como 'graph.png'
```

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
</markdown>// filepath: /Grafos-e-Caminhoes/README.md
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

### Exemplo de Entrada
```
4 5 4
1 2 9
1 3 0
2 3 8
2 4 7
3 4 4
1 4
2 1
3 1
4 3
```

### Exemplo de Saída
```
7
9
8
7
Grafo salvo como 'graph.png'
```

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