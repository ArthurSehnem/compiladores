import ply.lex as lex
import ply.yacc as yacc
import os
from collections import defaultdict, deque

# =======================
# 1. ANÁLISE LÉXICA
# =======================

tokens = (
    "CIRCUITO", "PORTA_LOGICA", "ENTRADA", "SAIDA",
    "CONEXAO", "CONECTAR", "NUMERO_DE_ENTRADAS", "NUMERO_DE_SAIDAS",
    "TABELA_VERDADE", "VALOR_INICIAL",
    "IDENT", "NUM", "ARROW", "DOT",
    "LCURL", "RCURL"
)

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
    # Só usar palavras reservadas se não estão em contexto de conexão
    # Para conexões, deixar como IDENT
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


lexer = lex.lex()


# =======================
# 2. ESTRUTURAS DE DADOS
# =======================

class Porta:
    def __init__(self, tipo, nome, entradas, saidas, tabela):
        self.tipo = tipo
        self.nome = nome
        self.entradas = entradas
        self.saidas = saidas
        self.tabela = tabela
        self.valores_entradas = [None] * entradas
        self.valor_saida = None
        self.processada = False

    def todas_entradas_conectadas(self):
        return all(v is not None for v in self.valores_entradas)

    def __str__(self):
        return f"Porta {self.nome} ({self.tipo}) - Entradas: {self.valores_entradas}, Saída: {self.valor_saida}"


class Entrada:
    def __init__(self, nome, valor):
        self.nome = nome
        self.valor = valor

    def __str__(self):
        return f"Entrada {self.nome} = {self.valor}"


class Saida:
    def __init__(self, nome):
        self.nome = nome
        self.valor = None

    def __str__(self):
        return f"Saída {self.nome} = {self.valor}"


class Conexao:
    def __init__(self, origem, destino):
        self.origem = origem
        self.destino = destino

    def __str__(self):
        return f"{self.origem} -> {self.destino}"


# Armazenamento global do circuito
circuito_atual = {}
portas = {}
entradas = {}
saidas = {}
conexoes = []

# =======================
# 3. ANÁLISE SINTÁTICA
# =======================

# Definir precedência para resolver conflitos
precedence = (
    ('left', 'ARROW'),
)


def p_circuito(p):
    'circuito : CIRCUITO IDENT LCURL blocos RCURL'
    circuito_atual['nome'] = p[2]
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

    portas[nome] = Porta(tipo, nome, entradas_num, saidas_num, tabela)
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
    entradas[nome] = Entrada(nome, valor)
    print(f"Entrada {nome} = {valor} definida")


def p_linha_entrada(p):
    'linha_entrada : VALOR_INICIAL NUM'
    p[0] = {'valor_inicial': p[2]}


def p_saida_def(p):
    'saida_def : SAIDA IDENT LCURL RCURL'
    nome = p[2]
    saidas[nome] = Saida(nome)
    print(f"Saída {nome} definida")


def p_conexao_def(p):
    'conexao_def : CONEXAO CONECTAR origem ARROW destino'
    origem = p[3]
    destino = p[5]
    conexoes.append(Conexao(origem, destino))
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


parser = yacc.yacc(start='circuito')


# =======================
# 4. VALIDAÇÃO DO CIRCUITO
# =======================

def validar_circuito():
    """Valida a estrutura do circuito"""
    erros = []

    # Verificar se todas as conexões são válidas
    for conexao in conexoes:
        origem_componente, origem_pino = conexao.origem.split('.')
        destino_componente, destino_pino = conexao.destino.split('.')

        # Verificar origem
        if origem_componente not in entradas and origem_componente not in portas:
            erros.append(f"Componente de origem '{origem_componente}' não existe")

        # Verificar destino
        if destino_componente not in portas and destino_componente not in saidas:
            erros.append(f"Componente de destino '{destino_componente}' não existe")

    # Verificar se todas as entradas das portas estão conectadas
    for nome, porta in portas.items():
        entradas_conectadas = 0
        for conexao in conexoes:
            if conexao.destino.startswith(f"{nome}.entrada"):
                entradas_conectadas += 1

        if entradas_conectadas < porta.entradas:
            erros.append(f"Porta '{nome}' tem {porta.entradas} entradas mas apenas {entradas_conectadas} conectadas")

    return erros


# =======================
# 5. SIMULADOR MELHORADO
# =======================

def avaliar_porta(porta):
    """Avalia uma porta lógica usando sua tabela verdade"""
    if not porta.todas_entradas_conectadas():
        return None

    for entrada, saida in porta.tabela:
        if porta.valores_entradas == entrada:
            return saida[0] if isinstance(saida, list) else saida

    print(f"Aviso: Combinação de entrada {porta.valores_entradas} não encontrada na tabela de {porta.nome}")
    return 0


