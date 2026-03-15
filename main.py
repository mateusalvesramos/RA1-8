# Estados
def estado_inicial(linha, i, token, vetor_tokens):
    # Chegou ao fim da linha, não vai para nenhum estado
    if i >= len(linha):
        return None, i, ""
    
    token = linha[i]

    if token.isspace():
        return estado_inicial, i+1, ""
    
    # Estado de aceitação para os operadores e parênteses
    elif token in "()+-*%^":
        vetor_tokens.append(token)
        return estado_inicial, i+1, ""
    
    # Verificação de divisão real e divisão inteira
    elif token == "/":
        return estado_barra, i+1, ""

    # Verificação de indentificador MEM ou RES
    elif token.isalpha() and token.isupper():
        return estado_identificador, i, ""
    
    # Verificação de números: inteiros ou decimais
    elif token.isdigit():
        return estado_numero, i, ""
    
    else:
        raise ValueError(f"Erro léxico: caractere inválido '{token}' na posição {i}")

def estado_identificador(linha, i, token, vetor_tokens):
    # Equanto houve letra maiúscula e a linha ainda não estiver no fim...
    while i < len(linha) and (linha[i].isalpha() and linha[i].isupper()):
        token += linha[i]
        i += 1
    
    vetor_tokens.append(token)
    
    # Posteriormente implementar verificardor MEM ou RES, para alocar com tuplas as informações em vetor_tokens
    
    return estado_inicial, i, ""

def estado_numero(linha, i, token, vetor_tokens):
    while i < len(linha) and (linha[i].isdigit()):
        token += linha[i]
        i += 1

    if i < len(linha) and linha[i] == ".":
        return estado_ponto, i, token

    vetor_tokens.append(token)
    return estado_inicial, i, ""

def estado_ponto(linha, i, token, vetor_tokens):
    if i >= len(linha):
        return None, i, ""

    if i+1 < len(linha) and linha[i+1].isdigit():
        i+=1
        token += "."
        # Enquanto a linha não tiver acabado e for um digito (número)
        while i < len(linha) and linha[i].isdigit():
            token += linha[i]
            i += 1
    
        vetor_tokens.append(token)

    return estado_inicial, i, ""

def estado_barra(linha, i, token, vetor_tokens):
    # Quando passado, o i já foi incrementado 1...
    if i < len(linha) and linha[i] == "/": # Caso seja divisão inteira...
        token += "//"
        vetor_tokens.append(token)
        return estado_inicial, i + 1, ""
    
    token = "/"
    vetor_tokens.append(token)
    return estado_inicial, i, ""


def parseExpressao(linha: str): # Realizar a conversão dos tokens que forem inteiros ou reais para float
    # Funções como estados do autômato finito determinístico (AFD)

    # Usando AFD ler linhas, validar (identificar casos de erro léxico)
    # e extrair tokens: números reais, operadores, comandos especiais e parênteses

    # Contruir funções de teste

    # return vetor de tokens

    vetor_tokens = []
    i = 0
    token = ""
    estado = estado_inicial

    while estado is not None:
        estado, i, token = estado(linha, i, token, vetor_tokens)
    
    return vetor_tokens

# def executarExpressao(vetor_tokens: list[str], memoria: dict, resultados: list[float]):
    # Usar pilha para avaliar expressoes RPN
    # Memória MEM e histórico de resultados em RES
    # Analisa e aplica operadores + - * / // % ^
    # Precisão de 64 bits com floar em Python
    # return resultado da expressão atual

# def gerarAssembly(vetor_tokens:list[str]):
    # Criar funções de teste
    # Contemplar operações, comandos especiais e expressões aninhadas
    # return código em assembly ARMv7 a partir da lista de tokens

# def exibirResultados(resultados: list[float]):
    # Imprime os resultados

# def lerArquivo(nome_arquivo_entrada: str):
    # Criar funções de teste
    # Verificar erros na abertura de arquivo e axibir mensagens claras
    # Return linhas (para o parseExpressao)

# def salvarTokens(vetor_tokens: list[str], nome_arquivo_saida: str):
    # Salvar em .txtou json os tokens da última execução

# def main():
    # Configurar a possibilidade de passar os arquivos txt por linha de comando
    # Organizar e juntar as outras funções

# if __name__ == "__main__":
    # main()

# Funções de teste (exemplos):
# def testar_parseExpressao():
    # print(parseExpressao("3.14 2.0 +"))
    # print(parseExpressao("( 5 RES )"))

# def testar_executarExpressao():
#     memoria = {}
#     historico = []
#     print(executarExpressao(["3.0", "2.0", "+"], memoria, historico))

print(parseExpressao("((A B *) (D E *) /)"))