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
from tkinter import Button, Tk, Text

def calculate_entropy(image):
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])
    hist = hist / float(hist.sum() + 1e-6)
    entropy = -np.sum(hist * np.log2(hist + 1e-6))
    return entropy

def encode_to_12_bits(color_symbol):
    if isinstance(color_symbol, str):
        try:
            # Intenta convertir la cadena en una tupla de tres elementos
            color = eval(color_symbol)
            if len(color) == 3:
                r, g, b = color
            else:
                raise ValueError("La tupla de color debe tener exactamente tres elementos")
        except (SyntaxError, ValueError):
            raise ValueError("No se puede evaluar la cadena como una tupla de color")
    elif isinstance(color_symbol, tuple) and len(color_symbol) == 3:
        r, g, b = color_symbol
    else:
        raise ValueError("El símbolo debe ser una cadena o una tupla de tres elementos")

    encoded_value = ((r & 0xF0) << 4) | ((g & 0xF0) << 2) | (b & 0xF0)
    return encoded_value

def decode_from_12_bits(encoded_value):
    r = ((encoded_value >> 8) & 0xF0)
    g = ((encoded_value >> 4) & 0xF0)
    b = (encoded_value & 0xF0)
    return (r, g, b)

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

def show_original_symbols():
    show_dataframe("DataFrame de Símbolos Originales", df_symbols_original)

def show_entropy_dataframe():
    show_dataframe("DataFrame de Entropía", df_entropy)

def show_copied_symbols():
    show_dataframe("DataFrame de Símbolos de la Copia", df_symbols_copia)

def show_12_bit_encoding():
    encoded_colors = [encode_to_12_bits(color) for color in df_symbols_original['Símbolo']]
    encoded_dataframe = pd.DataFrame({'Símbolo Original': df_symbols_original['Símbolo'], 'Codificación 12 bits': encoded_colors})
    show_dataframe("Codificación a 12 bits", encoded_dataframe)

def show_12_bit_decoding():
    decoded_colors = [decode_from_12_bits(value) for value in df_symbols_original['Símbolo']]
    decoded_dataframe = pd.DataFrame({'Símbolo Original': df_symbols_original['Símbolo'], 'Decodificación a 12 bits': decoded_colors})
    show_dataframe("Decodificación a 12 bits", decoded_dataframe)

def show_dataframe(title, dataframe):
    new_window = tk.Toplevel(root)
    new_window.title(title)
    
    text_widget = Text(new_window)
    text_widget.insert(tk.END, dataframe.to_string(index=False))
    text_widget.pack()

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

# Crear una copia del diccionario con símbolos aleatorios
diccionario_copia = dict()
for clave, valor in symbol_counts_dict.items():
    nuevo_simbolo = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(3))
    diccionario_copia[nuevo_simbolo] = valor

# Generar un DataFrame con los resultados de la copia del diccionario
df_symbols_copia = pd.DataFrame(sorted(diccionario_copia.items()), columns=['Símbolo', 'Cantidad'])

# Crear la interfaz gráfica
root = Tk()
root.title('Entropía a lo largo del tiempo')

# Agregar botón para generar gráfica
button_plot = Button(root, text='Generar Gráfica de Entropía', command=generate_plot)
button_plot.pack()

# Agregar botones para mostrar DataFrames
button_original_symbols = Button(root, text='Mostrar Símbolos Originales', command=show_original_symbols)
button_original_symbols.pack()

button_entropy_dataframe = Button(root, text='Mostrar DataFrame de Entropía', command=show_entropy_dataframe)
button_entropy_dataframe.pack()

button_copied_symbols = Button(root, text='Mostrar Símbolos de la Copia', command=show_copied_symbols)
button_copied_symbols.pack()

button_12_bit_encoding = Button(root, text='Mostrar Codificación a 12 bits', command=show_12_bit_encoding)
button_12_bit_encoding.pack()

button_12_bit_decoding = Button(root, text='Mostrar Decodificación a 12 bits', command=show_12_bit_decoding)
button_12_bit_decoding.pack()

# Agregar el lienzo para la gráfica
figure = plt.Figure(figsize=(6, 4), dpi=100)
plot_canvas = FigureCanvasTkAgg(figure, master=root)
plot_canvas.get_tk_widget().pack()

# Mostrar la interfaz gráfica
root.mainloop()