def propagar_sinal(componente_origem, pino_origem, valor):
    """Propaga um sinal através das conexões"""
    origem_completa = f"{componente_origem}.{pino_origem}"

    for conexao in conexoes:
        if conexao.origem == origem_completa:
            destino_componente, destino_pino = conexao.destino.split('.')

            if destino_componente in portas:
                # Conectar a uma entrada de porta
                if destino_pino.startswith('entrada'):
                    indice = int(destino_pino.replace('entrada', ''))
                    portas[destino_componente].valores_entradas[indice] = valor
            elif destino_componente in saidas:
                # Conectar a uma saída
                saidas[destino_componente].valor = valor


def simular_circuito():
    """Simula o circuito completo"""
    print("\n=== INICIANDO SIMULAÇÃO ===")

    # Validar circuito antes da simulação
    erros = validar_circuito()
    if erros:
        print("Erros encontrados no circuito:")
        for erro in erros:
            print(f"  - {erro}")
        return

    # Reset do estado das portas
    for porta in portas.values():
        porta.processada = False
        porta.valor_saida = None

    # Propagar valores das entradas
    print("\nPropagando sinais das entradas:")
    for nome, entrada in entradas.items():
        print(f"  {entrada}")
        propagar_sinal(nome, "saida", entrada.valor)

    # Simular portas em ordem (múltiplas passadas se necessário)
    max_iteracoes = len(portas) + 1
    for iteracao in range(max_iteracoes):
        progresso = False

        for nome, porta in portas.items():
            if not porta.processada and porta.todas_entradas_conectadas():
                resultado = avaliar_porta(porta)
                if resultado is not None:
                    porta.valor_saida = resultado
                    porta.processada = True
                    progresso = True
                    print(f"  {porta}")
                    propagar_sinal(nome, "saida", resultado)

        if not progresso:
            break

    # Verificar se todas as portas foram processadas
    portas_nao_processadas = [nome for nome, porta in portas.items() if not porta.processada]
    if portas_nao_processadas:
        print(f"Aviso: Portas não processadas: {portas_nao_processadas}")

    # Mostrar resultados finais
    print("\n=== RESULTADOS FINAIS ===")
    for nome, saida in saidas.items():
        print(f"  {saida}")


# =======================
# 6. GERADORES DE SAÍDA
# =======================

