# =======================
# ANÁLISE LÉXICA
# =======================

import ply.lex as lex

# Lista de tokens
tokens = (
    "CIRCUITO", "PORTA_LOGICA", "ENTRADA", "SAIDA",
    "CONEXAO", "CONECTAR", "NUMERO_DE_ENTRADAS", "NUMERO_DE_SAIDAS",
    "TABELA_VERDADE", "VALOR_INICIAL",
    "IDENT", "NUM", "ARROW", "DOT",
    "LCURL", "RCURL"
)

# Palavras reservadas
reserved = {
    "circuito": "CIRCUITO",
    "porta_logica": "PORTA_LOGICA",
    "entrada": "ENTRADA",
    "saida": "SAIDA",
    "conexao": "CONEXAO",
    "conectar": "CONECTAR",
    "numero_de_entradas": "NUMERO_DE_ENTRADAS",
    "numero_de_saidas": "NUMERO_DE_SAIDAS",
    "tabela_verdade": "TABELA_VERDADE",
    "valor_inicial": "VALOR_INICIAL"
}

# Tokens simples (expressões regulares)
t_ARROW = r'->'
t_DOT = r'\.'
t_LCURL = r'\{'
t_RCURL = r'\}'
t_ignore = ' \t'


def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_IDENT(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENT')
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_comment(t):
    r'//.*'
    pass


def t_error(t):
    print(f"Erro léxico na linha {t.lexer.lineno}: caractere inválido '{t.value[0]}'")
    t.lexer.skip(1)


# Cria o lexer
lexer = lex.lex()

