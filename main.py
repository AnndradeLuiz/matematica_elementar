import math
import matplotlib.pyplot as plt
import random

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

        self.menor_p, self.total_iter, self.trajetoria = self.buscar_melhor_ponto_origem(funcao_segundo_grau=False)
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

        delta = (b**2) - (4*a*c)
        xv = -b / (2*a)
        yv = -delta / (4*a)
        self.menor_p = (xv, yv)

        self.menor_p, self.total_iter, self.trajetoria = self.buscar_melhor_ponto_origem(funcao_segundo_grau=True)
        print(f"Total de iterações (2º grau): {self.total_iter}")

        if delta > 0:
            x1 = ((-b) + math.sqrt(delta)) / (2*a)
            x2 = ((-b) - math.sqrt(delta)) / (2*a)
            raizes = [(x1, 0), (x2, 0)]
        elif delta == 0:
            x = -b / (2*a)
            raizes = [(x, 0)]
        else:
            raizes = []

        return self.pontos_xy, self.menor_p, self.intercept_y, raizes

    def buscar_melhor_ponto_origem(self, iter_max=100000, erro_aceitavel=1e-3, funcao_segundo_grau=False):
        populacao = []
        intervalo_inicial = 10.0
        intervalo = intervalo_inicial
        iteracoes_realizadas = 0
        fator_reducao_intervalo = 0.97
        sem_melhoria = 0
        max_sem_melhoria = 5000 

        for _ in range(10):
            x = random.uniform(-intervalo, intervalo)
            y = (self.a * x**2 + self.b * x + self.c) if funcao_segundo_grau else (self.a * x + self.b)
            populacao.append((x, y))

        melhor_ponto = min(populacao, key=lambda p: math.hypot(p[0], p[1]))
        trajetoria = [melhor_ponto]

        while iteracoes_realizadas < iter_max:
            iteracoes_realizadas += 1
            nova_populacao = []

            for _ in range(9):
                x = random.uniform(melhor_ponto[0] - intervalo, melhor_ponto[0] + intervalo)
                y = (self.a * x**2 + self.b * x + self.c) if funcao_segundo_grau else (self.a * x + self.b)
                nova_populacao.append((x, y))

            nova_populacao.append(melhor_ponto)

            populacao = [
                novo if math.hypot(novo[0], novo[1]) < math.hypot(antigo[0], antigo[1]) else antigo
                for antigo, novo in zip(populacao, nova_populacao)
            ]

            novo_melhor = min(populacao, key=lambda p: math.hypot(p[0], p[1]))

            if math.hypot(novo_melhor[0], novo_melhor[1]) < math.hypot(melhor_ponto[0], melhor_ponto[1]):
                melhor_ponto = novo_melhor
                intervalo = max(intervalo * fator_reducao_intervalo, 1e-5)
                melhor_iter = iteracoes_realizadas
                sem_melhoria = 0
                trajetoria.append(melhor_ponto)
            else:
                sem_melhoria += 1

            if sem_melhoria >= max_sem_melhoria:
                print(f"Parando por estagnação após {sem_melhoria} iterações.")
                break

            if iteracoes_realizadas % 1000 == 0:
                dist = math.hypot(melhor_ponto[0], melhor_ponto[1])
                print(f"Iteração {iteracoes_realizadas}: Melhor ponto = {melhor_ponto}, distância = {dist:.6f}", flush=True)

            if math.hypot(melhor_ponto[0], melhor_ponto[1]) <= erro_aceitavel:
                print(f"Critério de erro atingido na iteração {iteracoes_realizadas}", flush=True)
                break

        print(f"Melhor ponto encontrado na iteração {melhor_iter}")
        print(f"Total de iterações realizadas: {iteracoes_realizadas}", flush=True)
        return melhor_ponto, iteracoes_realizadas, trajetoria


