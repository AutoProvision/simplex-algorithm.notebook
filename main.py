from pulp import *

CLIENTES = [
	{
		'modalidade': 'Capital de giro',
		'propostas_recebidas': 2051,
		'taxa_juros': 2.13,
	},
	{
		'modalidade': 'Cheque Especial',
		'propostas_recebidas': 2242,
		'taxa_juros': 8.16,
	},
	{
		'modalidade': 'Crédito Pessoal',
		'propostas_recebidas': 1982,
		'taxa_juros': 6.43,
	},
	{
		'modalidade': 'Crédito Pessoal Consignado',
		'propostas_recebidas': 218,
		'taxa_juros': 2.36,
	},
	{
		'modalidade': 'Financiamento Imobiliário',
		'propostas_recebidas': 1802,
		'taxa_juros': 0.81,
	},
	{
		'modalidade': 'Aquisição de veículos',
		'propostas_recebidas': 1802,
		'taxa_juros': 1.86,
	},
]

problema = LpProblem('Maximizar_Lucro_Implementacao_Gradual', LpMaximize)

QntClientesCapitalDeGiro = LpVariable('Capital_de_giro', lowBound=0)
QntClientesChequeEspecial = LpVariable('Cheque_Especial', lowBound=0)
QntClientesCreditoPessoal = LpVariable('Crédito_Pessoal', lowBound=0)
QntClientesCreditoPessoalConsignado = LpVariable('Crédito_Pessoal_Consignado', lowBound=0)
QntClientesFinanciamentoImobiliario = LpVariable('Financiamento_Imobiliário', lowBound=0)
QntClientesAquisicaoDeVeiculos = LpVariable('Aquisição_de_veículos', lowBound=0)

variaveisQnt = {
	'Capital de giro': QntClientesCapitalDeGiro,
	'Cheque Especial': QntClientesChequeEspecial,
	'Crédito Pessoal': QntClientesCreditoPessoal,
	'Crédito Pessoal Consignado': QntClientesCreditoPessoalConsignado,
	'Financiamento Imobiliário': QntClientesFinanciamentoImobiliario,
	'Aquisição de veículos': QntClientesAquisicaoDeVeiculos,
}


#### Calculando o lucro gerado por cada modalidade a partir da quantidade escolhida de clientes

problema += lpSum(
	(C['taxa_juros'] * variaveisQnt[C['modalidade']])
	for C in CLIENTES
)

#### Restringindo por quantidade máxima de clientes

MAX_CLIENTES_TRIMESTRE = 6000

problema += lpSum(variaveisQnt.values()) <= MAX_CLIENTES_TRIMESTRE

#### Restringindo por total de número de clientes interessados

for i in range(len(CLIENTES)):
	C = CLIENTES[i]
	V = variaveisQnt[C['modalidade']]
	problema += V <= C['propostas_recebidas']

#### Restringindo a quantidade de clientes de Cheque Especial, para evitar tantos problemas logo no começo

problema += QntClientesChequeEspecial <= 1000

## Resolvendo a otimização

problema.solve()

for C in CLIENTES:
	print(f"{C['modalidade']}: {variaveisQnt[C['modalidade']].varValue}")
