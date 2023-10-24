import cv2
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import random
import string
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import Button, Tk

def calculate_entropy(image):
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])
    hist = hist / float(hist.sum() + 1e-6)
    entropy = -np.sum(hist * np.log2(hist + 1e-6))
    return entropy

def generate_all_symbols(frame, use_pca=True, use_kmeans=True):
    symbols = []

    if use_pca:
        pca = PCA(n_components=3)
        pixels_flattened = frame.reshape((-1, 3))
        reduced_pixels = pca.fit_transform(pixels_flattened)
        for pixel in reduced_pixels:
            compact_color = tuple(pixel.astype(int) // 32)
            symbols.append(compact_color)
    elif use_kmeans:
        pixels_flattened = frame.reshape((-1, 3))
        kmeans = KMeans(n_clusters=10)
        labels = kmeans.fit_predict(pixels_flattened)
        for label in labels:
            symbols.append(str(label))
    else:
        for row in frame:
            for pixel in row:
                symbol = random.choice(string.ascii_letters + string.digits + string.punctuation)
                symbols.append(str(symbol))

    return symbols

def generate_plot():
    plt.plot(df_entropy['Frame'], df_entropy['Entropía'])
    plt.xlabel('Frame')
    plt.ylabel('Entropía')
    plt.title('Entropía a lo largo del tiempo')
    plt.show()

# Nombre del archivo de video
video_path = '5seg.mp4'

# Abre el video
cap = cv2.VideoCapture(video_path)

# Inicializa diccionarios para almacenar la cuenta de cada símbolo y la entropía
symbol_counts_dict = {}
entropy_dict = {}

# Lee los fotogramas del video
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
current_frame = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    entropy = calculate_entropy(gray)
    print(f'Entropía para el frame {current_frame + 1}: {entropy}')

    entropy_dict[current_frame] = entropy

    all_symbols = generate_all_symbols(frame, use_pca=True, use_kmeans=True)

    for symbol in all_symbols:
        symbol_key = str(symbol)
        if symbol_key in symbol_counts_dict:
            symbol_counts_dict[symbol_key] += 1
        else:
            symbol_counts_dict[symbol_key] = 1

    current_frame += 1
    print(f'Frames procesados: {current_frame}/{total_frames}')

cap.release()

# Crear un DataFrame con los resultados del diccionario original
df_symbols_original = pd.DataFrame(list(symbol_counts_dict.items()), columns=['Símbolo', 'Cantidad'])

# Crear un DataFrame con los resultados del diccionario de entropía
df_entropy = pd.DataFrame(list(entropy_dict.items()), columns=['Frame', 'Entropía'])

'''
# Mostrar el DataFrame del diccionario original
print("\nDataFrame de Símbolos Originales:")
print(df_symbols_original)
'''

# Mostrar el DataFrame de entropía
print("\nDataFrame de Entropía:")
print(df_entropy)

# Crear una copia del diccionario con símbolos aleatorios
diccionario_copia = dict()
for clave, valor in symbol_counts_dict.items():
    nuevo_simbolo = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(3))
    diccionario_copia[nuevo_simbolo] = valor

# Generar un DataFrame con los resultados de la copia del diccionario
df_symbols_copia = pd.DataFrame(sorted(diccionario_copia.items()), columns=['Símbolo', 'Cantidad'])

# Mostrar el DataFrame final de la copia del diccionario
print("\nDataFrame de Símbolos de la Copia:")
print(df_symbols_copia)

# Crear la interfaz gráfica
root = Tk()
root.title('Entropía a lo largo del tiempo')

# Agregar botón para generar gráfica
button_plot = Button(root, text='Generar Gráfica de Entropía', command=generate_plot)
button_plot.pack()

# Agregar el lienzo para la gráfica
figure = plt.Figure(figsize=(6, 4), dpi=100)
plot_canvas = FigureCanvasTkAgg(figure, master=root)
plot_canvas.get_tk_widget().pack()

# Mostrar la interfaz gráfica
root.mainloop()
