# =======================
# COMPILADOR DE CIRCUITOS LÓGICOS
# Linguagem de Domínio Específico (DSL)
# =======================

import os
import sys
from src.lexer import lexer
from src.parser_rules import parser
from src.models import circuito
from src.simulator import simular_circuito
from src.generators import gerar_html_circuito, gerar_resumo_textual, abrir_html


def criar_exemplo_padrao(arquivo):
    """Cria um arquivo de exemplo se não existir"""
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
    with open(arquivo, "w") as f:
        f.write(exemplo)
    print(f"Arquivo de exemplo criado: {arquivo}")


def processar_arquivo(arquivo_entrada):
    """Processa um arquivo de circuito"""
    circuito.limpar()

    with open(arquivo_entrada, "r", encoding="utf-8") as f:
        data = f.read()

    print("=== ANÁLISE LÉXICA E SINTÁTICA ===")

    lexer.input(data)
    print("Tokens encontrados:")
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(f"  {tok.type}: {tok.value}")

    lexer.input(data)
    parser.parse(data, lexer=lexer, debug=False)

    return circuito.nome is not None


def mostrar_ajuda():
    """Mostra as opções disponíveis"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║           COMPILADOR DE CIRCUITOS LÓGICOS                    ║
╠══════════════════════════════════════════════════════════════╣
║  Uso: python main.py [arquivo] [opcoes]                      ║
║                                                              ║
║  Opções:                                                     ║
║    --help, -h      Mostra esta ajuda                         ║
║    --no-open       Não abre o HTML automaticamente           ║
║                                                              ║
║  Exemplos:                                                   ║
║    python main.py                                            ║
║    python main.py exemplos/circuito_and.txt                  ║
║    python main.py exemplos/circuito_or.txt                   ║
║    python main.py exemplos/circuito_not.txt                  ║
║    python main.py exemplos/circuito_complexo.txt             ║
║    python main.py meu_circuito.txt --no-open                 ║
╚══════════════════════════════════════════════════════════════╝
""")


def main():
    # Verificar argumentos
    args = sys.argv[1:]
    
    if "--help" in args or "-h" in args:
        mostrar_ajuda()
        return
    
    abrir_navegador = "--no-open" not in args
    args = [a for a in args if not a.startswith("--")]
    
    arquivo_entrada = args[0] if args else "circuito_exemplo.txt"

    if not os.path.exists(arquivo_entrada):
        criar_exemplo_padrao(arquivo_entrada)

    try:
        if processar_arquivo(arquivo_entrada):
            simular_circuito()
            gerar_resumo_textual()
            html_file = gerar_html_circuito()
            
            if abrir_navegador and html_file:
                abrir_html(html_file)
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
