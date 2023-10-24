# Valores originales
valores_originales = [0.008, 0.012, 0.02, 0.012, 0.018, 0.03, 0.02, 0.03, 0.05, 0.012, 0.018, 0.03, 0.018, 0.027, 0.045, 0.03, 0.045, 0.075, 0.02, 0.03, 0.05, 0.03, 0.045, 0.075, 0.05, 0.075, 0.125]

# Crear una lista de tuplas (símbolo, valor original)
tuplas = [(f'r{i}', valor) for i, valor in enumerate(valores_originales)]

# Ordenar la lista de tuplas por el valor original (segundo elemento de la tupla)
tuplas_ordenadas = sorted(tuplas, key=lambda x: x[1], reverse=True)

# Imprimir la lista ordenada
for simbolo, valor in tuplas_ordenadas:
    print(f'{simbolo}: {valor}')
