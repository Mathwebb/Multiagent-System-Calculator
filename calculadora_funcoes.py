import math

def resolveEquacao(equacao):

    #Remove os espaçoes entre os caracteres e divide todos os caracteres da equação em uma lista
    equacao = equacao.split(" ")
    #equacao = list(equacao)

    while (len(equacao) != 1): #Repete até ter 1 elemento na equação(que seria o resultado final)
        print("Equacao")
        print(equacao)

        f = achaOperacao(equacao)
        maiorOperacao = f[0]
        x = int(f[1])

        if (maiorOperacao == "("):
            interiorParenteses = ""
            matchIndex = matchParentese(equacao)
            for a in range(x + 1, matchIndex): #Vai da primeira posição após o parenteses até a posição do primeiro ) encontrado
                interiorParenteses = interiorParenteses + " " + equacao[x + 1] if len(interiorParenteses) else interiorParenteses + equacao[x + 1] #Refazer a equacao no interior do parenteses
                equacao.pop(x + 1) #Tirar os elementos do interior do parenteses da equacao principal
            equacao.pop(x + 1) #Tirar o ) que sobrou
            equacao[x] = resolveEquacao(interiorParenteses) #Resolver a equacao do parenteses
        else:
            operandos = achaOperandos(equacao, maiorOperacao)
            if (maiorOperacao != "#"):
                num1 = float(operandos[0]) #Porque a operação de raiz quadrada só recebe 1 elemento(e ele normalmente não fica antes da operação raiz)
                num2 = float(operandos[1])
            else:
                num2 = float(operandos[1])

            #Em cada um deles quando ele resolve a operação ele insere ela na posição do primeiro caractere do primeiro operando
            if (maiorOperacao == "^"):
                equacao[x - operandos[2]] = resolvePotencia(num1, num2)
            elif (maiorOperacao == "#"):
                equacao[x - operandos[2]] = resolveRaiz(num2)
            elif (maiorOperacao == "*"):
                equacao[x - operandos[2]] = resolveMultiplicacao(num1, num2)
            elif (maiorOperacao == "/"):
                equacao[x - operandos[2]] = resolveDivisao(num1, num2)
            elif (maiorOperacao == "+"):
                equacao[x - operandos[2]] = resolveAdicao(num1, num2)
            elif (maiorOperacao == "-" or maiorOperacao == "–"):
                equacao[x - operandos[2]] = resolveSubtracao(num1, num2)

            #Depois elimina os valores que vão desde o segundo caractere do primero operando até o ultimo caractere do segundo operando
            for g in range(x - operandos[2] + 1, x + operandos[3] + 1):
                equacao.pop(x - operandos[2] + 1)

        #Se tiver apenas 1 elemento na lista é porque ele é o resultado
        if (len(equacao) == 1):
            print(equacao[0])
            return equacao[0]

#Acha o operando de maior prioridade da equação percorrendo ela e comparando a prioridade entre os operadores
def achaOperacao(equacao):
    operacoes = ["=", "-", "+", "/", "*", "#", "^", "("] #OBS: O '=' serve como maiorOperacao inicial e para indicar que não existem mais operandos na lista
    maiorOperacao = ["=", ""] #A primera posição vai receber caratere do maior operador da equação e a segunda recebe a posição dele
    for i in range(len(equacao)):
        if (equacao[i] in operacoes): #Verifica se o elemento atual é um operador
            # Verifica se a prioridade(posição na lista de operadores) da maiorOperação for menor do que do que a prioridade do operador da posição atual
            if (operacoes.index(maiorOperacao[0]) < operacoes.index(equacao[i])):
                maiorOperacao[0] = equacao[i]
    maiorOperacao[1] = equacao.index(maiorOperacao[0]) #Guarda a posição do maiorOperador encontrado
    return maiorOperacao

def achaOperandos(equacao, maiorOperacao):
    operacoes = ["=", "-", "+", "/", "*", "#", "^"]
    operandos = ["", "", 0, 0]
    for i in range(len(equacao)):
        if (equacao[i] == maiorOperacao):
            # Ele percorre a lista a partir do primeiro elemento antes da posição da maiorOperação
            # até chegar no primero caractere da equação
            for a in range(i - 1, -1, -1):
                if (equacao[a] in operacoes): #Mas se ele encontrar outro operador então a iteração é interrompida
                    break
                #Enquanto a iteração não é interrompida o primeiro operando da opeação vai sendo refeito
                #e colocado na lista operandos a partir do ultimo caractere até o primeiro dele
                operandos[0] = str(equacao[a]) + operandos[0]
                operandos[2] += 1

            # Ele percorre a lista a partir do primeiro elemento depois da posição da maiorOperação
            # até chegar no último caractere da equação
            for b in range(i + 1, len(equacao)):
                if (equacao[b] in operacoes):#Mas se ele encontrar outro operador então a iteração é interrompida e os operandos são retornados
                    return operandos
                # Enquanto a iteração não é interrompida o segundo operando da opeação vai sendo refeito
                # e colocado na lista operandos a partir do primeiro caractere até o último dele
                operandos[1] = operandos[1] + str(equacao[b])
                operandos[3] += 1
                # E se a posição atual +1 é igual ao tamanho da equação, ou seja, chegou no último caractere da equação então
                # a iteração é interrompida e os operandos são retornados
                if (b + 1 == len(equacao)):
                    return operandos

#Funções para resolver as operações
def resolvePotencia(num1, num2):
    return str(num1 ** num2)


def resolveRaiz(num1):
    return str(math.sqrt(num1))


def resolveMultiplicacao(num1, num2):
    return str(num1 * num2)


def resolveDivisao(num1, num2):
    return str(num1 / num2)


def resolveAdicao(num1, num2):
    return str(num1 + num2)


def resolveSubtracao(num1, num2):
    return str(num1 - num2)

def matchParentese(equacao):
    for i in range (len(equacao)-1, -1, -1):
        if (equacao[i] == ")"):
            return i


print(resolveEquacao("23 + 12 - 55 + ( 2 + 4 ) - 8 / 2 ^ 2"))

# print(resolveEquacao("10 * ( 9 / ( 2 + 1 ) )"))
