# Integrantes: Mateus Alves Ramos (GitHub: mateusalvesramos)
# Grupo: RA1 8

import sys
from typing import List, Tuple

class ErroGeracaoAssembly(Exception):
    def __init__(self, mensagem, linha_idx=None):
        self.linha_idx = linha_idx
        super().__init__(mensagem)

    def __str__(self):
        if self.linha_idx is None:
            return self.args[0]
        return f"Erro de geração (linha {self.linha_idx + 1}): {self.args[0]}"
    
# --------------------
# Redução de blocos por pilha
# --------------------

def eh_inteiro_positivo_string(texto: str) -> bool:
    return texto.isdigit()


def item_para_bloco(item):
    tipo = item[0]
    if tipo in {"NUM", "MEM_GET", "MEM_SET", "RES_GET", "BIN"}:
        return item
    if tipo == "ID_ITEM":
        # Modo permissivo: ID isolado vira leitura de memória.
        return ("MEM_GET", item[1])
    raise ErroGeracaoAssembly(f"item inválido em expressão: {item}")


def reduz_bloco_parenteses(itens):
    if len(itens) == 1:
        unico = itens[0]
        if unico[0] == "ID_ITEM":
            return ("MEM_GET", unico[1])
        raise ErroGeracaoAssembly("forma '(X)' inválida: esperado identificador de memória")

    if len(itens) == 2:
        a, b = itens
        if b[0] == "KW_RES":
            if a[0] != "NUM" or not eh_inteiro_positivo_string(a[1]):
                raise ErroGeracaoAssembly("(N RES) exige N inteiro não negativo")
            return ("RES_GET", int(a[1]))
        if b[0] == "ID_ITEM":
            return ("MEM_SET", b[1], item_para_bloco(a))
        raise ErroGeracaoAssembly("forma de 2 elementos inválida; esperado (N RES) ou (V MEM)")

    if len(itens) == 3:
        esq, dir_, op = itens
        if op[0] != "OP_ITEM":
            raise ErroGeracaoAssembly("expressão binária deve terminar com operador")
        return ("BIN", op[1], item_para_bloco(esq), item_para_bloco(dir_))

    raise ErroGeracaoAssembly("expressão com aridade inválida dentro de parênteses")


def token_para_item(token):
    tipo, valor = token
    if tipo == "NUM":
        return ("NUM", valor)
    if tipo == "ID":
        return ("ID_ITEM", valor)
    if tipo == "KW_RES":
        return ("KW_RES", valor)
    if tipo.startswith("OP_"):
        return ("OP_ITEM", tipo)
    raise ErroGeracaoAssembly(f"token não suportado na redução: {token}")


def reduzirBlocos(vetor_tokens):
    pilha = []

    for token in vetor_tokens:
        tipo = token[0]

        if tipo == "LPAREN":
            pilha.append(("MARCADOR", "("))
            continue

        if tipo == "RPAREN":
            itens = []
            while pilha and pilha[-1][0] != "MARCADOR":
                itens.append(pilha.pop())

            if not pilha:
                raise ErroGeracaoAssembly("parêntese de fechamento sem abertura na redução")

            pilha.pop()  # remove marcador de abertura
            itens.reverse()
            pilha.append(reduz_bloco_parenteses(itens))
            continue

        pilha.append(token_para_item(token))

    if len(pilha) != 1:
        raise ErroGeracaoAssembly("expressão inválida após redução por pilha")

    return pilha[0]


def coletar_memorias(no, memorias: set):
    tipo = no[0]
    if tipo == "MEM_GET":
        memorias.add(no[1])
    elif tipo == "MEM_SET":
        memorias.add(no[1])
        coletar_memorias(no[2], memorias)
    elif tipo == "BIN":
        coletar_memorias(no[2], memorias)
        coletar_memorias(no[3], memorias)


def coletar_constantes(no, constantes: set):
    tipo = no[0]
    if tipo == "NUM":
        constantes.add(no[1])
    elif tipo == "MEM_SET":
        coletar_constantes(no[2], constantes)
    elif tipo == "BIN":
        coletar_constantes(no[2], constantes)
        coletar_constantes(no[3], constantes)


def safe_label(texto: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "_" for ch in texto)


def emit_carrega_d0(label: str, asm: List[str]):
    asm.append(f"    ldr r0, ={label}")
    asm.append("    vldr.f64 d0, [r0]")


