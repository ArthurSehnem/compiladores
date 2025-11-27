# Módulos do compilador de circuitos
from .lexer import lexer, tokens
from .parser_rules import parser
from .models import circuito, Porta, Entrada, Saida, Conexao
from .simulator import simular_circuito, validar_circuito
from .generators import gerar_html_circuito, gerar_resumo_textual, abrir_html

