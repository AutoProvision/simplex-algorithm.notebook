from pulp import *

modelo = LpProblem('Maximizar_Lucro_Implementacao_Gradual', LpMaximize)

x1 = LpVariable('Qnt_Clientes_Capital_de_Giro', lowBound=0)
x2 = LpVariable('Qnt_Clientes_Cheque_Especial', lowBound=0)
x3 = LpVariable('Qnt_Clientes_Crédito_Pessoal', lowBound=0)
x4 = LpVariable('Qnt_Clientes_Crédito_Pessoal_Consignado', lowBound=0)
x5 = LpVariable('Qnt_Clientes_Financiamento_Imobiliário', lowBound=0)
x6 = LpVariable('Qnt_Clientes_Aquisição_de_Veículos', lowBound=0)

modelo +=\
	(2.13 / 100 * 18_000 * x1) +\
	(8.16 / 100 * 10_000 * x2) +\
	(6.43 / 100 * 15_000 * x3) +\
	(2.36 / 100 * 12_500 * x4) +\
	(0.81 / 100 * 13_425 * x5) +\
	(1.86 / 100 * 8_500 * x6), 'Lucro_Total'

MAXIMO_CLIENTES = 6_000
CAPITAL_MAXIMO = 125_000_000

modelo += x1 + x2 + x3 + x4 + x5 + x6 <= MAXIMO_CLIENTES, 'Total_de_Clientes_Processados'

modelo += x1 <= 1400, 'Máximo de clientes para Capital de Giro'
modelo += x2 <= 600, 'Máximo de clientes para Cheque Especial'
modelo += x3 <= 1600, 'Máximo de clientes para Crédito Pessoal'
modelo += x4 <= 6000, 'Máximo de clientes para Crédito Pessoal Consignado'
modelo += x5 <= 3400, 'Máximo de clientes para Financiamento Imobiliário'
modelo += x6 <= 3400, 'Máximo de clientes para Aquisição de Veículos'

modelo +=\
	18_000 * x1 +\
	10_000 * x2 +\
	15_000 * x3 +\
	12_500 * x4 +\
	13_425 * x5 +\
	8_500 * x6 <= CAPITAL_MAXIMO, 'Capital_Total_Disponível'

modelo +=\
	x1 >= 400,'Mínimo de clientes de Capital de Giro' +\
	x2 >= 400, 'Mínimo de clientes de Cheque Especial' +\
	x3 >= 400, 'Mínimo de clientes de Crédito Pessoal' +\
	x4 >= 400, 'Mínimo de clientes de Crédito Pessoal Consignado' +\
	x5 >= 400, 'Mínimo de clientes de Financiamento Imobiliário' +\
	x6 >= 400, 'Mínimo de clientes de Aquisição de Veículos'

modelo.solve(PULP_CBC_CMD(msg=False))

print(f"Clientes de Capital de Giro (x1): {x1.varValue}")
print(f"Clientes de Cheque Especial (x2): {x2.varValue}")
print(f"Clientes de Crédito Pessoal (x3): {x3.varValue}")
print(f"Clientes de Crédito Pessoal Consignado (x4): {x4.varValue}")
print(f"Clientes de Financiamento Imobiliário (x5): {x5.varValue}")
print(f"Clientes de Aquisição de Veículos (x6): {x6.varValue}")
print(f"Lucro Total: {modelo.objective.value()}")
