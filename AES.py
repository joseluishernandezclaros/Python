class SimplifiedAES:
    # S-Box
    s_box = [
        0x9, 0x4, 0xA, 0xB, 0xD, 0x1, 0x8, 0x5,
        0x6, 0x2, 0x0, 0x3, 0xC, 0xE, 0xF, 0x7
    ]

    # S-Box Inversa
    s_box_i = [
        0xA, 0x5, 0x9, 0xB, 0x1, 0x7, 0x8, 0xF,
        0x6, 0x0, 0x2, 0x3, 0xC, 0x4, 0xD, 0xE
    ]

    def __init__(self, key):
        # Round keys: K0 = w0 + w1; K1 = w2 + w3; K2 = w4 + w5
        self.key_0, self.key_1, self.key_2 = self.key_expansion(key)

    def sub_2_nib(self, word):
        # Substitute word
        return (self.s_box[word >> 4] << 4) + self.s_box[word & 0x0F]

    def rot_word(self, word):
        # Rotate word
        return ((word & 0x0F) << 4) + ((word & 0xF0) >> 4)

    def key_expansion(self, key):
        rcon_1 = 0x80
        rcon_2 = 0x30

        w = [((key & 0xFF00) >> 8), (key & 0x00FF)]
        w.append(w[0] ^ (self.sub_2_nib(self.rot_word(w[1])) ^ rcon_1))
        w.append(w[2] ^ w[1])
        w.append(w[2] ^ (self.sub_2_nib(self.rot_word(w[3])) ^ rcon_2))
        w.append(w[4] ^ w[3])

        return (
            self.int_to_state((w[0] << 8), w[1]),
            self.int_to_state((w[2] << 8), w[3]),
            self.int_to_state((w[4] << 8), w[5])
        )

    def gf_mult(self, a, b):
        product = 0

        a = (a & 0x0F)
        b = (b & 0x0F)

        while a != 0 and b != 0:
            if b & 1 != 0:
                product ^= a

            a <<= 1

            if a & 0x10 != 0:
                a ^= 0b10011

            b >>= 1

        return product

    def int_to_state(self, high_byte, low_byte):
        return [
            (high_byte >> 4) & 0xF,
            (low_byte >> 4) & 0xF,
            high_byte & 0xF,
            low_byte & 0xF
        ]

    def state_to_int(self, state):
        return (state[0] << 12) + (state[2] << 8) + (state[1] << 4) + state[3]

    def add_round_key(self, s1, s2):
        return [(s1[i] ^ s2[i]) for i in range(4)]

    def sub_nibbles(self, s_box, state):
        return [s_box[state[i]] for i in range(4)]

    def shift_rows(self, state):
        return [state[0], state[1], state[3], state[2]]

    def mix_columns(self, state):
        result = [
            state[0] ^ self.gf_mult(4, state[2]),
            state[1] ^ self.gf_mult(4, state[3]),
            state[2] ^ self.gf_mult(4, state[0]),
            state[3] ^ self.gf_mult(4, state[1])
        ]

        return result

    def inverse_mix_columns(self, state):
        result = [
            self.gf_mult(9, state[0]) ^ self.gf_mult(2, state[2]),
            self.gf_mult(9, state[1]) ^ self.gf_mult(2, state[3]),
            self.gf_mult(9, state[2]) ^ self.gf_mult(2, state[0]),
            self.gf_mult(9, state[3]) ^ self.gf_mult(2, state[1])
        ]

        return result

    def encrypt(self, plaintext):
        state = self.add_round_key(self.key_0, self.int_to_state((plaintext >> 8), plaintext))
        state = self.mix_columns(self.shift_rows(self.sub_nibbles(self.s_box, state)))
        state = self.add_round_key(self.key_1, state)
        state = self.shift_rows(self.sub_nibbles(self.s_box, state))
        state = self.add_round_key(self.key_2, state)

        return self.state_to_int(state)

    def decrypt(self, ciphertext):
        state = self.add_round_key(self.key_2, self.int_to_state((ciphertext >> 8), ciphertext))
        state = self.sub_nibbles(self.s_box_i, self.shift_rows(state))
        state = self.inverse_mix_columns(self.add_round_key(self.key_1, state))
        state = self.sub_nibbles(self.s_box_i, self.shift_rows(state))
        state = self.add_round_key(self.key_0, state)

        return self.state_to_int(state)


# Programa principal
key = 0x2B7E
aes = SimplifiedAES(key)

plaintext = 0x3243
encrypted = aes.encrypt(plaintext)
decrypted = aes.decrypt(encrypted)

print(f"Texto Plano: {'{:04X}'.format(plaintext)}")
print(f"Encriptado:  {encrypted:X4}")
print(f"Desencriptado: {decrypted:X4}")
