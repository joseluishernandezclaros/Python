import cv2
import numpy as np
import pandas as pd


def calculate_entropy(image):
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])
    hist = hist / float(hist.sum() + 1e-6)
    entropy = -np.sum(hist * np.log2(hist + 1e-6))
    return entropy


def generate_all_symbols(frame):
    symbols = []
    for row in frame:
        for pixel in row:
            # Usa una representación más compacta del color
            compact_color = tuple(pixel // 32)
            symbols.append(compact_color)
    return symbols


# Nombre del archivo de video
video_path = 'tu_video.mp4'

# Abre el video
cap = cv2.VideoCapture(video_path)

# Inicializa una lista para almacenar todos los símbolos del video
all_symbols_video = []

# Lee los fotogramas del video
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
current_frame = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Convierte la imagen a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calcula la entropía del canal de luminancia
    entropy = calculate_entropy(gray)

    # Genera todos los símbolos posibles para este fotograma
    all_symbols = generate_all_symbols(frame)

    # Agrega los símbolos de este fotograma a la lista general
    all_symbols_video.extend(all_symbols)

    # Imprime el progreso
    current_frame += 1
    print(f'Frames procesados: {current_frame}/{total_frames}')

# Convierte los símbolos a una lista de cadenas
symbols_list_video = [str(symbol) for symbol in all_symbols_video]

# Crea un DataFrame con los resultados de los símbolos de todo el video
df_symbols_video = pd.DataFrame({'Símbolo': symbols_list_video})

# Muestra el DataFrame final con la cuenta de cada símbolo
symbol_counts_video = df_symbols_video['Símbolo'].value_counts().reset_index()
symbol_counts_video.columns = ['Símbolo', 'Cantidad']
print("\nDataFrame de Símbolos para todo el Video:")
print(symbol_counts_video)

# Cierra el video y libera recursos
cap.release()
