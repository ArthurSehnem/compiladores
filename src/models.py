# =======================
# ESTRUTURAS DE DADOS
# =======================

class Porta:
    """Representa uma porta lógica no circuito"""
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

    def reset(self):
        """Reseta o estado da porta para nova simulação"""
        self.valores_entradas = [None] * self.entradas
        self.valor_saida = None
        self.processada = False

    def __str__(self):
        return f"Porta {self.nome} ({self.tipo}) - Entradas: {self.valores_entradas}, Saída: {self.valor_saida}"


class Entrada:
    """Representa uma entrada do circuito"""
    def __init__(self, nome, valor):
        self.nome = nome
        self.valor = valor
        self.valor_original = valor  # Guarda valor original

    def reset(self):
        """Restaura valor original"""
        self.valor = self.valor_original

    def __str__(self):
        return f"Entrada {self.nome} = {self.valor}"


class Saida:
    """Representa uma saída do circuito"""
    def __init__(self, nome):
        self.nome = nome
        self.valor = None

    def reset(self):
        """Reseta o valor da saída"""
        self.valor = None

    def __str__(self):
        return f"Saída {self.nome} = {self.valor}"


class Conexao:
    """Representa uma conexão entre componentes"""
    def __init__(self, origem, destino):
        self.origem = origem
        self.destino = destino

    def __str__(self):
        return f"{self.origem} -> {self.destino}"


class CircuitoState:
    """Gerencia o estado global do circuito"""
    def __init__(self):
        self.nome = None
        self.portas = {}
        self.entradas = {}
        self.saidas = {}
        self.conexoes = []

    def limpar(self):
        """Limpa todo o estado do circuito"""
        self.nome = None
        self.portas.clear()
        self.entradas.clear()
        self.saidas.clear()
        self.conexoes.clear()

    def reset_simulacao(self):
        """Reseta apenas o estado de simulação, mantendo a estrutura"""
        for porta in self.portas.values():
            porta.reset()
        for entrada in self.entradas.values():
            entrada.reset()
        for saida in self.saidas.values():
            saida.reset()


# Instância global do estado do circuito
circuito = CircuitoState()