def emit_expr(no, linha_idx: int, resultados_labels: List[str], asm: List[str], const_labels: dict, mem_labels: dict):
    tipo = no[0]

    if tipo == "NUM":
        emit_carrega_d0(const_labels[no[1]], asm)
        return

    if tipo == "MEM_GET":
        emit_carrega_d0(mem_labels[no[1]], asm)
        return

    if tipo == "RES_GET":
        desloc = no[1]
        idx_origem = linha_idx - desloc
        if idx_origem < 0:
            emit_carrega_d0(const_labels["0.0"], asm)
            return
        asm.append(f"    ldr r0, ={resultados_labels[idx_origem]}")
        asm.append("    vldr.f64 d0, [r0]")
        return

    if tipo == "MEM_SET":
        emit_expr(no[2], linha_idx, resultados_labels, asm, const_labels, mem_labels)
        asm.append(f"    ldr r0, ={mem_labels[no[1]]}")
        asm.append("    vstr.f64 d0, [r0]")
        return

    if tipo != "BIN":
        raise ErroGeracaoAssembly(f"nó inválido para emissão: {tipo}", linha_idx)

    op_tipo = no[1]
    esq = no[2]
    dir_ = no[3]

    emit_expr(esq, linha_idx, resultados_labels, asm, const_labels, mem_labels)
    asm.append("    vpush {d0}")
    emit_expr(dir_, linha_idx, resultados_labels, asm, const_labels, mem_labels)
    asm.append("    vpop {d1}")

    if op_tipo == "OP_ADD":
        asm.append("    vadd.f64 d0, d1, d0")
        return
    if op_tipo == "OP_SUB":
        asm.append("    vsub.f64 d0, d1, d0")
        return
    if op_tipo == "OP_MUL":
        asm.append("    vmul.f64 d0, d1, d0")
        return
    if op_tipo == "OP_DIV":
        asm.append("    vdiv.f64 d0, d1, d0")
        return

    if op_tipo == "OP_POW":
        asm.append("    vcvt.s32.f64 s0, d0")
        asm.append("    vmov r0, s0")
        asm.append("    vmov.f64 d0, d1")
        asm.append("    bl pow_f64_i32")
        return

    if op_tipo in {"OP_DIV_INT", "OP_MOD"}:
        asm.append("    vcvt.s32.f64 s2, d1")
        asm.append("    vmov r1, s2")
        asm.append("    vcvt.s32.f64 s0, d0")
        asm.append("    vmov r2, s0")
        asm.append("    bl divmod_i32")
        if op_tipo == "OP_MOD":
            asm.append("    vmov s0, r0")
        else:
            asm.append("    vmov s0, r3")
        asm.append("    vcvt.f64.s32 d0, s0")
        return

    raise ErroGeracaoAssembly(f"operador não suportado na geração: {op_tipo}", linha_idx)


def executarExpressao(vetor_tokens: List[Tuple[str, str]], memoria: dict, resultados: list):
    """
    Nesta fase, não executa cálculos em Python.
    Esta função reduz os tokens em blocos intermediários para geração de Assembly.
    """
    bloco = reduzirBlocos(vetor_tokens)
    memorias_encontradas = set()
    coletar_memorias(bloco, memorias_encontradas)
    for nome in memorias_encontradas:
        memoria.setdefault(nome, None)
    resultados.append(bloco)
    return bloco


