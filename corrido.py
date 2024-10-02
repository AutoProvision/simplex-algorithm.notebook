from pulp import *

perfis = [
	{
		"nome": "Aposentados",
		"propostas_recebidas": 2000,
		"taxa_inadimplencia": 0.04,
		"taxa_juros": 0.015
	},
	{
		"nome": "Pensionistas",
		"propostas_recebidas": 1242,
		"taxa_inadimplencia": 0.11,
		"taxa_juros": 0.02
	},
	{
		"nome": "PJ",
		"propostas_recebidas": 3982,
		"taxa_inadimplencia": 0.06,
		"taxa_juros": 0.03
	},
	{
		"nome": "CLT",
		"propostas_recebidas": 218,
		"taxa_inadimplencia": 0.08,
		"taxa_juros": 0.025
	},
	{
		"nome": "Funcionários internos",
		"propostas_recebidas": 1802,
		"taxa_inadimplencia": 0.00,
		"taxa_juros": 0.01
	}
]

max_clientes = 5000


problema = LpProblem('Maximizar_Lucro', LpMaximize)

variaveis = LpVariable.dicts('Propostas', [perfil['nome'] for perfil in perfis], lowBound=0)

problema += lpSum(
    (1 - perfil['taxa_inadimplencia']) * perfil['taxa_juros'] * variaveis[perfil['nome']]
    for perfil in perfis
)

problema += lpSum(variaveis) <= max_clientes

for perfil in perfis:
    problema += variaveis[perfil['nome']] <= perfil['propostas_recebidas']

problema.solve()

for perfil in perfis:
    print(f"{perfil['nome']} = {variaveis[perfil['nome']].varValue}")
