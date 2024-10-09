import pulp

# Dados de entrada
modalidades = [
    {'modalidade': 'Capital de giro', 'propostas_recebidas': 251, 'valor_medio_retirado': 500000, 'taxa_juros': 2.13},
    {'modalidade': 'Cheque Especial', 'propostas_recebidas': 2242, 'valor_medio_retirado': 200000, 'taxa_juros': 8.16},
]

# Variáveis de decisão: quantidade de propostas aceitas para cada modalidade
propostas_vars = [pulp.LpVariable(f"propostas_{mod['modalidade'].replace(' ', '_')}", 0, mod['propostas_recebidas'], cat='Integer') for mod in modalidades]

# Criar o problema de maximização
modelo = pulp.LpProblem("Maximizar_Lucro", pulp.LpMaximize)

# Função objetivo: Maximizar o lucro com base nas propostas aceitas e taxa de juros
modelo += pulp.lpSum([propostas_vars[i] * modalidades[i]['valor_medio_retirado'] * (modalidades[i]['taxa_juros'] / 100) for i in range(len(modalidades))])

# Restrições normalizadas
# Limitar propostas recebidas (proporcionalmente ao total)
max_total_propostas = 2000
max_total_valor_medio = 80000000

# Normalização proporcional para cada modalidade
modelo += pulp.lpSum([propostas_vars[i] / modalidades[i]['propostas_recebidas'] for i in range(len(modalidades))]) <= max_total_propostas / sum([mod['propostas_recebidas'] for mod in modalidades]), "Limite_Total_Propostas_Normalizado"

# Limitar valor retirado total (proporcionalmente ao valor máximo permitido)
modelo += pulp.lpSum([propostas_vars[i] * modalidades[i]['valor_medio_retirado'] for i in range(len(modalidades))]) <= max_total_valor_medio, "Limite_Total_Valor_Medio_Retirado"

# Resolver o problema
modelo.solve()

# Resultado
print("Status:", pulp.LpStatus[modelo.status])

for i, var in enumerate(propostas_vars):
    print(f"{modalidades[i]['modalidade']}: {var.varValue} propostas aceitas")

# Lucro total
print("Lucro total maximizado:", pulp.value(modelo.objective))