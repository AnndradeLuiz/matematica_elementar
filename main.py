import math
import matplotlib.pyplot as plt
import random


def f(x, y):
    return x**2 + y**2


class AlgoritmoGenetico:
    def __init__(self, funcao, intervalo=(-10, 10),
                tamanho_pop=30, geracoes=1000, taxa_mutacao=0.1):
        self.funcao = funcao
        self.intervalo = intervalo
        self.tamanho_pop = tamanho_pop
        self.geracoes = geracoes
        self.taxa_mutacao = taxa_mutacao

    def criar_individuo(self):
        x = random.uniform(self.intervalo[0], self.intervalo[1])
        y = random.uniform(self.intervalo[0], self.intervalo[1])
        return (x, y)

    def fitness(self, ponto):
        return -self.funcao(ponto[0], ponto[1])

    def selecao(self, populacao):
        populacao.sort(key=self.fitness, reverse=True)
        return populacao[:2]

    def crossover(self, pai, mae):
        alpha = random.random()
        x_filho = alpha * pai[0] + (1 - alpha) * mae[0]
        y_filho = alpha * pai[1] + (1 - alpha) * mae[1]
        return (x_filho, y_filho)

    def mutacao(self, individuo):
        if random.random() < self.taxa_mutacao:
            x_mutado = individuo[0] + random.uniform(-1, 1)
            y_mutado = individuo[1] + random.uniform(-1, 1)
            x_mutado = max(min(x_mutado, self.intervalo[1]), self.intervalo[0])
            y_mutado = max(min(y_mutado, self.intervalo[1]), self.intervalo[0])
            return (x_mutado, y_mutado)
        return individuo

    def executar(self):
        populacao = [self.criar_individuo() for _ in range(self.tamanho_pop)]
        melhor = min(populacao, key=lambda p: self.funcao(p[0], p[1]))
        trajetoria = [melhor]
        valores_f = [self.funcao(melhor[0], melhor[1])]

        for geracao in range(self.geracoes):
            nova_populacao = []
            pais = self.selecao(populacao)

            while len(nova_populacao) < self.tamanho_pop:
                filho = self.crossover(pais[0], pais[1])
                filho = self.mutacao(filho)
                nova_populacao.append(filho)

            populacao = nova_populacao
            candidato = min(populacao, key=lambda p: self.funcao(p[0], p[1]))

            if self.funcao(
                    candidato[0],
                    candidato[1]) < self.funcao(
                    melhor[0],
                    melhor[1]):
                melhor = candidato
                trajetoria.append(melhor)
                valores_f.append(self.funcao(melhor[0], melhor[1]))

            if self.funcao(melhor[0], melhor[1]) <= 1e-3:
                print(f"Critério de erro atingido na geração {geracao}")
                break

        print(f"Melhor ponto encontrado: {melhor}")
        print(f"Total de gerações: {geracao + 1}")
        plotar_graficos([], melhor, (0, 0), None, tipo=0,
                        trajetoria=trajetoria, valores_f=valores_f)
        return melhor, geracao + 1, trajetoria


