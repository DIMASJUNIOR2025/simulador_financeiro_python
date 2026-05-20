import ipywidgets as widgets
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import display, clear_output, HTML

# --- Funções de Cálculo ---
def calcular_iof(valor, meses):
    if not valor or not meses: return 0
    aliquota_fixa = 0.0038
    aliquota_diaria = 0.000082
    dias = min(meses * 30, 365)
    iof_fixo = valor * aliquota_fixa
    iof_diario = valor * (aliquota_diaria * dias)
    iof_diario = min(iof_diario, valor * 0.03)
    return iof_fixo + iof_diario

def taxa_mensal_equivalente(taxa_anual):
    return ((1 + taxa_anual)**(1/12)) - 1

def juros_compostos(principal, taxa, tempo):
    return principal * (1 + taxa)**tempo

def tabela_price(valor, taxa, meses, carencia=0):
    valor_pos_carencia = valor * (1 + taxa)**carencia
    if taxa == 0: return valor_pos_carencia / meses
    return valor_pos_carencia * (taxa * (1 + taxa)**meses) / ((1 + taxa)**meses - 1)

def comparar_amortizacao(valor, taxa, meses, carencia=0):
    iof = calcular_iof(valor, meses)
    valor_total_financiado = valor + iof
    pmt_price = tabela_price(valor_total_financiado, taxa, meses, carencia)
    total_price = pmt_price * meses
    valor_pos_carencia = valor_total_financiado * (1 + taxa)**carencia
    amort_sac = valor_pos_carencia / meses
    primeira_sac = (valor_pos_carencia * taxa) + amort_sac
    total_sac = sum([(valor_pos_carencia - (i * amort_sac)) * taxa + amort_sac for i in range(meses)])
    df = pd.DataFrame({
        'Sistema': ['PRICE', 'SAC'],
        'IOF Estimado': [f'R$ {iof:,.2f}', f'R$ {iof:,.2f}'],
        'Parcela': [f'R$ {pmt_price:,.2f} (Fixa)', f'R$ {primeira_sac:,.2f} (Inicial)'],
        'Total Pago': [f'R$ {total_price:,.2f}', f'R$ {total_sac:,.2f}']
    })
    return df, pmt_price, primeira_sac, iof

# --- Interface Moderna Finalizada ---
style_html = """
<style>
    .widget-vbox {
        background-image: linear-gradient(rgba(45, 45, 45, 0.9), rgba(45, 45, 45, 0.9)), url('https://images.pexels.com/photos/36488453/pexels-photo-36488453.jpeg');
        background-size: cover; background-position: center;
        padding: 230px; border-radius: 15px; border: 1px solid #50fa7b;
        margin: 10px auto; max-width: 100%;
    }
    .main-title { color: #50fa7b !important; font-family: 'Segoe UI', sans-serif; text-align: center; font-size: 24px; margin-bottom: 20px; }
    .calc-btn { font-weight: bold !important; background-color: #50fa7b !important; color: #1e1e1e !important; border-radius: 8px !important; margin-top: 10px !important; }
    .clear-btn { font-weight: bold !important; background-color: #ff5555 !important; color: #f8f8f2 !important; border-radius: 8px !important; margin-top: 10px !important; }
    .p-Widget { color: #f8f8f2; }
    .widget-label { color: white !important; }
</style>
"""
display(HTML(style_html))

# --- Componentes ---
valor_input = widgets.FloatText(value=0, description='Capital (R$):')
taxa_input = widgets.FloatText(value=0, description='Taxa (%):')
tempo_input = widgets.IntText(value=0, description='Meses:')
carencia_input = widgets.IntSlider(value=0, min=0, max=12, description='Carência:')
calcular_btn = widgets.Button(description='CALCULAR COM IOF', layout=widgets.Layout(width='100%'))
limpar_btn = widgets.Button(description='LIMPAR', layout=widgets.Layout(width='100%'))
calcular_btn.add_class('calc-btn')
limpar_btn.add_class('clear-btn')

output_resumo = widgets.Output()
output_grafico = widgets.Output()
tabs = widgets.Tab(children=[output_resumo, output_grafico])
tabs.set_title(0, 'Resultados'); tabs.set_title(1, 'Gráfico')

def atualizar_dashboard(b):
    if not valor_input.value or not tempo_input.value:
        with output_resumo: clear_output(); print("Erro: Preencha Capital e Meses.")
        return
    p, r, t, c_m = valor_input.value, taxa_input.value / 100, tempo_input.value, carencia_input.value
    df_amort, pmt_p, pmt_s, iof_val = comparar_amortizacao(p, r, t, c_m)
    with output_resumo: clear_output(); display(HTML(f"<div style='color:#f8f8f2; padding: 15px;'><h3 style='color:#50fa7b;'>Resultados (Total Financiado: R$ {p+iof_val:,.2f})</h3><p><b>• IOF:</b> R$ {iof_val:,.2f}</p><p><b>• Parcela PRICE:</b> R$ {pmt_p:,.2f}</p><p><b>• Parcela SAC (1ª):</b> R$ {pmt_s:,.2f}</p></div>")); display(df_amort)
    with output_grafico: clear_output(); eixo_x = np.arange(0, t + 1); plt.style.use('dark_background'); fig, ax = plt.subplots(figsize=(7, 3)); ax.plot(eixo_x, [juros_compostos(p+iof_val, r, i) for i in eixo_x], color='#50fa7b', marker='o'); ax.set_title("Evolução da Dívida"); plt.show()

def limpar_campos(b):
    valor_input.value, taxa_input.value, tempo_input.value, carencia_input.value = 0, 0, 0, 0
    with output_resumo: clear_output()
    with output_grafico: clear_output()

calcular_btn.on_click(atualizar_dashboard)
limpar_btn.on_click(limpar_campos)

ui = widgets.VBox([widgets.HTML("<h2 class='main-title'>Simulador Financeiro com IOF</h2>"), valor_input, taxa_input, tempo_input, carencia_input, calcular_btn, limpar_btn, tabs])
ui.add_class('widget-vbox')
display(ui)