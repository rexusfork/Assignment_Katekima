class BasicLFSR:
    def __init__(self, initial_state="0110"):
        # Mengubah String ke List Integer
        self.state = [int(bit) for bit in initial_state]

        # Menyimpan panjang LFSR
        self.size = len(self.state)

    def get_state(self):
        # Mengubah List Integer ke String (Menampilkan state)
        return "".join(str(bit) for bit in self.state)

    def get_next_bit(self):
        # Menghitung feedback bit menggunakan XOR antara bit posisi ke-3 dan ke-0.
        # Kasus ini menggunakan 4 bit LFSR menggunakan polinomial x^4 + x + 1
        # Sehingga menggunakan index 3 dan index 0
        feedback_bit = self.state[3] ^ self.state[0]

        # Menyimpan bit paling kanan
        output_bit = self.state[-1]

        # Memasukkan feedback_bit ke posisi paling kiri dan membuang bit paling kanan
        self.state = [feedback_bit] + self.state[:-1]

        # Mengembalikan Bit paling kanan yang akan dihapus
        return output_bit


def test_basic_lfsr():
    print("Testing Basic LFSR with initial state 0110:")
    print("-" * 50)
    print("Iteration | State  | Output Bit")
    print("-" * 50)

    # Membuat Class Basic LFSR untuk State 0110
    lfsr = BasicLFSR("0110")

    # Menampilkan state dan next stream bit sebanyak 20 kali
    for i in range(20):
        state = lfsr.get_state()
        bit = lfsr.get_next_bit()
        print(f"{i+1:9} | {state} | {bit}")


if __name__ == "__main__":
    test_basic_lfsr()