class Calcular_Funcao(Gerar_Pontos):
    def __init__(self):
        super().__init__()
        self.pontos_xy = []

    def calcular(self, escolha):
        if escolha == 1:
            tipo = 1
            print("Você escolheu a função do 1º grau, que tem forma: y = ax + b")
            try:
                a = int(input("Digite o valor de a: "))
                if a == 0:
                    print("O valor de 'a' não pode ser zero para uma função do 1º grau.")
                    return
                b = int(input("Digite o valor de b: "))

                pontos, intercept_y, menor_p = self.gerar_pts_1_grau(a, b)

                print(f"Função gerada: y = {a}x + {b}")
                print(f"Menor ponto otimizado: {menor_p}")

                plotar_gráfico(pontos, menor_p, intercept_y, None, tipo, self.trajetoria)

            except ValueError:
                print("Entrada inválida. Digite apenas números inteiros.")

        elif escolha == 2:
            tipo = 2
            print("Você escolheu a função do 2° grau, que tem forma: y = ax² + bx + c")
            try:
                a = int(input("Digite o valor de a: "))
                if a == 0:
                    print("O valor de 'a' não pode ser zero para uma função do 2º grau.")
                    return
                b = int(input("Digite o valor de b: "))
                c = int(input("Digite o valor de c: "))

                pontos, menor_p, intercept_y, raizes = self.gerar_pts_2_grau(a, b, c)

                print(f"Função gerada: y = {a}x² + {b}x + {c}")
                print(f"Vértice ajustado (mínimo ou máximo): {menor_p}")

                plotar_gráfico(pontos, menor_p, intercept_y, raizes, tipo, self.trajetoria)

            except ValueError:
                print("Entrada inválida. Digite apenas números inteiros.")
        else:
            print("Escolha inválida.")


def lista_nao_vazia_e_com_tuplas(lista):
    return isinstance(lista, list) and len(lista) > 0 and isinstance(lista[0], tuple)


def plotar_gráfico(pontos, menor_p, intercept_y, raizes, tipo, trajetoria=None):
    import matplotlib.pyplot as plt

    # ---------- Gráfico 1: Pontos e ponto mais próximo ----------
    fig1, ax1 = plt.subplots()
    x, y = zip(*pontos)

    if tipo == 1:
        ax1.plot(x, y, marker='o', linestyle='None', color='b', label='Função do 1° Grau')
    elif tipo == 2:
        ax1.plot(x, y, marker='o', linestyle='None', color='m', label="Função 2º grau")

    if raizes is not None and lista_nao_vazia_e_com_tuplas(raizes):
        for i, raiz in enumerate(raizes):
            ax1.plot(raiz[0], raiz[1], marker='o', color='y', linestyle='None',
                     label=f"Raiz {i+1} ({raiz[0]:.2f}, {raiz[1]:.2f})")

    ax1.plot(menor_p[0], menor_p[1], marker='o', color='c', linestyle='None',
             label=f"Menor ponto ({menor_p[0]:.2f}, {menor_p[1]:.2f})")

    ax1.plot(intercept_y[0], intercept_y[1], marker='o', color='k', linestyle='None',
             label=f"Intercepto em y ({intercept_y[0]}, {intercept_y[1]})")

    ax1.spines['left'].set_position('zero')
    ax1.spines['bottom'].set_position('zero')
    ax1.spines['right'].set_color('none')
    ax1.spines['top'].set_color('none')

    ax1.set_xlabel('x', labelpad=15)
    ax1.set_ylabel('y', labelpad=15, rotation=0)
    ax1.xaxis.set_label_coords(0.97, 0.48)
    ax1.yaxis.set_label_coords(0.48, 0.97)

    ax1.set_title("Gráfico dos Pontos Gerados")
    ax1.legend()
    ax1.grid(True)

    # ---------- Gráfico 2: Trajetória de Otimização ----------
    if trajetoria:
        fig2, ax2 = plt.subplots()
        x_traj, y_traj = zip(*trajetoria)
        ax2.plot(x_traj, y_traj, linestyle='--', color='orange', linewidth=2, marker='x',
                label="Trajetória de otimização")

        ax2.plot(0, 0, marker='o', color='gray', label="Origem (0,0)")
        ax2.plot(menor_p[0], menor_p[1], marker='o', color='c',
                label=f"Melhor ponto final ({menor_p[0]:.2f}, {menor_p[1]:.2f})")

        ax2.spines['left'].set_position('zero')
        ax2.spines['bottom'].set_position('zero')
        ax2.spines['right'].set_color('none')
        ax2.spines['top'].set_color('none')

        ax2.set_xlabel('x', labelpad=15)
        ax2.set_ylabel('y', labelpad=15, rotation=0)
        ax2.xaxis.set_label_coords(0.97, 0.48)
        ax2.yaxis.set_label_coords(0.48, 0.97)

        ax2.set_title("Trajetória da Otimização")
        ax2.legend()
        ax2.grid(True)

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
            else:
                print("Opção Inválida")
        except ValueError:
            print("Digite um número inteiro válido.")
