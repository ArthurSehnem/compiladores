# 🔌 Compilador de Circuitos Lógicos

> **Linguagem de Domínio Específico (DSL)** para definição, análise e simulação de circuitos lógicos digitais.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PLY](https://img.shields.io/badge/PLY-3.11-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 🚀 Quick Start

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

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Arquitetura do Compilador](#-arquitetura-do-compilador)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
- [Sintaxe da Linguagem](#-sintaxe-da-linguagem)
- [Análise Léxica](#-análise-léxica)
- [Análise Sintática](#-análise-sintática)
- [Modelo de Dados](#-modelo-de-dados)
- [Simulador](#-simulador)
- [Geradores de Saída](#-geradores-de-saída)
- [Exemplos](#-exemplos)
- [Referência Técnica](#-referência-técnica)

---

## 📖 Sobre o Projeto

Este projeto implementa um **compilador completo** para uma linguagem de domínio específico (DSL) voltada à descrição e simulação de circuitos lógicos digitais. O compilador segue a arquitetura clássica de compiladores, incluindo:

1. **Análise Léxica** - Tokenização do código fonte
2. **Análise Sintática** - Construção da árvore sintática
3. **Representação Intermediária** - Modelo de dados do circuito
4. **Simulação** - Execução do circuito com propagação de sinais
5. **Geração de Código** - Relatórios em HTML e TXT

### Funcionalidades Principais

- ✅ Definição de entradas com valores iniciais (0 ou 1)
- ✅ Definição de portas lógicas customizadas via tabela verdade
- ✅ Definição de saídas do circuito
- ✅ Conexões flexíveis entre componentes
- ✅ Simulação automática com propagação de sinais
- ✅ Geração de tabela verdade completa
- ✅ Relatório HTML interativo
- ✅ Suporte a comentários no código

---

## 🏗️ Arquitetura do Compilador

```
┌─────────────────────────────────────────────────────────────────┐
│                        CÓDIGO FONTE                              │
│                    (arquivo .txt)                                │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                     ANÁLISE LÉXICA                               │
│                      (lexer.py)                                  │
│  • Tokenização do código fonte                                  │
│  • Identificação de palavras reservadas                         │
│  • Tratamento de erros léxicos                                  │
└───────────────────────────┬─────────────────────────────────────┘
                            │ Tokens
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ANÁLISE SINTÁTICA                             │
│                    (parser_rules.py)                             │
│  • Gramática livre de contexto                                  │
│  • Construção do modelo do circuito                             │
│  • Validação estrutural                                         │
└───────────────────────────┬─────────────────────────────────────┘
                            │ Modelo do Circuito
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   REPRESENTAÇÃO INTERMEDIÁRIA                    │
│                       (models.py)                                │
│  • Classes: Porta, Entrada, Saida, Conexao                      │
│  • Estado global: CircuitoState                                 │
└───────────────────────────┬─────────────────────────────────────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
              ▼                           ▼
┌─────────────────────────┐   ┌─────────────────────────┐
│       SIMULADOR         │   │    GERADORES DE SAÍDA   │
│     (simulator.py)      │   │     (generators.py)     │
│  • Propagação de sinais │   │  • Relatório HTML       │
│  • Avaliação de portas  │   │  • Resumo textual       │
│  • Validação do circuito│   │  • Tabela verdade       │
└─────────────────────────┘   └─────────────────────────┘
```

---

## 📁 Estrutura do Projeto

```
compiladores/
├── main.py                    # 🚀 Ponto de entrada principal
├── requirements.txt           # 📦 Dependências do projeto
├── README.md                  # 📖 Esta documentação
├── circuito_exemplo.txt       # 📄 Exemplo padrão (gerado automaticamente)
│
├── src/                       # 📂 Código fonte do compilador
│   ├── __init__.py           # Inicialização do módulo
│   ├── lexer.py              # 🔤 Análise léxica (tokenização)
│   ├── parser_rules.py       # 📐 Análise sintática (gramática)
│   ├── models.py             # 🗃️ Modelos de dados
│   ├── simulator.py          # ⚡ Motor de simulação
│   └── generators.py         # 📊 Geradores de relatórios
│
├── exemplos/                  # 📂 Circuitos de exemplo
│   ├── circuito_and.txt      # Porta AND simples
│   ├── circuito_or.txt       # Porta OR simples
│   ├── circuito_not.txt      # Porta NOT (inversor)
│   └── circuito_complexo.txt # Circuito combinacional
│
└── venv/                      # 📂 Ambiente virtual Python
```

---

## 🔧 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

```bash
# 1. Clone ou navegue até o diretório do projeto
cd compiladores

# 2. Crie o ambiente virtual (se ainda não existir)
python3 -m venv venv

# 3. Ative o ambiente virtual
source venv/bin/activate  # Linux/macOS
# ou
.\venv\Scripts\activate   # Windows

# 4. Instale as dependências
pip install -r requirements.txt
```

### Dependências

| Pacote | Versão | Descrição |
|--------|--------|-----------|
| PLY | 3.11 | Python Lex-Yacc - Ferramentas para análise léxica e sintática |

---

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

### Opções da Linha de Comando

| Opção | Descrição |
|-------|-----------|
| `--help`, `-h` | Mostra a ajuda |
| `--no-open` | Não abre o HTML automaticamente no navegador |

### Saídas Geradas

Após a execução, são gerados dois arquivos:

1. **`circuito_NOME.html`** - Relatório visual completo com:
   - Lista de entradas e seus valores
   - Lista de portas lógicas e seus estados
   - Lista de saídas com resultados
   - Diagrama de conexões
   - Tabela verdade completa (para até 4 entradas)

2. **`resumo_NOME.txt`** - Resumo textual com:
   - Componentes do circuito
   - Estados da simulação
   - Conexões definidas

---

## 📝 Sintaxe da Linguagem

### Estrutura Geral

```
circuito NomeDoCircuito {
    // Comentários iniciados com //
    
    entrada NOME {
        valor_inicial VALOR
    }
    
    porta_logica TIPO nome {
        numero_de_entradas N
        numero_de_saidas M
        tabela_verdade {
            ENTRADA1 ENTRADA2 ... -> SAIDA1 SAIDA2 ...
        }
    }
    
    saida NOME {
    }
    
    conexao conectar origem.pino -> destino.pino
}
```

### Componentes

#### 1. Circuito

Define o container principal do circuito.

```
circuito MeuCircuito {
    // componentes aqui
}
```

#### 2. Entrada

Define uma entrada do circuito com valor inicial binário.

```
entrada A {
    valor_inicial 1    // 0 ou 1
}
```

#### 3. Porta Lógica

Define uma porta lógica customizada através de sua tabela verdade.

```
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
```

#### 4. Saída

Define uma saída do circuito.

```
saida resultado {
}
```

#### 5. Conexão

Conecta componentes entre si.

```
conexao conectar A.saida -> porta1.entrada0
conexao conectar porta1.saida -> resultado.entrada
```

### Convenções de Nomenclatura

| Elemento | Formato |
|----------|---------|
| Nome do circuito | `PascalCase` |
| Nome de entrada | `MAIÚSCULAS` ou `PascalCase` |
| Nome de porta | `snake_case` |
| Nome de saída | `snake_case` ou `MAIÚSCULAS` |
| Pinos de entrada | `entrada0`, `entrada1`, ... |
| Pinos de saída | `saida` |

---

## 🔤 Análise Léxica

O analisador léxico (`lexer.py`) é responsável por transformar o código fonte em uma sequência de tokens.

### Tokens Reconhecidos

| Token | Padrão | Descrição |
|-------|--------|-----------|
| `CIRCUITO` | `circuito` | Palavra reservada |
| `ENTRADA` | `entrada` | Palavra reservada |
| `SAIDA` | `saida` | Palavra reservada |
| `PORTA_LOGICA` | `porta_logica` | Palavra reservada |
| `CONEXAO` | `conexao` | Palavra reservada |
| `CONECTAR` | `conectar` | Palavra reservada |
| `NUMERO_DE_ENTRADAS` | `numero_de_entradas` | Palavra reservada |
| `NUMERO_DE_SAIDAS` | `numero_de_saidas` | Palavra reservada |
| `TABELA_VERDADE` | `tabela_verdade` | Palavra reservada |
| `VALOR_INICIAL` | `valor_inicial` | Palavra reservada |
| `IDENT` | `[a-zA-Z_][a-zA-Z0-9_]*` | Identificador |
| `NUM` | `\d+` | Número inteiro |
| `ARROW` | `->` | Operador de seta |
| `DOT` | `.` | Operador de ponto |
| `LCURL` | `{` | Abre chaves |
| `RCURL` | `}` | Fecha chaves |

### Caracteres Ignorados

- Espaços e tabulações (`\t`)
- Quebras de linha (`\n`) - contadas para rastreamento de linha
- Comentários de linha (`//...`)

### Exemplo de Tokenização

Código fonte:
```
entrada A {
    valor_inicial 1
}
```

Tokens gerados:
```
ENTRADA: entrada
IDENT: A
LCURL: {
VALOR_INICIAL: valor_inicial
NUM: 1
RCURL: }
```

---

## 📐 Análise Sintática

O analisador sintático (`parser_rules.py`) implementa uma gramática livre de contexto usando o algoritmo LALR(1).

### Gramática BNF

```bnf
<circuito>        ::= CIRCUITO IDENT LCURL <blocos> RCURL

<blocos>          ::= <blocos> <bloco>
                    | <bloco>

<bloco>           ::= <porta_logica_def>
                    | <entrada_def>
                    | <saida_def>
                    | <conexao_def>

<entrada_def>     ::= ENTRADA IDENT LCURL <linha_entrada> RCURL

<linha_entrada>   ::= VALOR_INICIAL NUM

<porta_logica_def>::= PORTA_LOGICA IDENT IDENT LCURL <porta_props> RCURL

<porta_props>     ::= <porta_props> <linha_porta>
                    | <linha_porta>

<linha_porta>     ::= NUMERO_DE_ENTRADAS NUM
                    | NUMERO_DE_SAIDAS NUM
                    | TABELA_VERDADE LCURL <tabela_entradas> RCURL

<tabela_entradas> ::= <tabela_entradas> <linha_tabela>
                    | <linha_tabela>

<linha_tabela>    ::= <lista_bits> ARROW <lista_bits>

<lista_bits>      ::= <lista_bits> NUM
                    | NUM

<saida_def>       ::= SAIDA IDENT LCURL RCURL

<conexao_def>     ::= CONEXAO CONECTAR <origem> ARROW <destino>

<origem>          ::= IDENT DOT IDENT
                    | IDENT DOT SAIDA
                    | IDENT DOT ENTRADA

<destino>         ::= IDENT DOT IDENT
                    | IDENT DOT SAIDA
                    | IDENT DOT ENTRADA
```

### Ações Semânticas

Durante a análise sintática, as seguintes ações são executadas:

1. **Definição de Circuito**: Armazena o nome do circuito
2. **Definição de Entrada**: Cria objeto `Entrada` com valor inicial
3. **Definição de Porta**: Cria objeto `Porta` com tabela verdade
4. **Definição de Saída**: Cria objeto `Saida`
5. **Definição de Conexão**: Cria objeto `Conexao` entre componentes

---

## 🗃️ Modelo de Dados

O módulo `models.py` define as estruturas de dados que representam o circuito.

### Classes

#### `Porta`

Representa uma porta lógica no circuito.

```python
class Porta:
    tipo: str              # Tipo da porta (AND, OR, NOT, etc.)
    nome: str              # Nome identificador
    entradas: int          # Número de entradas
    saidas: int            # Número de saídas
    tabela: list           # Tabela verdade [(entrada, saida), ...]
    valores_entradas: list # Valores atuais das entradas
    valor_saida: int       # Valor atual da saída
    processada: bool       # Flag de processamento
```

#### `Entrada`

Representa uma entrada do circuito.

```python
class Entrada:
    nome: str              # Nome identificador
    valor: int             # Valor atual (0 ou 1)
    valor_original: int    # Valor inicial definido
```

#### `Saida`

Representa uma saída do circuito.

```python
class Saida:
    nome: str              # Nome identificador
    valor: int             # Valor calculado
```

#### `Conexao`

Representa uma conexão entre componentes.

```python
class Conexao:
    origem: str            # "componente.pino"
    destino: str           # "componente.pino"
```

#### `CircuitoState`

Gerencia o estado global do circuito.

```python
class CircuitoState:
    nome: str              # Nome do circuito
    portas: dict           # {nome: Porta}
    entradas: dict         # {nome: Entrada}
    saidas: dict           # {nome: Saida}
    conexoes: list         # [Conexao, ...]
```

---

## ⚡ Simulador

O módulo `simulator.py` implementa a lógica de simulação do circuito.

### Algoritmo de Simulação

```
1. VALIDAR estrutura do circuito
   - Verificar se todas as conexões são válidas
   - Verificar se todas as entradas das portas estão conectadas

2. RESETAR estado das portas
   - Limpar valores de entrada e saída
   - Marcar como não processadas

3. PROPAGAR sinais das entradas
   - Para cada entrada do circuito
   - Propagar seu valor para os componentes conectados

4. SIMULAR portas (iterativo)
   - Enquanto houver progresso:
     - Para cada porta não processada:
       - Se todas as entradas estão conectadas:
         - Avaliar usando tabela verdade
         - Propagar resultado
         - Marcar como processada

5. VERIFICAR resultados
   - Alertar sobre portas não processadas
   - Exibir valores das saídas
```

### Propagação de Sinais

```
propagar_sinal(componente, pino, valor):
    origem = "componente.pino"
    
    para cada conexão do circuito:
        se conexão.origem == origem:
            destino = conexão.destino
            
            se destino é porta:
                porta.entrada[índice] = valor
            
            se destino é saída:
                saída.valor = valor
```

### Avaliação de Porta

```
avaliar_porta(porta):
    se não todas_entradas_conectadas:
        retorna None
    
    para cada (entrada, saída) na tabela_verdade:
        se porta.valores_entradas == entrada:
            retorna saída
    
    retorna 0 (fallback)
```

---

## 📊 Geradores de Saída

O módulo `generators.py` produz os relatórios finais.

### Relatório HTML

Gera um arquivo HTML completo com:

- **Cabeçalho**: Nome do circuito
- **Seção Entradas**: Lista de entradas com valores
- **Seção Portas**: Lista de portas com estados
- **Seção Saídas**: Resultados finais
- **Seção Conexões**: Diagrama de conexões
- **Tabela Verdade**: Todas as combinações possíveis (até 4 entradas)

### Estilização

O HTML gerado inclui CSS inline com:
- Design responsivo
- Cores diferenciadas por tipo de componente
- Tabelas formatadas
- Layout em container centralizado

### Resumo Textual

Gera um arquivo TXT simples com:
- Lista de componentes
- Estados atuais
- Conexões definidas

---

## 📚 Exemplos

### 1. Porta AND

**Arquivo**: `exemplos/circuito_and.txt`

```
circuito CircuitoAND {
    entrada A {
        valor_inicial 1
    }

    entrada B {
        valor_inicial 1
    }

    porta_logica AND porta_and {
        numero_de_entradas 2
        numero_de_saidas 1
        tabela_verdade {
            0 0 -> 0
            0 1 -> 0
            1 0 -> 0
            1 1 -> 1
        }
    }

    saida S {
    }

    conexao conectar A.saida -> porta_and.entrada0
    conexao conectar B.saida -> porta_and.entrada1
    conexao conectar porta_and.saida -> S.entrada
}
```

**Resultado**: `A=1, B=1 → S=1`

**Tabela Verdade**:
| A | B | S |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

---

### 2. Porta OR

**Arquivo**: `exemplos/circuito_or.txt`

```
circuito CircuitoOR {
    entrada A {
        valor_inicial 0
    }

    entrada B {
        valor_inicial 1
    }

    porta_logica OR porta_or {
        numero_de_entradas 2
        numero_de_saidas 1
        tabela_verdade {
            0 0 -> 0
            0 1 -> 1
            1 0 -> 1
            1 1 -> 1
        }
    }

    saida S {
    }

    conexao conectar A.saida -> porta_or.entrada0
    conexao conectar B.saida -> porta_or.entrada1
    conexao conectar porta_or.saida -> S.entrada
}
```

**Resultado**: `A=0, B=1 → S=1`

**Tabela Verdade**:
| A | B | S |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 1 |

---

### 3. Porta NOT (Inversor)

**Arquivo**: `exemplos/circuito_not.txt`

```
circuito CircuitoNOT {
    entrada A {
        valor_inicial 1
    }

    porta_logica NOT inversor {
        numero_de_entradas 1
        numero_de_saidas 1
        tabela_verdade {
            0 -> 1
            1 -> 0
        }
    }

    saida S {
    }

    conexao conectar A.saida -> inversor.entrada0
    conexao conectar inversor.saida -> S.entrada
}
```

**Resultado**: `A=1 → S=0`

**Tabela Verdade**:
| A | S |
|---|---|
| 0 | 1 |
| 1 | 0 |

---

### 4. Circuito Complexo: (A AND B) OR (NOT C)

**Arquivo**: `exemplos/circuito_complexo.txt`

```
circuito CircuitoComplexo {
    entrada A {
        valor_inicial 1
    }

    entrada B {
        valor_inicial 0
    }

    entrada C {
        valor_inicial 0
    }

    porta_logica AND porta_and {
        numero_de_entradas 2
        numero_de_saidas 1
        tabela_verdade {
            0 0 -> 0
            0 1 -> 0
            1 0 -> 0
            1 1 -> 1
        }
    }

    porta_logica NOT porta_not {
        numero_de_entradas 1
        numero_de_saidas 1
        tabela_verdade {
            0 -> 1
            1 -> 0
        }
    }

    porta_logica OR porta_or {
        numero_de_entradas 2
        numero_de_saidas 1
        tabela_verdade {
            0 0 -> 0
            0 1 -> 1
            1 0 -> 1
            1 1 -> 1
        }
    }

    saida resultado {
    }

    conexao conectar A.saida -> porta_and.entrada0
    conexao conectar B.saida -> porta_and.entrada1
    conexao conectar C.saida -> porta_not.entrada0
    conexao conectar porta_and.saida -> porta_or.entrada0
    conexao conectar porta_not.saida -> porta_or.entrada1
    conexao conectar porta_or.saida -> resultado.entrada
}
```

**Diagrama do Circuito**:
```
    A ──┐
        ├── AND ──┐
    B ──┘         │
                  ├── OR ── resultado
    C ── NOT ─────┘
```

**Resultado**: `A=1, B=0, C=0 → resultado=1`

**Explicação**: `(1 AND 0) OR (NOT 0) = 0 OR 1 = 1`

**Tabela Verdade Completa**:
| A | B | C | resultado |
|---|---|---|-----------|
| 0 | 0 | 0 | 1 |
| 0 | 0 | 1 | 0 |
| 0 | 1 | 0 | 1 |
| 0 | 1 | 1 | 0 |
| 1 | 0 | 0 | 1 |
| 1 | 0 | 1 | 0 |
| 1 | 1 | 0 | 1 |
| 1 | 1 | 1 | 1 |

---

## 📖 Referência Técnica

### Erros Comuns

| Erro | Causa | Solução |
|------|-------|---------|
| Erro léxico | Caractere inválido | Verificar caracteres especiais |
| Erro sintático | Estrutura incorreta | Verificar sintaxe da linguagem |
| Componente não existe | Conexão para componente inexistente | Definir componente antes de conectar |
| Entradas não conectadas | Porta com entradas sem conexão | Conectar todas as entradas |

### Limitações

- Tabela verdade gerada apenas para circuitos com até 4 entradas
- Apenas portas com uma saída são suportadas na simulação atual
- Não há suporte para loops ou realimentação

### Extensões Possíveis

- [ ] Suporte a portas com múltiplas saídas
- [ ] Simulação temporal com delays
- [ ] Editor visual de circuitos
- [ ] Exportação para VHDL/Verilog
- [ ] Detecção de loops infinitos

---

## 👥 Autores

Desenvolvido como trabalho da disciplina de **Compiladores**.

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
