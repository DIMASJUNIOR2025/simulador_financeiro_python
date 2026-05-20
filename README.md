# 💰 Simulador Financeiro com IOF

> Ferramenta interativa para simulação de financiamentos com cálculo automático de IOF, comparação entre sistemas de amortização PRICE e SAC, e visualização gráfica da evolução da dívida. Desenvolvida para Jupyter Notebook com interface moderna via `ipywidgets`.

---

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [Cálculos e Fórmulas](#cálculos-e-fórmulas)
- [Interface](#interface)
- [Estrutura do Código](#estrutura-do-código)
- [Exemplos de Uso](#exemplos-de-uso)
- [Limitações Conhecidas](#limitações-conhecidas)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)

---

## 🔍 Visão Geral

O **Simulador Financeiro com IOF** é um notebook interativo que permite simular operações de crédito levando em conta o Imposto sobre Operações Financeiras (IOF). O usuário informa o capital desejado, a taxa de juros, o prazo e o período de carência, e o simulador retorna automaticamente a comparação entre as duas principais modalidades de amortização do mercado brasileiro: **Tabela PRICE** e **Sistema SAC**.

---

## ✨ Funcionalidades

- **Cálculo de IOF** com alíquotas fixa e diária conforme legislação vigente
- **Comparação PRICE vs SAC** com totais pagos e parcelas estimadas
- **Período de carência** configurável de 0 a 12 meses
- **Gráfico interativo** de evolução da dívida ao longo do tempo
- **Interface visual** com tema escuro via CSS customizado
- **Botão de limpeza** para reset rápido dos campos
- **Tabela comparativa** em `pandas.DataFrame` exibida inline

---

## 📦 Pré-requisitos

- Python **3.8+**
- Jupyter Notebook ou JupyterLab
- Conexão com internet (para carregar a imagem de fundo via Pexels)

---

## ⚙️ Instalação

**1. Clone o repositório ou faça download do notebook:**

```bash
git clone https://github.com/seu-usuario/simulador-financeiro-iof.git
cd simulador-financeiro-iof
```

**2. Instale as dependências:**

```bash
pip install ipywidgets pandas matplotlib numpy notebook
```

**3. Ative a extensão de widgets no Jupyter (se necessário):**

```bash
jupyter nbextension enable --py widgetsnbextension
```

Para JupyterLab:

```bash
jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

**4. Execute o notebook:**

```bash
jupyter notebook simulador_financeiro.ipynb
```

---

## 🚀 Como Usar

1. Abra o notebook no Jupyter e execute a célula principal com `Shift + Enter`
2. Preencha os campos da interface:

| Campo | Descrição | Exemplo |
|---|---|---|
| **Capital (R$)** | Valor total do financiamento | `50000` |
| **Taxa (%)** | Taxa de juros **anual** em percentual | `12.5` |
| **Meses** | Prazo total em meses | `36` |
| **Carência** | Meses de carência antes da amortização | `3` |

3. Clique em **CALCULAR COM IOF** para ver os resultados
4. Navegue entre as abas **Resultados** e **Gráfico**
5. Clique em **LIMPAR** para resetar todos os campos

---

## 📐 Cálculos e Fórmulas

### IOF (Imposto sobre Operações Financeiras)

O IOF é calculado com base em duas alíquotas somadas:

```
IOF_fixo  = Principal × 0,38%
IOF_diário = Principal × (0,0082% × dias)   [limitado a 3% do principal]
Dias       = min(meses × 30, 365)

IOF_total  = IOF_fixo + IOF_diário
```

### Taxa Mensal Equivalente

Conversão da taxa anual nominal para mensal equivalente pelo regime de juros compostos:

```
taxa_mensal = (1 + taxa_anual)^(1/12) - 1
```

### Tabela PRICE (Parcelas Fixas)

Com carência aplicada ao saldo devedor antes do início das parcelas:

```
Saldo_pós_carência = Principal × (1 + taxa)^carência

PMT = Saldo × [ taxa × (1 + taxa)^n ] / [ (1 + taxa)^n - 1 ]
```

### Sistema SAC (Amortização Constante)

```
Amortização_fixa  = Saldo_pós_carência / n
Parcela_i         = (Saldo - (i × Amortização)) × taxa + Amortização
Total_pago        = Σ Parcela_i  para i = 0 até n-1
```

> Em ambos os sistemas, o IOF é somado ao valor principal antes dos cálculos de parcela.

---

## 🖥️ Interface

A interface é construída com `ipywidgets` e estilizada com CSS injetado via `IPython.display.HTML`:

```
┌──────────────────────────────────────────┐
│     💰 Simulador Financeiro com IOF      │
├──────────────────────────────────────────┤
│  Capital (R$):   [___________________]   │
│  Taxa (%):       [___________________]   │
│  Meses:          [___________________]   │
│  Carência:       [====|_____]  (slider)  │
│                                          │
│  [     CALCULAR COM IOF     ]            │
│  [          LIMPAR          ]            │
├───────────────┬──────────────────────────┤
│  Resultados   │  Gráfico                 │
│               │                          │
│  IOF: R$ ...  │  📈 Evolução da Dívida   │
│  PRICE: R$... │                          │
│  SAC:   R$... │                          │
│  Tabela DF    │                          │
└───────────────┴──────────────────────────┘
```

**Paleta de cores:**

| Elemento | Cor |
|---|---|
| Destaque / títulos | `#50fa7b` (verde neon) |
| Fundo principal | `#2d2d2d` (cinza escuro) |
| Texto | `#f8f8f2` (branco suave) |
| Botão limpar | `#ff5555` (vermelho) |

---

## 🗂️ Estrutura do Código

```
simulador_financeiro.ipynb
│
├── Funções de Cálculo
│   ├── calcular_iof(valor, meses)
│   ├── taxa_mensal_equivalente(taxa_anual)
│   ├── juros_compostos(principal, taxa, tempo)
│   ├── tabela_price(valor, taxa, meses, carencia)
│   └── comparar_amortizacao(valor, taxa, meses, carencia)
│
├── Estilo CSS (style_html)
│
├── Componentes de Interface (ipywidgets)
│   ├── valor_input, taxa_input, tempo_input
│   ├── carencia_input (slider)
│   ├── calcular_btn, limpar_btn
│   ├── output_resumo, output_grafico
│   └── tabs (Resultados | Gráfico)
│
└── Handlers de Eventos
    ├── atualizar_dashboard(b)
    └── limpar_campos(b)
```

---

## 💡 Exemplos de Uso

**Exemplo 1 — Financiamento de veículo:**

| Parâmetro | Valor |
|---|---|
| Capital | R$ 45.000,00 |
| Taxa anual | 18% |
| Prazo | 48 meses |
| Carência | 0 meses |

**Resultado esperado:**
- IOF estimado: ≈ R$ 1.575,00
- Parcela PRICE (fixa): ≈ R$ 1.350,00/mês
- Parcela SAC (1ª): ≈ R$ 1.720,00/mês
- Total PRICE < Total SAC nas primeiras parcelas, mas SAC é mais barato no total

---

**Exemplo 2 — Crédito pessoal com carência:**

| Parâmetro | Valor |
|---|---|
| Capital | R$ 10.000,00 |
| Taxa anual | 24% |
| Prazo | 12 meses |
| Carência | 2 meses |

---

## ⚠️ Limitações Conhecidas

- A taxa informada é tratada como **taxa anual** e convertida internamente para mensal. Certifique-se de inserir o valor correto.
- O cálculo de IOF segue a lógica simplificada prevista na legislação vigente, podendo haver pequenas variações dependendo do tipo de operação financeira e do contrato específico.
- A imagem de fundo da interface depende de conexão com internet (Pexels). Em ambientes offline, o fundo será exibido como cor sólida.
- O gráfico exibe a **evolução bruta dos juros compostos**, não o saldo devedor residual parcelado — serve como referência visual de crescimento exponencial da dívida sem amortização.

---

## 🛠️ Tecnologias Utilizadas

| Biblioteca | Versão mínima | Uso |
|---|---|---|
| `ipywidgets` | 7.x | Interface interativa no Jupyter |
| `pandas` | 1.x | Tabela comparativa de resultados |
| `matplotlib` | 3.x | Gráfico de evolução da dívida |
| `numpy` | 1.x | Vetor de eixo X do gráfico |
| `IPython` | — | Exibição de HTML e limpeza de output |

---

## 📄 Licença

Distribuído sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.

---

*Desenvolvido para fins educacionais e de simulação. Não substitui a análise de um profissional financeiro.*
