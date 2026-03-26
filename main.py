import sys

# Exceção
class ErroLexico(Exception):
    def __init__(self, mensagem, token, i):
        self.token = token
        self.posicao = i
        super().__init__(mensagem)
    
    def __str__(self):
        return f"Erro léxico na posição {self.posicao}: {self.args[0]} -> '{self.token}'"

# Funções auxiliares
def eh_limite(linha, i):
    """Verifica se o caractere está antes de um limite (espaço, parenteses, tabulação ou fim da linha)"""
    return i >= len(linha) or linha[i] in ' \t()\n'

def valida_parenteses(vetor_tokens, saldo_parenteses):
    """Valida o fechamento de parênteses de acordo com a saída do analisador léxico"""
    
    # Captura o tipo do últim token adicionado ao vetor
    tipo_token = vetor_tokens[-1][0]

    if tipo_token == "LPAREN":
        saldo_parenteses += 1
    elif tipo_token == "RPAREN":
        saldo_parenteses -= 1
        if saldo_parenteses < 0:
            raise ErroLexico("parêntese de fechamento sem abertura", ")", "")
        
    return saldo_parenteses

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
        if token == "(":    
            vetor_tokens.append(("LPAREN", token))
        elif token == ")":
            vetor_tokens.append(("RPAREN", token))
        elif token == "+":
            vetor_tokens.append(("OP_ADD", token))
        elif token == "-":
            vetor_tokens.append(("OP_SUB", token))
        elif token == "*":
            vetor_tokens.append(("OP_MUL", token))
        elif token == "%":
            vetor_tokens.append(("OP_MOD", token))
        elif token == "^":
            vetor_tokens.append(("OP_POW", token))
        return estado_inicial, i+1, ""
    
    # Verificação de divisão real e divisão inteira
    elif token == "/":
        return estado_barra, i+1, "/"

    # Verificação de indentificador MEM ou RES
    elif token.isalpha() and token.isupper():
        return estado_identificador, i, ""
    
    # Verificação de números: inteiros ou decimais
    elif token.isdigit():
        return estado_numero, i, ""
    
    else:
        raise ErroLexico("caractere inválido", token, i) from None

def estado_identificador(linha, i, token, vetor_tokens):
    # Equanto houve letra maiúscula e a linha ainda não estiver no fim...
    while i < len(linha) and (linha[i].isalpha() and linha[i].isupper()):
        token += linha[i]
        i += 1

    if eh_limite(linha, i):
        if token == "RES":
            vetor_tokens.append(("KW_RES", token))
            return estado_inicial, i, ""
        
        else:
            vetor_tokens.append(("ID", token))
            return estado_inicial, i, ""
    
    raise ErroLexico("identificador deve conter apenas letras maiúsculas", token, i) from None

def estado_numero(linha, i, token, vetor_tokens):
    while i < len(linha) and (linha[i].isdigit()):
        token += linha[i]
        i += 1
    
    if i < len(linha) and linha[i] == ".":
        return estado_ponto, i, token
    
    if eh_limite(linha, i):
        vetor_tokens.append(("NUM", token))
        return estado_inicial, i, ""
    
    if linha[i] == ",":
        raise ErroLexico("separador decimal inválido (vírgula)", token, i) from None
    
    raise ErroLexico("número seguido de caractere inválido", token, i) from None

def estado_ponto(linha, i, token, vetor_tokens):
    if i >= len(linha):
        return None, i, ""

    # Verificando o caractere seguido do ponto
    if i+1 < len(linha) and linha[i+1].isdigit():
        i+=1
        token += "."
        # Enquanto a linha não tiver acabado e for um digito (número)
        while i < len(linha) and linha[i].isdigit():
            token += linha[i]
            i += 1

        if eh_limite(linha, i):
            vetor_tokens.append(("NUM", token))
            return estado_inicial, i, ""
        
        raise ErroLexico("número real malformado", token, i) from None

def estado_barra(linha, i, token, vetor_tokens):
    # Quando passado, o i já foi incrementado 1...
    if i < len(linha) and linha[i] == "/": # Caso seja divisão inteira ("//")...
        token += "/"
        # Caso haja um caractere após a barra que não seja " ", "\n", "\t" ou ")"...
        if not eh_limite(linha, i+1):
            token += linha[i+1]
            raise ErroLexico("Operador '//' seguido de caractere inválido.", token, i) from None
        vetor_tokens.append(("OP_DIV_INT", token))
        return estado_inicial, i + 1, ""
    
    # Caso haja um caractere após a barra que não seja " ", "\n", "\t" ou ")"...
    if not eh_limite(linha, i):
            # Atribuindo o caractere inválido para ser mostrado na mensagem de erro
            token += linha[i+1]
            raise ErroLexico("Operador '/' seguido de caractere inválido.", token, i) from None
    vetor_tokens.append(("OP_DIV", token))
    return estado_inicial, i, ""

def parseExpressao(linha: str):
    vetor_tokens = []
    i = 0
    token = ""
    estado = estado_inicial
    saldo_parenteses = 0 # Variável para verificação do balanceamento dos parênteses

    while estado is not None:
        tamanho_antes = len(vetor_tokens)

        # Aqui ocorre a mudança de estados, sendo o retorno do estado atual aplicado como "argumento" para o próximo estado
        estado, i, token = estado(linha, i, token, vetor_tokens)

        # Verifica se houve adição de novos tokens no vetor de tokens (evita processamento desnecessário)
        if len(vetor_tokens) > tamanho_antes:
            saldo_parenteses = valida_parenteses(vetor_tokens, saldo_parenteses)

    if saldo_parenteses > 0:
        raise ErroLexico("parênteses desbalanceados", "(", i)
    
    return vetor_tokens

# def executarExpressao(vetor_tokens: list[str], memoria: dict, resultados: list[float]):
    # Usar pilha para avaliar expressoes RPN
    # Memória MEM e histórico de resultados em RES
    # Analisa e aplica operadores + - * / // % ^
    # Precisão de 64 bits com float em Python
    # return resultado da expressão atual

# def gerarAssembly(vetor_tokens:list[str]):
    # Criar funções de teste
    # Contemplar operações, comandos especiais e expressões aninhadas
    # return código em assembly ARMv7 a partir da lista de tokens

# def exibirResultados(resultados: list[float]):
    # Imprime os resultados

def lerArquivo(nome_arquivo_entrada: str):
    # Criar funções de teste
    # Verificar erros na abertura de arquivo e exibir mensagens claras
    # Return linhas (para o parseExpressao)
    try:
        with open(nome_arquivo_entrada, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"Erro: arquivo '{nome_arquivo_entrada}' não encontrado.")
        return None
    except OSError as e:
        print(f"Erro ao abrir '{nome_arquivo_entrada}': {e}")
        return None

# def salvarTokens(vetor_tokens: list[str], nome_arquivo_saida: str):
    # Salvar em .txtou json os tokens da última execução

def main():
    # Configurar a possibilidade de passar os arquivos txt por linha de comando
    # Organizar e juntar as outras funções

    if len(sys.argv) != 2:
        print("Erro!\nForma correta de executar: python main.py <arquivo.txt>")
        return
    
    nome_arquivo = sys.argv[1]
    linhas = lerArquivo(nome_arquivo)
    if linhas is None:
        return
    
    for linha in linhas:
        try:
            tokens = parseExpressao(linha)
            print(f"\nOK | {linha} -> {tokens}")
        except ErroLexico as e:
            print(f"\nERRO | {linha} -> {e}")

if __name__ == "__main__":
    main()