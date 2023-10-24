


def add_round_key(state, round_key):
  """
  Combina el estado de la ronda anterior con la subclave actual.

  Args:
    state: El estado de la ronda anterior.
    round_key: La subclave actual.

  Returns:
    El estado de la ronda actual.
  """

  for i in range(4):
    for j in range(4):
      state[i][j] ^= round_key[i][j]

  return state

def mix_columns(state):
  """
  Mezcla los bytes de cada columna del estado.

  Args:
    state: El estado de AES.

  Returns:
    El estado mezclado.
  """

  for i in range(4):
    # Selecciona la columna i del estado.
    column = state[:, i]

    # Aplica la función MixColumns a cada byte de la columna.
    for j in range(4):
      column[j] = (column[j] ^ g(column[0]) ^ h(column[1]) ^ i(column[2]) ^ j(column[3]))

    state[:, i] = column

  return state

def shift_rows(state):
  """
  Desplaza los bytes de cada fila del estado.

  Args:
    state: El estado de AES.

  Returns:
    El estado desplazado.
  """

  # Desplaza los bytes de la primera fila 1 byte a la izquierda.
  state[0] = state[0][1:] + [state[0][0]]

  # Desplaza los bytes de la segunda fila 2 bytes a la izquierda.
  state[1] = state[1][2:] + [state[1][0], state[1][1]]

  # Desplaza los bytes de la tercera fila 3 bytes a la izquierda.
  state[2] = state[2][3:] + [state[2][0], state[2][1], state[2][2]]

  # Desplaza los bytes de la cuarta fila 4 bytes a la izquierda.
  state[3] = state[3][4:] + [state[3][0], state[3][1], state[3][2], state[3][3]]

  return state

def SubBytes(state):
  """
  Sustituye los bytes de un estado AES128 utilizando la tabla S-Box.

  Args:
    state: Un estado AES128 de 16 bytes.

  Returns:
    Un estado AES128 modificado.
  """

  for i in range(16):
    state[i] = sbox[state[i]]

  return state

def generate_round_keys(key):
  """
  Genera las subclaves del algoritmo AES128.

  Args:
    key: La clave AES128 de 16 bytes.

  Returns:
    Una lista de 11 subclaves de 16 bytes.
  """

  # Inicializa la matriz de subclaves.
  round_keys = [[0] * 4 for _ in range(11)]

  # Copia la clave original en la primera fila de la matriz de subclaves.
  for i in range(4):
    round_keys[0][i] = key[i]

  # Genera las 10 subclaves restantes.
  for round in range(1, 11):
    # Realiza una rotación circular de la fila superior de la matriz de subclaves.
    round_keys[round][0] = round_keys[round - 1][3]
    round_keys[round][1] = round_keys[round - 1][0]
    round_keys[round][2] = round_keys[round - 1][1]
    round_keys[round][3] = round_keys[round - 1][2]

    # Aplica la función SubBytes a la fila superior de la matriz de subclaves.
    for i in range(4):
      round_keys[round][i] = sbox[round_keys[round][i]]

    # Realiza una XOR entre la fila superior de la matriz de subclaves y la constante RCON[round - 1].
    round_keys[round][0] ^= RCON[round - 1]

  return round_keys

def main():
  """
  Función principal del algoritmo AES128.

  Pide un texto al usuario y lo cifra utilizando el algoritmo AES128.

  Returns:
    El texto cifrado.
  """

  # Pide un texto al usuario.
  plaintext = input("Introduzca el texto que desea cifrar: ")

  # Convierte el texto en bytes.
  plaintext = bytes(plaintext, "utf-8")

  # Inicializa el estado AES128.
  state = plaintext[:16]

  # Genera las subclaves.
  key = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
  round_keys = generate_round_keys(key)

  # Cifra el texto.
  for round_key in round_keys:
    state = add_round_key(state, round_key)
    state = SubBytes(state)
    state = shift_rows(state)
    state = mix_columns(state)

  # Obtiene el texto cifrado.
  ciphertext = state

  # Devuelve el texto cifrado.
  return ciphertext


if __name__ == "__main__":
  ciphertext = main()
  print("El texto cifrado es:", ciphertext.hex())



main()