# Compilador de Circuitos Lógicos

DSL para definição e simulação de circuitos lógicos digitais.

## Estrutura do Projeto

```
compiladores/
├── main.py              # Ponto de entrada
├── requirements.txt     # Dependências
├── src/
│   ├── lexer.py         # Análise léxica
│   ├── parser_rules.py  # Análise sintática
│   ├── models.py        # Classes de dados
│   ├── simulator.py     # Simulador
│   └── generators.py    # Geradores HTML/TXT
└── exemplos/
    ├── circuito_and.txt
    ├── circuito_or.txt
    ├── circuito_not.txt
    └── circuito_complexo.txt
```

## Como usar

```bash

# Ativar ambiente virtual primeiro
source venv/bin/activate

pip install -r requirements.txt

# 1. Ver ajuda
python main.py --help

# 2. Rodar exemplo padrão (AND simples)
python main.py

# 3. Testar porta AND (A=1, B=1 → S=1)
python main.py exemplos/circuito_and.txt

# 4. Testar porta OR (A=0, B=1 → S=1)
python main.py exemplos/circuito_or.txt

# 5. Testar porta NOT (A=1 → S=0)
python main.py exemplos/circuito_not.txt

# 6. Testar circuito complexo (A AND B) OR (NOT C)
python main.py exemplos/circuito_complexo.txt

# 7. Rodar sem abrir navegador
python main.py exemplos/circuito_and.txt --no-open
```

## Sintaxe da Linguagem

### Estrutura básica

```
circuito NomeDoCircuito {
    entrada NOME { valor_inicial 0 }
    
    porta_logica TIPO nome {
        numero_de_entradas N
        numero_de_saidas 1
        tabela_verdade {
            0 0 -> 0
            1 1 -> 1
        }
    }
    
    saida NOME { }
    
    conexao conectar origem.saida -> destino.entrada0
}
```

### Componentes

- **entrada**: define entrada do circuito com valor inicial (0 ou 1)
- **porta_logica**: define porta com tabela verdade customizada
- **saida**: define saída do circuito
- **conexao**: conecta componentes entre si

## Saídas geradas

- `circuito_NOME.html` - relatório visual com tabela verdade
- `resumo_NOME.txt` - resumo em texto

## Exemplos

Veja a pasta `exemplos/` para circuitos AND, OR, NOT e combinações.

## Tokens da linguagem

| Token | Descrição |
|-------|-----------|
| circuito | declara um circuito |
| entrada | declara entrada |
| saida | declara saída |
| porta_logica | declara porta lógica |
| conexao conectar | define conexão |
| tabela_verdade | define comportamento |
| -> | separador entrada/saída |
| { } | delimitadores de bloco |
