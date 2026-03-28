# Integrantes: Mateus Alves Ramos (GitHub: mateusalvesramos)
# Grupo: RA1 8

from lexico import parseExpressao, ErroLexico
from gerador import executarExpressao, gerarAssembly, ErroGeracaoAssembly
from io_utils import lerArquivo, salvarTokens, salvarAssembly
from testes import testarAnalisadorLexico
from typing import List, Tuple

import sys

def main():
    # Configurar a possibilidade de passar os arquivos txt por linha de comando
    # Organizar e juntar as outras funções

    if len(sys.argv) != 2:
        print("Erro!\nForma correta de executar: python main.py <arquivo.txt>")
        return
    
    nome_arquivo = sys.argv[1]
    if nome_arquivo == "--testes":
        testarAnalisadorLexico()
        return

    linhas = lerArquivo(nome_arquivo)
    if linhas is None:
        return

    vetores_tokens: List[List[Tuple[str, str]]] = []
    blocos: List[Tuple] = []
    memoria_catalogo: dict = {}
    resultados_exibicao: List[float] = []
    houve_erro = False

    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue

        try:
            tokens = parseExpressao(linha)
            bloco = executarExpressao(tokens, memoria_catalogo, blocos)
            vetores_tokens.append(tokens)
            resultados_exibicao.append(0.0)
            print(f"\nOK | {linha} -> {tokens}")
            print(f"BLOCO | {bloco}")
        except (ErroLexico, ErroGeracaoAssembly) as e:
            houve_erro = True
            print(f"\nERRO | {linha} -> {e}")

    if houve_erro:
        print("\nGeração interrompida: corrija os erros léxicos antes de gerar tokens/Assembly.")
        return

    if not vetores_tokens:
        print("\nNenhuma expressão válida encontrada no arquivo.")
        return

    try:
        codigo_assembly = gerarAssembly(vetores_tokens)
    except ErroGeracaoAssembly as e:
        print(f"\nErro na geração de Assembly: {e}")
        return

    if not salvarTokens(vetores_tokens, "tokens_ultima_execucao.txt"):
        return

    if not salvarAssembly(codigo_assembly, "ultimo_programa.s"):
        return

    print("\nTokens salvos em: tokens_ultima_execucao.txt")
    print("Assembly salvo em: ultimo_programa.s")
    print("Execute o arquivo Assembly no Cpulator ARMv7 DEC1-SOC(v16.1).")

if __name__ == "__main__":
    main()