# Um roteirizador inteligente é um sistema que utiliza algoritmos avançados e inteligência 
# artificial para otimizar rotas em logística, transporte e entregas


# Classe que irá representar os bairros
class Bairro:
    # Inicializando a rota

    def __init__(self, bairro_dict=None, direcionado=True):
        self.bairro_dict = bairro_dict or {}
        self.direcionado = direcionado
        if not direcionado:
            self.nao_direcionado()

    # Criando o gráfico
    def nao_direcionado(self):
        for a in list(self.bairro_dict.keys()):
            for (b, dist) in self.bairro_dict[a].items():
                self.bairro_dict.setdefault(b, {})[a] = dist

    # Adiciona as rotas entre os pontos destinados
    def conexao(self, A, B, distance=1):
        self.bairro_dict.setdefault(A, {})[B] = distance
        if not self.direcionado:
            self.bairro_dict.setdefault(B, {})[A] = distance

    # Calcula os vizinhos
    def get(self, a, b=None):
        links = self.bairro_dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)

    # Retorna a lista dos bairros
    def nodes(self):
        s1 = set([k for k in self.bairro_dict.keys()])
        s2 = set([k2 for v in self.bairro_dict.values() for k2, v2 in v.items()])
        nodes = s1.union(s2)
        return list(nodes)


# Essa classe representa um ponto
class Node:
    # Inicializando a classe
    def __init__(self, name: str, parent: str):
        self.name = name
        self.parent = parent
        self.g = 0  # Distancia inicial
        self.h = 0  # Distancia entre os pontos
        self.f = 0  # Total percorrido

    # Comparação entre os nós
    def __eq__(self, other):
        return self.name == other.name

    # Nós curtos
    def __lt__(self, other):
        return self.f < other.f

    # Captura dos nós
    def __repr__(self):
        return ('({0},{1})'.format(self.name, self.f))


# Busca A*
def astar_search(bairro, distancia, start, end):
    # Criação distância percorrida entre os bairros
    open = []
    closed = []
    # Criando o ponto inicial ao ponto final
    no_inicial = Node(start, None)
    goal_node = Node(end, None)
    # Adicionando o ponto inicial
    open.append(no_inicial)

    # Loop quando a lista está vazia
    while len(open) > 0:
        #  Classificação da lista para obter a menor distância
        open.sort()
        # Obtenha o ponto com a menor distância
        conexao_atual = open.pop(0)
        # Adiciona o ponto atual a lista fechada
        closed.append(conexao_atual)

        # checagem se atingiu o objetivo e retorna o caminho
        if conexao_atual == goal_node:
            caminho = []
            while conexao_atual != no_inicial:
                caminho.append(conexao_atual.name + ': ' + str(conexao_atual.g))
                conexao_atual = conexao_atual.parent
            caminho.append(no_inicial.name + ': ' + str(no_inicial.g))
            # retorna o caminho reverso
            return caminho[::-1]
        # obtem os vizinhos
        vizinhos = bairro.get(conexao_atual.name)
        # loop de vizinhos
        for key, value in vizinhos.items():
            # cria o nó vizinho
            vizinho = Node(key, conexao_atual)
            # verifica se o vizinho está na lista fechada
            if (vizinho in closed):
                continue
            # calcula todo o caminho percorrido
            vizinho.g = conexao_atual.g + bairro.get(conexao_atual.name, vizinho.name)
            vizinho.h = distancia.get(vizinho.name)
            vizinho.f = vizinho.g + vizinho.h
            # checagem se o vizinho está na lista aberta
            if (add_to_open(open, vizinho) == True):
                # Tudo está ok, adicione vizinho à lista aberta
                open.append(vizinho)
    # nenhum caminho foi encontrado
    return None


# Verifique se um vizinho deve ser adicionado à lista aberta
def add_to_open(open, vizinho):
    for node in open:
        if (vizinho == node and vizinho.f > node.f):
            return False
    return True


# O principal ponto de entrada para as rotas
def main():
    # Criação de rotas
    bairro = Bairro()
    # crie as rotas de conexão
    # Distância entre os bairros
    bairro.conexao('A', 'B', 0.7)
    bairro.conexao('A', 'C', 0.5)
    bairro.conexao('A', 'D', 1.5)
    bairro.conexao('B', 'E', 0.2)
    bairro.conexao('C', 'E', 0.2)
    bairro.conexao('D', 'F', 0.8)
    bairro.conexao('E', 'F', 2)
    bairro.conexao('E', 'G', 0.8)
    bairro.conexao('F', 'H', 0.4)
    bairro.conexao('G', 'I', 0.4)
    bairro.conexao('H', 'I', 0.6)
    # Faz o gráfico não direcionado
    bairro.nao_direcionado()
    # Distância estreita para um destino
    distancia = {}
    distancia['A'] = 1.9
    distancia['B'] = 1.4
    distancia['C'] = 1.4
    distancia['D'] = 1.8
    distancia['E'] = 1.2
    distancia['F'] = 1.0
    distancia['G'] = 0.4
    distancia['H'] = 0.6
    distancia['I'] = 0

    Barroca_lanches = 'A'
    entrega = str(input("Digite em qual bairro será feita e entrega (A-I) = ").upper())
    # Execute o algoritmo de pesquisa
    caminho = astar_search(bairro, distancia, Barroca_lanches, entrega)
    print("A melhor rota e os pontos que você deve passar para chegar no seu destino são:")
    print(caminho)

# Diga ao python para executar o método principal
if __name__ == "__main__": main()