def gerar_html_circuito():
    """Gera um relatório HTML do circuito"""
    html = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Circuito {circuito_atual.get('nome', 'Sem Nome')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }}
        .container {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        .component {{ background: #ecf0f1; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #3498db; }}
        .connection {{ background: #e8f5e8; padding: 10px; margin: 5px 0; border-radius: 3px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 10px; text-align: center; border: 1px solid #bdc3c7; }}
        th {{ background-color: #3498db; color: white; }}
        .resultado {{ background: #d5f4e6; padding: 15px; border-radius: 5px; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Circuito: {circuito_atual.get('nome', 'Sem Nome')}</h1>

        <h2>📥 Entradas</h2>
"""

    if entradas:
        for nome, entrada in entradas.items():
            html += f'        <div class="component">🔌 <strong>{entrada.nome}</strong>: {entrada.valor}</div>\n'
    else:
        html += '        <p>Nenhuma entrada definida</p>\n'

    html += '\n        <h2>🔧 Portas Lógicas</h2>\n'

    if portas:
        for nome, porta in portas.items():
            html += f'''        <div class="component">
            <strong>{porta.nome}</strong> ({porta.tipo})<br>
            Entradas: {porta.entradas} | Saídas: {porta.saidas}<br>
            Estado: {porta.valores_entradas} → {porta.valor_saida}
        </div>\n'''
    else:
        html += '        <p>Nenhuma porta lógica definida</p>\n'

    html += '\n        <h2>📤 Saídas</h2>\n'

    if saidas:
        for nome, saida in saidas.items():
            html += f'        <div class="resultado">📊 <strong>{saida.nome}</strong>: {saida.valor}</div>\n'
    else:
        html += '        <p>Nenhuma saída definida</p>\n'

    html += '\n        <h2>🔗 Conexões</h2>\n'

    if conexoes:
        for conexao in conexoes:
            html += f'        <div class="connection">⚡ {conexao.origem} → {conexao.destino}</div>\n'
    else:
        html += '        <p>Nenhuma conexão definida</p>\n'

    # Tabela verdade do circuito (se aplicável)
    if len(entradas) <= 4:  # Só gerar para até 4 entradas (para não ficar muito grande)
        html += '\n        <h2>📋 Tabela Verdade Completa</h2>\n'
        html += '        <table>\n            <tr>\n'

        # Cabeçalhos
        for nome in entradas.keys():
            html += f'                <th>{nome}</th>\n'
        for nome in saidas.keys():
            html += f'                <th>{nome}</th>\n'
        html += '            </tr>\n'

        # Gerar todas as combinações
        num_entradas = len(entradas)
        for i in range(2 ** num_entradas):
            html += '            <tr>\n'

            # Definir valores das entradas para esta linha
            valores_entrada = []
            for j in range(num_entradas):
                valor = (i >> (num_entradas - 1 - j)) & 1
                valores_entrada.append(valor)
                html += f'                <td>{valor}</td>\n'

            # Simular com estes valores
            entrada_names = list(entradas.keys())
            for k, nome in enumerate(entrada_names):
                entradas[nome].valor = valores_entrada[k]

            # Reset e simular
            for porta in portas.values():
                porta.processada = False
                porta.valor_saida = None
                porta.valores_entradas = [None] * porta.entradas

            for saida in saidas.values():
                saida.valor = None

            # Simular silenciosamente
            import io
            import sys
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()
            try:
                simular_circuito()
            finally:
                sys.stdout = old_stdout

            # Adicionar resultados das saídas
            for nome in saidas.keys():
                html += f'                <td><strong>{saidas[nome].valor}</strong></td>\n'

            html += '            </tr>\n'

    html += '''        </table>
    </div>
</body>
</html>'''

    filename = f"circuito_{circuito_atual.get('nome', 'sem_nome')}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\nRelatório HTML gerado: {filename}")


def gerar_resumo_textual():
    """Gera um resumo textual do circuito"""
    filename = f"resumo_{circuito_atual.get('nome', 'circuito')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"RELATÓRIO DO CIRCUITO: {circuito_atual.get('nome', 'Sem Nome')}\n")
        f.write("=" * 50 + "\n\n")

        f.write("ENTRADAS:\n")
        for entrada in entradas.values():
            f.write(f"  - {entrada}\n")

        f.write(f"\nPORTAS LÓGICAS:\n")
        for porta in portas.values():
            f.write(f"  - {porta}\n")

        f.write(f"\nSAÍDAS:\n")
        for saida in saidas.values():
            f.write(f"  - {saida}\n")

        f.write(f"\nCONEXÕES:\n")
        for conexao in conexoes:
            f.write(f"  - {conexao}\n")

    print(f"Resumo textual gerado: {filename}")


# =======================
# 7. EXECUÇÃO PRINCIPAL
# =======================

def limpar_estado():
    """Limpa o estado global para nova execução"""
    global circuito_atual, portas, entradas, saidas, conexoes
    circuito_atual.clear()
    portas.clear()
    entradas.clear()
    saidas.clear()
    conexoes.clear()


def main():
    arquivo_entrada = "circuito_exemplo.txt"

    if not os.path.exists(arquivo_entrada):
        # Criar arquivo de exemplo se não existir
        exemplo = """circuito MeuCircuito {
    entrada A {
        valor_inicial 1
    }

    entrada B {
        valor_inicial 0
    }

    porta_logica AND porta1 {
        numero_de_entradas 2
        numero_de_saidas 1
        tabela_verdade {
            0 0 -> 0
            0 1 -> 0
            1 0 -> 0
            1 1 -> 1
        }
    }

    saida resultado {
    }

    conexao conectar A.saida -> porta1.entrada0
    conexao conectar B.saida -> porta1.entrada1
    conexao conectar porta1.saida -> resultado.entrada
}"""
        with open(arquivo_entrada, "w") as f:
            f.write(exemplo)
        print(f"Arquivo de exemplo criado: {arquivo_entrada}")

    try:
        # Limpar estado anterior
        limpar_estado()

        with open(arquivo_entrada, "r", encoding="utf-8") as f:
            data = f.read()

        print("=== ANÁLISE LÉXICA E SINTÁTICA ===")

        # Debug: mostrar tokens
        lexer.input(data)
        print("Tokens encontrados:")
        while True:
            tok = lexer.token()
            if not tok:
                break
            print(f"  {tok.type}: {tok.value}")

        # Reiniciar lexer para parsing
        lexer.input(data)
        resultado = parser.parse(data, lexer=lexer, debug=False)

        if circuito_atual:
            simular_circuito()
            gerar_html_circuito()
            gerar_resumo_textual()
        else:
            print("Erro: Circuito não foi definido corretamente")

    except FileNotFoundError:
        print(f"Erro: Arquivo '{arquivo_entrada}' não encontrado")
    except Exception as e:
        print(f"Erro durante a execução: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()