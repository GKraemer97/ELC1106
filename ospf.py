import math
import matplotlib.pyplot as plt
import networkx as nx

# Função para calcular a distância entre dois roteadores
def calcular_distancia(rota1, rota2):
    x1, y1 = rota1
    x2, y2 = rota2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Função para encontrar os roteadores no campo de visão de um roteador específico
def encontrar_roteadores_no_campo_visao(rota_atual, roteadores, campo_visao):
    roteadores_no_campo_visao = []
    for rota in roteadores:
        if rota == rota_atual:
            continue
        distancia = calcular_distancia(rota_atual, rota)
        if distancia <= campo_visao:
            roteadores_no_campo_visao.append(rota)
    return roteadores_no_campo_visao

# Função para construir a tabela de roteamento usando o algoritmo Dijkstra com custos
def construir_tabela_de_roteamento(rota_inicial, roteadores, campo_visao):
    tabela_roteamento = {}
    visitados = set()
    nao_visitados = set(roteadores)
    distancias = {rota: math.inf for rota in roteadores}
    distancias[rota_inicial] = 0

    while nao_visitados:
        rota_atual = None
        for rota in nao_visitados:
            if rota_atual is None or distancias[rota] < distancias[rota_atual]:
                rota_atual = rota

        nao_visitados.remove(rota_atual)
        visitados.add(rota_atual)

        roteadores_vizinhos = encontrar_roteadores_no_campo_visao(rota_atual, roteadores, campo_visao)
        for rota_vizinha in roteadores_vizinhos:
            distancia = distancias[rota_atual] + calcular_distancia(rota_atual, rota_vizinha)
            if distancia < distancias[rota_vizinha]:
                distancias[rota_vizinha] = distancia
                tabela_roteamento[rota_vizinha] = rota_atual

    return tabela_roteamento


# Configurações
num_linhas = 5
num_colunas = 5
campo_visao = 2

# Criar a matriz de roteadores
roteadores = []
for i in range(num_linhas):
    for j in range(num_colunas):
        roteadores.append((i, j))

# Construir a tabela de roteamento para cada roteador
tabelas_de_roteamento = {}
for rota_inicial in roteadores:
    tabela_roteamento = construir_tabela_de_roteamento(rota_inicial, roteadores, campo_visao)
    tabelas_de_roteamento[rota_inicial] = tabela_roteamento


# Imprimir as tabelas de roteamento de cada roteador
for rota_inicial, tabela_roteamento in tabelas_de_roteamento.items():
    print(f"Tabela de Roteamento para o Roteador {rota_inicial}:")
    print("Destino\t\tPróximo Salto")
    for destino, proximo_salto in tabela_roteamento.items():
        print(f"{destino}\t\t{proximo_salto}")
    print()
    
# Plotar os roteadores e os caminhos entre eles
G = nx.Graph()
G.add_nodes_from(roteadores)
for rota_inicial, tabela_roteamento in tabelas_de_roteamento.items():
    for destino, proximo_salto in tabela_roteamento.items():
        custo = int(calcular_distancia(rota_inicial, destino))
        G.add_edge(rota_inicial, proximo_salto, custo=custo)

plt.figure(figsize=(8, 6))
pos = {rota: rota for rota in roteadores}
nx.draw_networkx(G, pos=pos, with_labels=True, node_size=500, node_color='lightblue', font_weight='bold', font_color='black', edge_color='gray')

# Adicionar rótulos com os custos das arestas
custos = nx.get_edge_attributes(G, 'custo')
nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=custos, font_size=8)

plt.title('Topologia de Roteadores')
plt.axis('off')
plt.show()
