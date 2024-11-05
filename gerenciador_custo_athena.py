import tkinter as tk
import pulp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

def resolver_modelo(custo_total_limite):
    modelo = pulp.LpProblem("distribuir_custo", pulp.LpMinimize)

    custo = {nome: pulp.LpVariable(f"custo_{nome}", lowBound=0) for nome in cenarios}

    modelo += pulp.lpSum(custo[nome] for nome in cenarios), "Custo Total"

    for nome, dados in cenarios.items():
        demanda = dados["demanda"]
        quantidade_gb = dados["dados_verificacao_gb"]
        modelo += custo[nome] == ((demanda * quantidade_gb) / 1024) * 5, f"Custo_{nome}"

    modelo += pulp.lpSum(custo[nome] for nome in cenarios) <= custo_total_limite, "Custo Total Limite"

    modelo.solve()

    custo_resultado = []
    for nome in cenarios:
        custo_valor = custo[nome].varValue if custo[nome].varValue else 0
        custo_resultado.append(custo_valor)

    return custo_resultado, modelo.objective.value()

def atualizar_interface(custo_total_limite, demanda_atualizada):
    for idx, nome in enumerate(cenarios):
        cenarios[nome]["demanda"] = demanda_atualizada[idx]
    
    custo_resultado, custo_total_minimo = resolver_modelo(custo_total_limite)

    ax.clear()

    if custo_total_minimo > custo_total_limite:
        ax.text(0.5, 0.5, "Solução Não Viável (Custo Excede o Limite)", ha='center', va='center', fontsize=14, color='red')
    else:
        ax.bar(cenarios.keys(), custo_resultado, color='skyblue')
        ax.set_xlabel('Cenários')
        ax.set_ylabel('Custo Total ($)')
        ax.set_title(f'Distribuição de Custos por Cenário\nCusto Total: ${custo_total_minimo:.4f}')
        ax.set_xticklabels(cenarios.keys(), rotation=45, ha='right')

    custo_label.config(text=f"Custo Total Limite: ${custo_total_limite:.4f}")
    resultado_label.config(text=f"Custo Total Mínimo: ${custo_total_minimo:.4f}")

    canvas.draw()

def criar_sliders_demanda():
    sliders = {}
    for nome, dados in cenarios.items():
        demanda_slider = tk.Scale(inner_frame, from_=0, to=500, orient="horizontal", resolution=1, length=500,
                                  label=f"{nome} Demanda", command=lambda val, nome=nome: atualizar_demanda(val, nome))
        demanda_slider.set(dados["demanda"])
        demanda_slider.pack(pady=10)
        sliders[nome] = demanda_slider
    return sliders

def atualizar_demanda(val, nome):
    cenarios[nome]["demanda"] = int(val)
    atualizar_interface(slider_custo_total_limite.get(), [cenarios[n]["demanda"] for n in cenarios])

root = tk.Tk()
root.title("Otimização de Custos")

canvas_root = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas_root.yview)
canvas_root.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas_root.pack(side="left", fill="both", expand=True)

inner_frame = tk.Frame(canvas_root)
canvas_root.create_window((0, 0), window=inner_frame, anchor="nw")

inner_frame.bind("<Configure>", lambda e: canvas_root.configure(scrollregion=canvas_root.bbox("all")))

custo_label = tk.Label(inner_frame, text="Custo Total Limite: $3.0000", font=("Arial", 12))
custo_label.pack(pady=10)

resultado_label = tk.Label(inner_frame, text="Custo Total Mínimo: $0.0000", font=("Arial", 12))
resultado_label.pack(pady=10)

slider_custo_total_limite = tk.Scale(inner_frame, from_=0.1, to=5.0, orient="horizontal", resolution=0.01, length=500,
                                     command=lambda val: atualizar_interface(float(val), [cenarios[n]["demanda"] for n in cenarios]))
slider_custo_total_limite.set(3.0)
slider_custo_total_limite.pack(pady=20)

sliders_demanda = criar_sliders_demanda()

fig, ax = plt.subplots(figsize=(10, 6))

canvas = FigureCanvasTkAgg(fig, master=inner_frame)
canvas.get_tk_widget().pack()

atualizar_interface(3.0, [cenarios[n]["demanda"] for n in cenarios])

root.mainloop()
