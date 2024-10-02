def juros_anual_p_mensal(taxa_anual, periodo_desejado, periodo_atual):
    a = 1 + (taxa_anual / 100)
    b = periodo_desejado/periodo_atual
    c = round(a**b, 4)
    d = c - 1
    e = round(d * 100, 2)
    return e

print(juros_anual_p_mensal(0.8499999999999952, 12, 1))