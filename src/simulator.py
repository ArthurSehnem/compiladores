# =======================
# SIMULADOR DE CIRCUITOS
# =======================

from .models import circuito


def validar_circuito():
    """Valida a estrutura do circuito"""
    erros = []

    # Verificar se todas as conexões são válidas
    for conexao in circuito.conexoes:
        origem_componente, origem_pino = conexao.origem.split('.')
        destino_componente, destino_pino = conexao.destino.split('.')

        # Verificar origem
        if origem_componente not in circuito.entradas and origem_componente not in circuito.portas:
            erros.append(f"Componente de origem '{origem_componente}' não existe")

        # Verificar destino
        if destino_componente not in circuito.portas and destino_componente not in circuito.saidas:
            erros.append(f"Componente de destino '{destino_componente}' não existe")

    # Verificar se todas as entradas das portas estão conectadas
    for nome, porta in circuito.portas.items():
        entradas_conectadas = 0
        for conexao in circuito.conexoes:
            if conexao.destino.startswith(f"{nome}.entrada"):
                entradas_conectadas += 1

        if entradas_conectadas < porta.entradas:
            erros.append(f"Porta '{nome}' tem {porta.entradas} entradas mas apenas {entradas_conectadas} conectadas")

    return erros


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

    for conexao in circuito.conexoes:
        if conexao.origem == origem_completa:
            destino_componente, destino_pino = conexao.destino.split('.')

            if destino_componente in circuito.portas:
                # Conectar a uma entrada de porta
                if destino_pino.startswith('entrada'):
                    indice = int(destino_pino.replace('entrada', ''))
                    circuito.portas[destino_componente].valores_entradas[indice] = valor
            elif destino_componente in circuito.saidas:
                # Conectar a uma saída
                circuito.saidas[destino_componente].valor = valor


def simular_circuito(verbose=True):
    """Simula o circuito completo"""
    if verbose:
        print("\n=== INICIANDO SIMULAÇÃO ===")

    # Validar circuito antes da simulação
    erros = validar_circuito()
    if erros:
        print("Erros encontrados no circuito:")
        for erro in erros:
            print(f"  - {erro}")
        return False

    # Reset do estado das portas
    for porta in circuito.portas.values():
        porta.processada = False
        porta.valor_saida = None

    # Propagar valores das entradas
    if verbose:
        print("\nPropagando sinais das entradas:")
    for nome, entrada in circuito.entradas.items():
        if verbose:
            print(f"  {entrada}")
        propagar_sinal(nome, "saida", entrada.valor)

    # Simular portas em ordem (múltiplas passadas se necessário)
    max_iteracoes = len(circuito.portas) + 1
    for iteracao in range(max_iteracoes):
        progresso = False

        for nome, porta in circuito.portas.items():
            if not porta.processada and porta.todas_entradas_conectadas():
                resultado = avaliar_porta(porta)
                if resultado is not None:
                    porta.valor_saida = resultado
                    porta.processada = True
                    progresso = True
                    if verbose:
                        print(f"  {porta}")
                    propagar_sinal(nome, "saida", resultado)

        if not progresso:
            break

    # Verificar se todas as portas foram processadas
    portas_nao_processadas = [nome for nome, porta in circuito.portas.items() if not porta.processada]
    if portas_nao_processadas:
        print(f"Aviso: Portas não processadas: {portas_nao_processadas}")

    # Mostrar resultados finais
    if verbose:
        print("\n=== RESULTADOS FINAIS ===")
        for nome, saida in circuito.saidas.items():
            print(f"  {saida}")

    return True

