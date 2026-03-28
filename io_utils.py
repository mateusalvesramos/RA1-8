from typing import List, Tuple

def lerArquivo(nome_arquivo_entrada: str):
    try:
        with open(nome_arquivo_entrada, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"Erro: arquivo '{nome_arquivo_entrada}' não encontrado.")
        return None
    except OSError as e:
        print(f"Erro ao abrir '{nome_arquivo_entrada}': {e}")
        return None
    
def salvarTokens(vetores_tokens: List[List[Tuple[str, str]]], nome_arquivo_saida: str):
    try:
        with open(nome_arquivo_saida, "w", encoding="utf-8") as file:
            for i, vetor in enumerate(vetores_tokens, start=1):
                serializado = " ".join(f"{tipo}:{valor}" for tipo, valor in vetor)
                file.write(f"linha_{i}: {serializado}\n")
        return True
    except OSError as e:
        print(f"Erro ao salvar tokens em '{nome_arquivo_saida}': {e}")
        return False
    
def salvarAssembly(codigo_assembly: str, nome_arquivo_saida: str):
    try:
        with open(nome_arquivo_saida, "w", encoding="utf-8") as file:
            file.write(codigo_assembly)
        return True
    except OSError as e:
        print(f"Erro ao salvar Assembly em '{nome_arquivo_saida}': {e}")
        return False