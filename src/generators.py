# =======================
# GERADORES DE SAÍDA
# =======================

from .models import circuito
from .simulator import simular_circuito


def gerar_resumo_textual():
    """Gera um resumo textual do circuito (ANTES da tabela verdade)"""
    filename = f"resumo_{circuito.nome or 'circuito'}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"RELATÓRIO DO CIRCUITO: {circuito.nome or 'Sem Nome'}\n")
        f.write("=" * 50 + "\n\n")

        f.write("ENTRADAS:\n")
        for entrada in circuito.entradas.values():
            f.write(f"  - {entrada}\n")

        f.write(f"\nPORTAS LÓGICAS:\n")
        for porta in circuito.portas.values():
            f.write(f"  - {porta}\n")

        f.write(f"\nSAÍDAS:\n")
        for saida in circuito.saidas.values():
            f.write(f"  - {saida}\n")

        f.write(f"\nCONEXÕES:\n")
        for conexao in circuito.conexoes:
            f.write(f"  - {conexao}\n")

    print(f"Resumo textual gerado: {filename}")


def gerar_html_circuito():
    """Gera um relatório HTML do circuito"""
    
    # Salvar estado original das entradas
    valores_originais = {nome: entrada.valor for nome, entrada in circuito.entradas.items()}
    estados_portas = {nome: (porta.valores_entradas.copy(), porta.valor_saida) 
                      for nome, porta in circuito.portas.items()}
    estados_saidas = {nome: saida.valor for nome, saida in circuito.saidas.items()}
    
    html = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Circuito {circuito.nome or 'Sem Nome'}</title>
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
        <h1>Circuito: {circuito.nome or 'Sem Nome'}</h1>

        <h2>📥 Entradas</h2>
"""

    if circuito.entradas:
        for nome, entrada in circuito.entradas.items():
            # Usar valor original salvo
            html += f'        <div class="component">🔌 <strong>{entrada.nome}</strong>: {valores_originais[nome]}</div>\n'
    else:
        html += '        <p>Nenhuma entrada definida</p>\n'

    html += '\n        <h2>🔧 Portas Lógicas</h2>\n'

    if circuito.portas:
        for nome, porta in circuito.portas.items():
            # Usar estado original salvo
            vals_entrada, val_saida = estados_portas[nome]
            html += f'''        <div class="component">
            <strong>{porta.nome}</strong> ({porta.tipo})<br>
            Entradas: {porta.entradas} | Saídas: {porta.saidas}<br>
            Estado: {vals_entrada} → {val_saida}
        </div>\n'''
    else:
        html += '        <p>Nenhuma porta lógica definida</p>\n'

    html += '\n        <h2>📤 Saídas</h2>\n'

    if circuito.saidas:
        for nome, saida in circuito.saidas.items():
            # Usar estado original salvo
            html += f'        <div class="resultado">📊 <strong>{saida.nome}</strong>: {estados_saidas[nome]}</div>\n'
    else:
        html += '        <p>Nenhuma saída definida</p>\n'

    html += '\n        <h2>🔗 Conexões</h2>\n'

    if circuito.conexoes:
        for conexao in circuito.conexoes:
            html += f'        <div class="connection">⚡ {conexao.origem} → {conexao.destino}</div>\n'
    else:
        html += '        <p>Nenhuma conexão definida</p>\n'

    # Tabela verdade do circuito (se aplicável)
    if len(circuito.entradas) <= 4:  # Só gerar para até 4 entradas
        html += '\n        <h2>📋 Tabela Verdade Completa</h2>\n'
        html += '        <table>\n            <tr>\n'

        # Cabeçalhos
        for nome in circuito.entradas.keys():
            html += f'                <th>{nome}</th>\n'
        for nome in circuito.saidas.keys():
            html += f'                <th>{nome}</th>\n'
        html += '            </tr>\n'

        # Gerar todas as combinações
        num_entradas = len(circuito.entradas)
        entrada_names = list(circuito.entradas.keys())
        
        for i in range(2 ** num_entradas):
            html += '            <tr>\n'

            # Definir valores das entradas para esta linha
            valores_entrada = []
            for j in range(num_entradas):
                valor = (i >> (num_entradas - 1 - j)) & 1
                valores_entrada.append(valor)
                html += f'                <td>{valor}</td>\n'

            # Configurar entradas para simulação
            for k, nome in enumerate(entrada_names):
                circuito.entradas[nome].valor = valores_entrada[k]

            # Reset e simular
            for porta in circuito.portas.values():
                porta.processada = False
                porta.valor_saida = None
                porta.valores_entradas = [None] * porta.entradas

            for saida in circuito.saidas.values():
                saida.valor = None

            # Simular silenciosamente
            simular_circuito(verbose=False)

            # Adicionar resultados das saídas
            for nome in circuito.saidas.keys():
                html += f'                <td><strong>{circuito.saidas[nome].valor}</strong></td>\n'

            html += '            </tr>\n'

    html += '''        </table>
    </div>
</body>
</html>'''

    # Restaurar estado original
    for nome, valor in valores_originais.items():
        circuito.entradas[nome].valor = valor
    for nome, (vals_entrada, val_saida) in estados_portas.items():
        circuito.portas[nome].valores_entradas = vals_entrada
        circuito.portas[nome].valor_saida = val_saida
    for nome, valor in estados_saidas.items():
        circuito.saidas[nome].valor = valor

    filename = f"circuito_{circuito.nome or 'sem_nome'}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\nRelatório HTML gerado: {filename}")
    return filename


def abrir_html(filename):
    """Abre o arquivo HTML no navegador padrão"""
    import webbrowser
    import os
    filepath = os.path.abspath(filename)
    webbrowser.open(f"file://{filepath}")
    print(f"Abrindo {filename} no navegador...")

