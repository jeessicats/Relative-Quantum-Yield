linha = '=' * 100
titulo = "Rendimento Relativo"
nome = "Jéssica Teixeira dos Santos"

print(linha)
print(titulo.center(100))
print(linha)

print(nome.rjust(100))

# Basic Imports
import matplotlib.pyplot as plt
import numpy as np
import os

# Definitions
def file_select():
    path_all = os.listdir()
    path_use = []

    for i in range(len(path_all)):
        if (path_all[i].endswith('.txt')):
            path_use.append(path_all[i])

    print("Você tem os seguintes arquivos:")

    for i in range(len(path_use)):
        print(path_use[i])

    lock = 0    #medida de seguranção --> quando ele achar o arquivo lock == 1 sai do def e retorna o arquivo escolhido aberto

    while True:
        choice = input("Escolha um arquivo para abrir, ou digite 'exit' para sair:\n")

        for i in range(len(path_use)):
            if path_use[i] == choice:
                lock = 1
                break

        if (lock == 1):
            break
        elif choice == "exit":
            print("Você saiu do programa!")
            exit()
        else:
            print("Arquivo inválido!")

    return open(choice)

def acquire_array(file, eixo):
    if (eixo.lower() == 'x'):                       #medida de segurança pra prevenir erros no codigo
        e = 0
    elif (eixo.lower() == 'y'):
        e = 1

    list_output = []                #guarda uma lista, ou x ou y, depende de qual foi dito quando a função foi chamada
    file.seek(0)

    for linha in file:
        valores = linha.split()
        list_output.append(valores[e])

    list_output = [float(i) for i in list_output]      #garrantir que todos os valores são float

    return np.asarray(list_output)

def draw_graph(x, y, y_string):
    plt.xlabel("Comprimento de onda (nm)", fontsize=12)
    plt.ylabel(y_string, fontsize=12)
    plt.plot(x, y, color="blue")
    return plt.show()

def find_closest(array, target):      #np --> biblioteca as --> função
    index = (np.abs(array - target)).argmin()     #index --> posição no array onde está o valor que eu quero #np.abs transforma todos os valores em valores absolutos #.argmin() função da biblioteca arg que devolve o menos valor do meu array
    return index

def integrate(x, y):
    print('\nSeu grafico possui', len(x) - 1, 'valores que variam de ', x[0], 'nm até', x[len(x) - 1], 'nm')
    print('Gostaria de calcular a integral entre quais dos valores?')
    v_i = float(input("Valor Incial (em nm) = "))
    v_f = float(input("Valor Final (em nm) = "))

    v_i = find_closest(x, v_i)

    v_f = find_closest(x, v_f)

    area = 0.0

    while (v_i < v_f):
        if (y[v_i] > y[v_i + 1]):
            b_y = y[v_i]
            s_y = y[v_i + 1]
        else:
            s_y = y[v_i]
            b_y = y[v_i + 1]

        area = area + (((b_y - s_y) * (x[v_i + 1] - x[v_i])) / 2)
        area = area + (s_y) * (x[v_i + 1] - x[v_i])
        v_i = v_i + 1

    return area

def abs_value(x, y):
    print('\nSeu grafico possui', len(x) - 1, 'valores que variam de ', x[0], 'nm até', x[len(x) - 1], 'nm')
    valor = int(input("Para qual valor de comprimento de onda (nm) você gostaria de saber a Absorbância = "))

    valor = find_closest(x, valor)

    return y[valor]

def Rendimento_Relativo(I_A,I_R,A_R,A_A):
    fi = float(input("Digite o valor de rendimento para o seu padrão:\n"))
    n_a = float(input("Digite o valor de índice de refração do solvente utilizado nas análises das amostras:\n"))
    n_r = float(input("Digite o valor de índice de refração do solvente utilizado nas análises do seu padrão:\n"))
    area = I_A/I_R
    absorbance = A_R/A_A
    n = (n_a/n_r)**2
    q_yield = fi*area*absorbance*n
    return round(q_yield,2)

def call_function(function):
    f = file_select()
    x = acquire_array(f, 'x')
    y = acquire_array(f, 'y')
    if (function.lower() == 'integrate'):
        result = integrate(x, y)
    elif (function.lower() == 'abs'):
        result = abs_value(x, y)
    f.close()
    return result

def output (I_A,I_R,A_R,A_A,q_yield):
    file_name = str(input("Digite um nome para o seu arquivo de output:\n"))
    output = open(file_name+".txt","w")
    output.write("Dados do cálculo de Rendimento Relativo:\n\n")
    output.write("Integral da area sob a curva de emissão da sua amostra:\n") + output.write(str(I_A))
    output.write("\n\nIntegral da area sob a curva de emissão do seu padrão:\n") + output.write(str(I_R))
    output.write("\n\nAbosrobância do seu padrão no comprimento de onda de excitação:\n") + output.write(str(A_R))
    output.write("\n\nAbosrobância do seu padrão no comprimento de onda de excitação:\n") + output.write(str(A_A))
    output.write("\n\nO rendimento relativo calculado para sua amostra é de:\n") + output.write(str(q_yield))

# Start of the program
samples = [0., 0., 0., 0.] #0=I_A, 1=I_R, 2=A_A, 3=A_R

while True:
    try:
        option = int(input("1. Calcular o Rendimento Relativo\n2. Plotar um gráfico\n3. Sair\n"))
        if option == 1:
            print("\nEscolha um arquivo para calcular a integral do gráfico de emissão para sua amostra:")
            samples[0] = call_function('integrate')

            print("\nEscolha um arquivo para calcular a integral do gráfico de emissão para sua referência:")
            samples[1] = call_function('integrate')

            print("\nEscolha um arquivo para pegar um valor de absorbância para o comprimento de onda de excitassão da referência:")
            samples[2] = call_function('abs')

            print("\nEscolha um arquivo para pegar um valor de absorbância para o comprimento de onda de excitassão da amostra:")
            samples[3] = call_function('abs')

            if (samples[0] > 0 and samples[1] > 0 and samples[2] > 0 and samples[3] > 0):
                rendimento = Rendimento_Relativo(samples[0], samples[1], samples[2], samples[3])
                print("O rendimento relativo calculado é",rendimento,"\n")
                output(samples[0], samples[1], samples[2], samples[3], rendimento)

        elif option == 2:
            f = file_select()
            x = acquire_array(f , 'x')
            y = acquire_array(f , 'y')
            y_string = str(input("Digite um título para o eixo y:\n"))
            draw_graph(x, y, y_string)
        elif option == 3:
            print("Você saiu do programa!")
            break
        else:
            print("Este não é um valor válido")
    except ValueError:
        print("Este não é um valor válido!\n")