def gerarAssembly(vetores_tokens: List[List[Tuple[str, str]]]):
    if not vetores_tokens:
        raise ErroGeracaoAssembly("não há tokens para gerar Assembly")

    blocos = []
    memoria_catalogo = {}
    resultados_blocos = []

    for idx, vetor in enumerate(vetores_tokens):
        try:
            bloco = executarExpressao(vetor, memoria_catalogo, resultados_blocos)
            blocos.append(bloco)
        except ErroGeracaoAssembly as e:
            raise ErroGeracaoAssembly(str(e), idx) from None

    constantes = {"0.0", "1.0"}
    memorias = set(memoria_catalogo.keys())
    for bloco in blocos:
        coletar_constantes(bloco, constantes)
        coletar_memorias(bloco, memorias)

    const_labels = {valor: f"const_{safe_label(valor)}" for valor in sorted(constantes)}
    mem_labels = {nome: f"mem_{safe_label(nome)}" for nome in sorted(memorias)}

    resultados_labels = [f"resultado_{i}" for i in range(len(blocos))]

    asm: List[str] = []
    asm.append(".text")
    asm.append(".global _start")
    asm.append("_start:")

    for i, bloco in enumerate(blocos):
        asm.append(f"    @ Linha {i + 1}")
        emit_expr(bloco, i, resultados_labels, asm, const_labels, mem_labels)
        asm.append(f"    ldr r0, ={resultados_labels[i]}")
        asm.append("    vstr.f64 d0, [r0]")

    asm.append("    b fim_programa")
    asm.append("")
    asm.append("divmod_i32:")
    asm.append("    @ Entrada: r1=dividendo, r2=divisor")
    asm.append("    @ Saida  : r3=quociente, r0=resto")
    asm.append("    push {r5, r6, lr}")
    asm.append("    mov r3, #0")
    asm.append("    mov r0, #0")
    asm.append("    cmp r2, #0")
    asm.append("    beq fim_divmod_i32")
    asm.append("    mov r5, #0")
    asm.append("    mov r6, #0")
    asm.append("    cmp r1, #0")
    asm.append("    bge div_i32_dividendo_ok")
    asm.append("    rsb r1, r1, #0")
    asm.append("    mov r6, #1")
    asm.append("    eor r5, r5, #1")
    asm.append("div_i32_dividendo_ok:")
    asm.append("    cmp r2, #0")
    asm.append("    bge div_i32_divisor_ok")
    asm.append("    rsb r2, r2, #0")
    asm.append("    eor r5, r5, #1")
    asm.append("div_i32_divisor_ok:")
    asm.append("    mov r0, r1")
    asm.append("div_i32_loop:")
    asm.append("    cmp r0, r2")
    asm.append("    blt div_i32_loop_fim")
    asm.append("    sub r0, r0, r2")
    asm.append("    add r3, r3, #1")
    asm.append("    b div_i32_loop")
    asm.append("div_i32_loop_fim:")
    asm.append("    cmp r5, #0")
    asm.append("    beq div_i32_sinal_resto")
    asm.append("    rsb r3, r3, #0")
    asm.append("div_i32_sinal_resto:")
    asm.append("    cmp r6, #0")
    asm.append("    beq fim_divmod_i32")
    asm.append("    rsb r0, r0, #0")
    asm.append("fim_divmod_i32:")
    asm.append("    pop {r5, r6, pc}")
    asm.append("")
    asm.append("pow_f64_i32:")
    asm.append("    push {r4, lr}")
    asm.append("    vmov.f64 d2, d0")
    asm.append(f"    ldr r4, ={const_labels['1.0']}")
    asm.append("    vldr.f64 d0, [r4]")
    asm.append("    cmp r0, #0")
    asm.append("    ble fim_pow")
    asm.append("loop_pow:")
    asm.append("    vmul.f64 d0, d0, d2")
    asm.append("    subs r0, r0, #1")
    asm.append("    bgt loop_pow")
    asm.append("fim_pow:")
    asm.append("    pop {r4, pc}")
    asm.append("")
    asm.append("fim_programa:")
    asm.append("    b fim_programa")
    asm.append("")
    asm.append(".data")
    asm.append(".align 3")

    for valor in sorted(const_labels.keys()):
        asm.append(f"{const_labels[valor]}: .double {valor}")

    for nome in sorted(mem_labels.keys()):
        asm.append(f"{mem_labels[nome]}: .double 0.0")

    for rot in resultados_labels:
        asm.append(f"{rot}: .double 0.0")

    return "\n".join(asm) + "\n"


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


def testarAnalisadorLexico():
    entradas_validas = [
        "(3.14 2.0 +)",
        "(5 RES)",
        "(10.5 CONTADOR)",
        "((A B *) (D E *) /)",
    ]
    entradas_invalidas = [
        "(3.14 2.0 &)",
        "3.14.5",
        "3,45",
        "((2.0 2.0 -)",
    ]

    print("[Teste Léxico] Válidas")
    for exp in entradas_validas:
        try:
            parseExpressao(exp)
            print(f"OK  -> {exp}")
        except ErroLexico as e:
            print(f"FALHOU (não era esperado): {exp} -> {e}")

    print("\n[Teste Léxico] Inválidas")
    for exp in entradas_invalidas:
        try:
            parseExpressao(exp)
            print(f"FALHOU (deveria dar erro): {exp}")
        except ErroLexico:
            print(f"OK  -> {exp}")

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