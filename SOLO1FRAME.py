import cv2
import pandas as pd
import random
import string
import matplotlib.pyplot as plt

def generate_random_symbols(frame):
    symbols = []
    all_printable_characters = string.printable
    for row in frame:
        for pixel in row:
            random_symbol = random.choice(all_printable_characters)
            symbols.append(random_symbol)
    return symbols

# Nombre del archivo de video
video_path = '5seg.mp4'

# Abre el video
cap = cv2.VideoCapture(video_path)

# Lee un solo fotograma
ret, frame = cap.read()

# Inicializa una lista para almacenar todos los símbolos aleatorios
all_symbols_random = generate_random_symbols(frame)

# Convierte los símbolos aleatorios a una lista de cadenas
symbols_list_random = [str(symbol) for symbol in all_symbols_random]

# Crea un DataFrame con los resultados de todos los símbolos aleatorios
df_symbols_random = pd.DataFrame({'Símbolo': symbols_list_random})

# Muestra el DataFrame final con la cuenta de cada símbolo aleatorio
symbol_counts_random = df_symbols_random['Símbolo'].value_counts().reset_index()
symbol_counts_random.columns = ['Símbolo', 'Cantidad']
print("\nDataFrame de Símbolos Aleatorios:")
print(symbol_counts_random)

# Crea una gráfica de barras
plt.figure(figsize=(10, 6))
plt.bar(symbol_counts_random['Símbolo'], symbol_counts_random['Cantidad'])
plt.xlabel('Símbolo')
plt.ylabel('Cantidad')
plt.title('Frecuencia de Símbolos Aleatorios')
plt.xticks(rotation=45, ha='right')  # Ajusta la rotación de las etiquetas del eje x
plt.tight_layout()

# Muestra la gráfica
plt.show()

# Cierra el video y libera recursos
cap.release()
