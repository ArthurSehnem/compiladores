# =======================
# ANÁLISE SINTÁTICA
# =======================

import ply.yacc as yacc
from .lexer import tokens  # noqa: F401 - necessário para o PLY
from .models import Porta, Entrada, Saida, Conexao, circuito

# Precedência para resolver conflitos
precedence = (
    ('left', 'ARROW'),
)


def p_circuito(p):
    'circuito : CIRCUITO IDENT LCURL blocos RCURL'
    circuito.nome = p[2]
    print(f"Circuito '{p[2]}' definido com sucesso!")


def p_blocos(p):
    '''blocos : blocos bloco
              | bloco'''
    pass


def p_bloco(p):
    '''bloco : porta_logica_def
             | entrada_def
             | saida_def
             | conexao_def'''
    pass


def p_porta_logica_def(p):
    'porta_logica_def : PORTA_LOGICA IDENT IDENT LCURL porta_props RCURL'
    tipo, nome = p[2], p[3]
    props = p[5]

    if 'numero_de_entradas' not in props or 'numero_de_saidas' not in props or 'tabela_verdade' not in props:
        print(f"Erro: Porta {nome} deve ter numero_de_entradas, numero_de_saidas e tabela_verdade")
        return

    entradas_num = props['numero_de_entradas']
    saidas_num = props['numero_de_saidas']
    tabela = props['tabela_verdade']

    circuito.portas[nome] = Porta(tipo, nome, entradas_num, saidas_num, tabela)
    print(f"Porta lógica {nome} ({tipo}) definida")


def p_porta_props(p):
    '''porta_props : porta_props linha_porta
                   | linha_porta'''
    if len(p) == 3:
        p[1].update(p[2])
        p[0] = p[1]
    else:
        p[0] = p[1]


def p_linha_porta_num(p):
    '''linha_porta : NUMERO_DE_ENTRADAS NUM
                   | NUMERO_DE_SAIDAS NUM'''
    p[0] = {p[1]: p[2]}


def p_linha_porta_tabela(p):
    'linha_porta : TABELA_VERDADE LCURL tabela_entradas RCURL'
    p[0] = {'tabela_verdade': p[3]}


def p_tabela_entradas(p):
    '''tabela_entradas : tabela_entradas linha_tabela
                       | linha_tabela'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_linha_tabela(p):
    'linha_tabela : lista_bits ARROW lista_bits'
    p[0] = (p[1], p[3])


def p_lista_bits(p):
    '''lista_bits : lista_bits NUM
                  | NUM'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_entrada_def(p):
    'entrada_def : ENTRADA IDENT LCURL linha_entrada RCURL'
    nome = p[2]
    valor = p[4]['valor_inicial']
    circuito.entradas[nome] = Entrada(nome, valor)
    print(f"Entrada {nome} = {valor} definida")


def p_linha_entrada(p):
    'linha_entrada : VALOR_INICIAL NUM'
    p[0] = {'valor_inicial': p[2]}


def p_saida_def(p):
    'saida_def : SAIDA IDENT LCURL RCURL'
    nome = p[2]
    circuito.saidas[nome] = Saida(nome)
    print(f"Saída {nome} definida")


def p_conexao_def(p):
    'conexao_def : CONEXAO CONECTAR origem ARROW destino'
    origem = p[3]
    destino = p[5]
    circuito.conexoes.append(Conexao(origem, destino))
    print(f"Conexão: {origem} -> {destino}")


def p_origem(p):
    '''origem : IDENT DOT IDENT
              | IDENT DOT SAIDA
              | IDENT DOT ENTRADA'''
    p[0] = f"{p[1]}.{p[3]}"


def p_destino(p):
    '''destino : IDENT DOT IDENT
               | IDENT DOT SAIDA
               | IDENT DOT ENTRADA'''
    p[0] = f"{p[1]}.{p[3]}"


def p_error(p):
    if p:
        print(f"Erro sintático na linha {p.lineno}: token inesperado '{p.value}'")
    else:
        print("Erro sintático: final de arquivo inesperado")


import os

# Diretório para arquivos de cache do parser
_cache_dir = os.path.join(os.path.dirname(__file__), '__pycache__')
os.makedirs(_cache_dir, exist_ok=True)

# Cria o parser
parser = yacc.yacc(start='circuito', outputdir=_cache_dir, debuglog=None, errorlog=None)

