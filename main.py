def parseExpressao(linha: str):
    # Funções como estados do autômato finito determinístico (AFD)

    # Usando AFD ler linhas, validar (identificar casos de erro léxico)
    # e extrair tokens: números reais, operadores, comandos especiais e parênteses

    # Contruir funções de teste

    # return vetor de tokens

def executarExpressao(vetor_tokens: list[str], memoria: dict, resultados: list[float]):
    # Usar pilha para avaliar expressoes RPN
    # Memória MEM e histórico de resultados em RES
    # Analisa e aplica operadores + - * / // % ^
    # Precisão de 64 bits com floar em Python
    # return resultado da expressão atual

def gerarAssembly(vetor_tokens:list[str]):
    # Criar funções de teste
    # Contemplar operações, comandos especiais e expressões aninhadas
    # return código em assembly ARMv7 a partir da lista de tokens

def exibirResultados(resultados: list[float]):
    # Imprime os resultados

def lerArquivo(nome_arquivo_entrada: str):
    # Criar funções de teste
    # Verificar erros na abertura de arquivo e axibir mensagens claras
    # Return linhas (para o parseExpressao)

def salvarTokens(vetor_tokens: list[str], nome_arquivo_saida: str):
    # Salvar em .txtou json os tokens da última execução

def main():
    # Configurar a possibilidade de passar os arquivos txt por linha de comando
    # Organizar e juntar as outras funções

if __name__ == "__main__":
    main()

# Funções de teste (exemplos):
# def testar_parseExpressao():
    # print(parseExpressao("3.14 2.0 +"))
    # print(parseExpressao("( 5 RES )"))

# def testar_executarExpressao():
#     memoria = {}
#     historico = []
#     print(executarExpressao(["3.0", "2.0", "+"], memoria, historico))