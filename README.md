# Fase 1 - Analisador Lexico e Gerador de Assembly para ARMv7

## Informacoes Gerais

- Instituicao: Pontificia Universidade Catolica do Parana (PUCPR)
- Disciplina: Contrucao de Interpretadores - 2026/1
- Professor: Frank Coelho de Alcantara
- Aluno: Mateus Alves Ramos (GitHub: `mateusalvesramos`)
- Grupo no Canvas: 8

## Objetivo do Trabalho

Implementar um analisador lexico com AFD (estados como funcoes) para expressoes da linguagem proposta e, a partir dos tokens gerados, produzir codigo Assembly ARMv7 compativel com o CPUlator (modelo DEC1-SOC v16.1).

## Estrutura Atual do Projeto

- `main.py`: codigo principal do analisador lexico e fluxo de leitura de arquivo.
- Arquivos de teste (`.txt`): entradas com uma expressao por linha.

## Como Executar

1. Abra o terminal na pasta do projeto.
2. Execute o programa com um arquivo de entrada:

```bash
python main.py expressoes1.txt
```
