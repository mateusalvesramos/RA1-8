# Integrantes: Mateus Alves Ramos (GitHub: mateusalvesramos)
# Grupo: RA1 8

from lexico import parseExpressao, ErroLexico
from gerador import executarExpressao, gerarAssembly, ErroGeracaoAssembly
from io_utils import lerArquivo, salvarTokens, salvarAssembly
from typing import List, Tuple

import sys

def exibirResultados(registros):
    for registro in registros:
        status = registro["status"]
        linha = registro["linha"]

        if status == "ok":
            print(f"\nOK | {linha} -> {registro['tokens']}")
            print(f"BLOCO | {registro['bloco']}")
        else:
            print(f"\nERRO | {linha} -> {registro['erro']}")

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

    vetores_tokens: List[List[Tuple[str, str]]] = []
    blocos: List[Tuple] = []
    memoria_catalogo: dict = {}
    registros_processamento = []
    houve_erro = False

    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue

        try:
            tokens = parseExpressao(linha)
            bloco = executarExpressao(tokens, memoria_catalogo, blocos)
            vetores_tokens.append(tokens)
            registros_processamento.append({
                "status": "ok",
                "linha": linha,
                "tokens": tokens,
                "bloco": bloco,
            })
        except (ErroLexico, ErroGeracaoAssembly) as e:
            houve_erro = True
            registros_processamento.append({
                "status": "erro",
                "linha": linha,
                "erro": str(e),
            })

    exibirResultados(registros_processamento)

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