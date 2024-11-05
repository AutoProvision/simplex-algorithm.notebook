import tkinter as tk
from tkinter import ttk
import pulp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Dados dos cenários
cenarios = {
    "Query 1": {
        "demanda": 200,
        "dados_verificacao_gb": 3.09,
        "tempo_execucao_sec": 180,
        "stmt": 'SELECT * FROM "autoprovision_client"."operacoes_credito";'
    },
    "Query 2": {
        "demanda": 200,
        "dados_verificacao_gb": 0.16,
        "tempo_execucao_sec": 28.46,
        "stmt": 'SELECT * FROM "autoprovision_client"."operacoes_credito" where YEAR(dt_data_base) in (2023,2024);'
    },
    "Query 3": {
        "demanda": 50,
        "dados_verificacao_gb": 0.35,
        "tempo_execucao_sec": 22.08,
        "stmt": 'SELECT * FROM "autoprovision_client"."operacoes_credito" order by dt_data_base desc limit 300000;'
    },
    "Query 4": {
        "demanda": 100,
        "dados_verificacao_gb": 0.35,
        "tempo_execucao_sec": 14.41,
        "stmt": 'SELECT * FROM "autoprovision_client"."operacoes_credito" order by dt_data_base desc limit 300000;'
    },
    "Query 5": {
        "demanda": 150,
        "dados_verificacao_gb": 0.35,
        "tempo_execucao_sec": 26.00,
        "stmt": "SELECT * FROM 'autoprovision_client'.'operacoes_credito' where ct_porte in ('PF - Acima de 20 salários mínimos', 'PJ - Grande', 'PJ - Médio');"
    }
}

# Função para resolver o modelo e gerar os resultados
def resolver_modelo(custo_total_limite):
    # Criando o modelo de otimização (minimizar os custos)
    modelo = pulp.LpProblem("distribuir_custo", pulp.LpMinimize)

    # Definindo as variáveis de custo, um custo para cada cenário, com limite inferior de 0
    custo = {nome: pulp.LpVariable(f"custo_{nome}", lowBound=0) for nome in cenarios}

    # Função objetivo: minimizar o custo total
    modelo += pulp.lpSum(custo[nome] for nome in cenarios), "Custo Total"

    # Equação de custo para cada cenário
    for nome, dados in cenarios.items():
        demanda = dados["demanda"]
        quantidade_gb = dados["dados_verificacao_gb"]
        modelo += custo[nome] == ((demanda * quantidade_gb) / 1024) * 5, f"Custo_{nome}"

    # Restrições:
    modelo += pulp.lpSum(custo[nome] for nome in cenarios) <= custo_total_limite, "Custo Total Limite"

    # Resolvendo o modelo
    modelo.solve()

    # Exibindo os resultados
    custo_resultado = []
    for nome in cenarios:
        custo_valor = custo[nome].varValue if custo[nome].varValue else 0  # Evita erro caso o valor não tenha sido atribuído
        custo_resultado.append(custo_valor)

    # Retorna o resultado e o valor do objetivo (custo total mínimo)
    return custo_resultado, modelo.objective.value()

# Função para atualizar a interface gráfica com os novos resultados
def atualizar_interface(custo_total_limite, demanda_atualizada):
    # Atualizando os dados dos cenários com a demanda do slider
    for idx, nome in enumerate(cenarios):
        cenarios[nome]["demanda"] = demanda_atualizada[idx]
    
    custo_resultado, custo_total_minimo = resolver_modelo(custo_total_limite)

    # Limpa o gráfico anterior
    ax.clear()

    # Verifica se o custo total mínimo excede o limite
    if custo_total_minimo > custo_total_limite:
        # Se exceder, o gráfico fica vazio e exibe uma mensagem
        ax.text(0.5, 0.5, "Solução Não Viável (Custo Excede o Limite)", ha='center', va='center', fontsize=14, color='red')
    else:
        # Caso contrário, exibe o gráfico de barras com os custos
        ax.bar(cenarios.keys(), custo_resultado, color='skyblue')
        ax.set_xlabel('Cenários')
        ax.set_ylabel('Custo Total ($)')
        ax.set_title(f'Distribuição de Custos por Cenário\nCusto Total: ${custo_total_minimo:.4f}')
        ax.set_xticklabels(cenarios.keys(), rotation=45, ha='right')

    # Atualiza a interface com o novo valor de custo total
    custo_label.config(text=f"Custo Total Limite: ${custo_total_limite:.4f}")
    resultado_label.config(text=f"Custo Total Mínimo: ${custo_total_minimo:.4f}")

    canvas.draw()

# Função para criar sliders de demanda para cada cenário
def criar_sliders_demanda():
    sliders = {}
    for nome, dados in cenarios.items():
        demanda_slider = tk.Scale(root, from_=0, to=500, orient="horizontal", resolution=1, length=500,
                                  label=f"{nome} Demanda", command=lambda val, nome=nome: atualizar_demanda(val, nome))
        demanda_slider.set(dados["demanda"])
        demanda_slider.pack(pady=10)
        sliders[nome] = demanda_slider
    return sliders

# Função para atualizar a demanda de um cenário específico
def atualizar_demanda(val, nome):
    cenarios[nome]["demanda"] = int(val)
    atualizar_interface(slider_custo_total_limite.get(), [cenarios[n]["demanda"] for n in cenarios])

# Criando a janela principal
root = tk.Tk()
root.title("Otimização de Custos")

# Label para exibir o valor atual do custo total limite
custo_label = tk.Label(root, text="Custo Total Limite: $3.0000", font=("Arial", 12))
custo_label.pack(pady=10)

# Label para exibir o custo total mínimo após a otimização
resultado_label = tk.Label(root, text="Custo Total Mínimo: $0.0000", font=("Arial", 12))
resultado_label.pack(pady=10)

# Slider para ajustar o custo total limite
slider_custo_total_limite = tk.Scale(root, from_=0.1, to=5.0, orient="horizontal", resolution=0.01, length=500,
                                     command=lambda val: atualizar_interface(float(val), [cenarios[n]["demanda"] for n in cenarios]))
slider_custo_total_limite.set(3.0)  # Valor inicial do slider
slider_custo_total_limite.pack(pady=20)

# Criação de sliders para os cenários
sliders_demanda = criar_sliders_demanda()

# Configurando o gráfico dentro da interface
fig, ax = plt.subplots(figsize=(10, 6))

# Criação do canvas para exibir o gráfico no tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

atualizar_interface(3.0, [cenarios[n]["demanda"] for n in cenarios])

# Iniciar o loop principal da interface
root.mainloop()
