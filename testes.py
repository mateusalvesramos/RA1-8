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