class Gerar_Pontos:
    def __init__(self):
        self.pontos_xy = []
        self.menor_p = None

    def gerar_pts_1_grau(self, a, b):
        self.pontos_xy = []
        self.a = a
        self.b = b
        self.intercept_y = (0, b)

        for _ in range(10):
            x = random.randint(-10, 10)
            y = (a * x) + b
            self.pontos_xy.append((x, y))

        print("Pontos iniciais gerados:")
        for ponto in self.pontos_xy:
            print(ponto)

        self.menor_p, self.total_iter, self.trajetoria, self.valores_f = self.buscar_melhor_ponto_origem(
            funcao_segundo_grau=False)
        print(f"Total de iterações (1º grau): {self.total_iter}")

        return self.pontos_xy, self.intercept_y, self.menor_p

    def gerar_pts_2_grau(self, a, b, c):
        self.pontos_xy = []
        self.a = a
        self.b = b
        self.c = c
        self.intercept_y = (0, c)

        for _ in range(10):
            x = random.randint(-10, 10)
            y = (a * x**2) + (b * x) + c
            self.pontos_xy.append((x, y))

        print("Pontos iniciais gerados:")
        for ponto in self.pontos_xy:
            print(ponto)

        delta = (b**2) - (4 * a * c)
        xv = -b / (2 * a)
        yv = -delta / (4 * a)
        self.menor_p = (xv, yv)

        self.menor_p, self.total_iter, self.trajetoria, self.valores_f = self.buscar_melhor_ponto_origem(
            funcao_segundo_grau=True)
        print(f"Total de iterações (2º grau): {self.total_iter}")

        if delta > 0:
            x1 = ((-b) + math.sqrt(delta)) / (2 * a)
            x2 = ((-b) - math.sqrt(delta)) / (2 * a)
            raizes = [(x1, 0), (x2, 0)]
        elif delta == 0:
            x = -b / (2 * a)
            raizes = [(x, 0)]
        else:
            raizes = []

        return self.pontos_xy, self.menor_p, self.intercept_y, raizes

    def buscar_melhor_ponto_origem(
            self,
            iter_max=100000,
            erro_aceitavel=1e-3,
            funcao_segundo_grau=False):
        populacao = []
        intervalo = 10.0
        fator_reducao = 0.97
        sem_melhoria = 0
        max_sem_melhoria = 5000
        melhor_iter = 0
        valores_f = []

        for _ in range(10):
            x = random.uniform(-intervalo, intervalo)
            y = (
                self.a *
                x**2 +
                self.b *
                x +
                self.c) if funcao_segundo_grau else (
                self.a *
                x +
                self.b)
            populacao.append((x, y))

        melhor_ponto = min(populacao, key=lambda p: f(p[0], p[1]))
        trajetoria = [melhor_ponto]
        valores_f.append(f(melhor_ponto[0], melhor_ponto[1]))

        for i in range(iter_max):
            nova_populacao = []

            for _ in range(9):
                x = random.uniform(
                    melhor_ponto[0] - intervalo,
                    melhor_ponto[0] + intervalo)
                y = (
                    self.a *
                    x**2 +
                    self.b *
                    x +
                    self.c) if funcao_segundo_grau else (
                    self.a *
                    x +
                    self.b)
                nova_populacao.append((x, y))

            nova_populacao.append(melhor_ponto)

            populacao = [
                novo if f(*novo) < f(*antigo) else antigo
                for antigo, novo in zip(populacao, nova_populacao)
            ]

            novo_melhor = min(populacao, key=lambda p: f(p[0], p[1]))

            if f(*novo_melhor) < f(*melhor_ponto):
                melhor_ponto = novo_melhor
                intervalo = max(intervalo * fator_reducao, 1e-5)
                melhor_iter = i + 1
                sem_melhoria = 0
                trajetoria.append(melhor_ponto)
                valores_f.append(f(melhor_ponto[0], melhor_ponto[1]))
            else:
                sem_melhoria += 1

            if sem_melhoria >= max_sem_melhoria:
                print(f"Parando por estagnação após {sem_melhoria} iterações.")
                break

            if f(*melhor_ponto) <= erro_aceitavel:
                print(f"Critério de erro atingido na iteração {i + 1}")
                break

            if (i + 1) % 1000 == 0:
                print(f"Iteração {i +
                                1}: Melhor ponto = {melhor_ponto}, f(x,y) = {f(*
                                                                                melhor_ponto):.6f}"
                                                                                )

        print(f"Melhor ponto encontrado na iteração {melhor_iter}")
        print(f"Total de iterações realizadas: {i + 1}")
        return melhor_ponto, i + 1, trajetoria, valores_f


