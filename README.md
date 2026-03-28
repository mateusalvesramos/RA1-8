# Fase 1 - Analisador Lexico e Gerador de Assembly para ARMv7

## Informacoes Gerais

- Instituicao: Pontificia Universidade Catolica do Parana (PUCPR)
- Disciplina: Contrucao de Interpretadores - 2026/1
- Professor: Frank Coelho de Alcantara
- Aluno: Mateus Alves Ramos (GitHub: mateusalvesramos)
- Grupo no Canvas: 8

## Objetivo do Trabalho

Implementar um analisador lexico com AFD (estados como funcoes) para expressoes da linguagem proposta e, a partir dos tokens gerados, produzir codigo Assembly ARMv7 compativel com o CPUlator (modelo DEC1-SOC v16.1).

## Estrutura do Projeto

```text
RA1-8/
|-- main.py
|-- lexico.py
|-- gerador.py
|-- io_utils.py
|-- expressoes1.txt
|-- expressoes2.txt
|-- expressoes3.txt
|-- tokens_ultima_execucao.txt
|-- ultimo_programa.s
|-- README.md
```

### Descricao dos Arquivos

- main.py: ponto de entrada do programa; integra leitura, analise lexica, reducao em blocos, exibicao e geracao dos arquivos finais.
- lexico.py: analisador lexico com AFD, implementado por funcoes de estado.
- gerador.py: reduz tokens para blocos intermediarios e gera codigo Assembly ARMv7.
- io_utils.py: leitura do arquivo de entrada e escrita dos arquivos de saida (tokens e assembly).
- expressoes1.txt, expressoes2.txt, expressoes3.txt: arquivos de teste da linguagem, com uma expressao por linha.
- tokens_ultima_execucao.txt: vetor de tokens salvo na ultima execucao valida.
- ultimo_programa.s: codigo Assembly gerado na ultima execucao valida.

## Como Executar

1. Abra o terminal na pasta do projeto.
2. Execute o programa com um arquivo de entrada:

```bash
python main.py expressoes1.txt
```