class Calcular_Funcao(Gerar_Pontos):
    def __init__(self):
        super().__init__()

    def calcular(self, escolha):
        if escolha == 1:
            tipo = 1
            print("Você escolheu a função do 1º grau, que tem forma: y = ax + b")
            try:
                a = int(input("Digite o valor de a: "))
                if a == 0:
                    print(
                        "O valor de 'a' não pode ser zero para uma função do 1º grau.")
                    return
                b = int(input("Digite o valor de b: "))

                pontos, intercept_y, menor_p = self.gerar_pts_1_grau(a, b)

                print(f"Função gerada: y = {a}x + {b}")
                print(f"Menor ponto encontrado: {menor_p}")

                plotar_graficos(
                    pontos,
                    menor_p,
                    intercept_y,
                    None,
                    tipo,
                    self.trajetoria,
                    self.valores_f)

            except ValueError:
                print("Entrada inválida. Digite apenas números inteiros.")

        elif escolha == 2:
            tipo = 2
            print("Você escolheu a função do 2° grau, que tem forma: y = ax² + bx + c")
            try:
                a = int(input("Digite o valor de a: "))
                if a == 0:
                    print(
                        "O valor de 'a' não pode ser zero para uma função do 2º grau.")
                    return
                b = int(input("Digite o valor de b: "))
                c = int(input("Digite o valor de c: "))

                pontos, menor_p, intercept_y, raizes = self.gerar_pts_2_grau(
                    a, b, c)

                print(f"Função gerada: y = {a}x² + {b}x + {c}")
                print(f"Menor ponto encontrado: {menor_p}")

                plotar_graficos(
                    pontos,
                    menor_p,
                    intercept_y,
                    raizes,
                    tipo,
                    self.trajetoria,
                    self.valores_f)

            except ValueError:
                print("Entrada inválida. Digite apenas números inteiros.")
        else:
            print("Escolha inválida.")


def plotar_graficos(
        pontos,
        menor_p,
        intercept_y,
        raizes,
        tipo,
        trajetoria,
        valores_f):
    if pontos:
        fig1, ax1 = plt.subplots()
        x, y = zip(*pontos)
        cor = 'b' if tipo == 1 else 'm'
        ax1.plot(x, y, 'o', color=cor, label='Pontos gerados')
        ax1.plot(0, 0, 'o', color='gray', label='Origem (0,0)')
        ax1.plot(
            menor_p[0],
            menor_p[1],
            'o',
            color='c',
            label=f'Melhor ponto{
                menor_p[0],
                menor_p[1]}')
        ax1.plot(
            intercept_y[0],
            intercept_y[1],
            'o',
            color='k',
            label='Intercepto em y')

        plt.axhline(0, color='black', linewidth=1)
        plt.axvline(0, color='black', linewidth=1)
        plt.xlabel("Eixo X")
        plt.ylabel("Eixo Y")

        if raizes:
            for i, raiz in enumerate(raizes):
                ax1.plot(
                    raiz[0],
                    raiz[1],
                    'o',
                    color='y',
                    label=f"Raiz {
                        i + 1}"
                )

        ax1.set_title("Gráfico dos Pontos")
        ax1.legend()
        ax1.grid(True)

    if trajetoria:
        fig2, ax2 = plt.subplots()
        x_t, y_t = zip(*trajetoria)
        ax2.plot(
            x_t,
            y_t,
            linestyle='--',
            color='orange',
            marker='x',
            label='Trajetória')
        ax2.plot(0, 0, 'o', color='gray', label='Origem (0,0)')
        ax2.plot(
            menor_p[0],
            menor_p[1],
            'o',
            color='c',
            label=f'Melhor ponto{
                menor_p[0],
                menor_p[1]}'
                )
        ax2.set_title("Trajetória de Otimização")
        ax2.legend()
        ax2.grid(True)

    if valores_f:
        fig3, ax3 = plt.subplots()
        ax3.plot(valores_f, color='purple')
        ax3.set_title("Evolução da Função f(x,y)")
        ax3.set_xlabel("Iterações")
        ax3.set_ylabel("f(x,y)")
        ax3.set_yscale('log')
        ax3.grid(True)

    plt.show()


if __name__ == '__main__':
    escolha = Calcular_Funcao()
    while True:
        try:
            opcao = int(input(
                "\nDigite [1] para calcular função do 1° Grau:\n"
                "Digite [2] para calcular função do 2° Grau:\n"
                "Digite [0] para sair:\n"
                "Qual a opção: "
            ))
            if opcao == 0:
                print("Até logo!")
                break
            elif opcao == 1 or opcao == 2:
                escolha.calcular(opcao)
                usar_genetico = input(
                    "Deseja usar o algoritmo genético? [s/n]: ").lower() == 's'
                if usar_genetico:
                    ag = AlgoritmoGenetico(funcao=f)
                    menor, iteracoes, trajetoria = ag.executar()
            else:
                print("Opção Inválida")
        except ValueError:
            print("Digite um número inteiro válido.")
