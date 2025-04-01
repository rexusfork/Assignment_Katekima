class GeneralLFSR:
    def __init__(self, size=4, initial_state=None, taps=None):
        # Ukuran dari State
        self.size = size

        # Menetapkan Status awal jika initial_state=None
        # Sehingga semua Initial State diisi nol sebanyak size
        if initial_state is None:
            self.state = [0] * size
        elif isinstance(initial_state, str):
            # Mengubah String menjadi List Integer dan mengambil size elemen paling kanan
            # Hal ini dilakukan karena hanya menyimpan bit terakhir sebanyak size
            self.state = [int(bit) for bit in initial_state][-size:]

            # Hanya terjadi ketika size dari initial_state lebih pendek
            # Menambahkan 0 pada state tersebut
            if len(self.state) < size:
                self.state = [0] * (size - len(self.state)) + self.state
        else:
            # Mengubah String menjadi List Integer dan mengambil size elemen paling kanan
            # Hal ini dilakukan karena hanya menyimpan bit terakhir sebanyak size
            self.state = initial_state[-size:]

        # Jika taps=None maka default nya posisi 3 dan 0
        # Mengambil Posisi Default berdasarkan polynomial -> x^4 + x + 1
        self.taps = taps if taps is not None else [3, 0]

    def get_state(self):
        # Mengubah List Integer ke String (Menampilkan state)
        return "".join(str(bit) for bit in self.state)

    def set_state(self, new_state):
        # Mengatur Ulang isi LFSR tanpa membuat Objek Kembali
        if isinstance(new_state, str):
            self.state = [int(bit) for bit in new_state][-self.size :]
        else:
            self.state = new_state[-self.size :]

    def get_size(self):
        # Mengambil Size dari LFSR (State)
        return self.size

    def set_size(self, new_size):
        # Mengubah Ukuran LFSR (State) dan mempertahankan bit paling kanan
        current_state = self.state
        self.size = new_size

        # Jika State Saat ini lebih besar dari ukuran baru
        if len(current_state) > new_size:
            # Mempertahankan bit paling kanan, ketika akan dipotong bit di bagian kiri
            self.state = current_state[-new_size:]
        else:
            # Menambahkan 0 pada bagian paling kiri ketika ukuran baru lebih besar dari ukuran saat ini
            self.state = [0] * (new_size - len(current_state)) + current_state

    def set_taps(self, new_taps):
        # Mengatur ukuran dari tap dengan tap yang baru
        self.taps = new_taps

    def get_taps(self):
        # Mendapatkan posisi tap saat ini
        return self.taps

    def reset(self):
        # Mengembalikan State LFSR untuk semua dengan nilai 0 sebanyak size
        self.state = [0] * self.size

    def get_next_bit(self):
        feedback_bit = 0

        # Menghitung feedback_bit tidak hanya pada kasus polynomial X^4 + x + 1
        # Namun bisa untuk positi tap lain.
        for tap in self.taps:
            feedback_bit ^= self.state[tap]

        # Menyimpan bit paling kanan
        output_bit = self.state[-1]

        # Memasukkan feedback_bit ke posisi paling kiri dan membuang bit paling kanan
        self.state = [feedback_bit] + self.state[:-1]

        return output_bit


# Testing General LFSR untuk Konfigurasi Basic LFSR
def test_general_lfsr():
    print("\nTesting General LFSR configured to match the basic LFSR:")
    print("-" * 50)
    print("Iteration | State  | Output Bit")
    print("-" * 50)

    # Konfigurasi LFSR untuk state seperti basic dengan initial state 0110 dan tap[3,0]
    lfsr = GeneralLFSR(size=4, initial_state="0110", taps=[3, 0])

    for i in range(20):
        state = lfsr.get_state()
        bit = lfsr.get_next_bit()
        print(f"{i+1:9} | {state} | {bit}")


# Testing General LFSR dengan konfigurasi yang berbeda-beda
def test_different_configurations():
    print("\nTesting General LFSR with different configurations:")

    # Test 1: Menggunakan LFSR dengan 5 bit dengan posisi tap 4 dan 1
    print("\n5-bit LFSR (x^5 + x^2 + 1), initial state 10101:")
    print("-" * 50)
    print("Iteration | State   | Output Bit")
    print("-" * 50)

    lfsr1 = GeneralLFSR(size=5, initial_state="10101", taps=[4, 1])

    for i in range(10):
        state = lfsr1.get_state()
        bit = lfsr1.get_next_bit()
        print(f"{i+1:9} | {state} | {bit}")

    # Test 2: Menggunakan LFSR dengan 3-bit dengan posisi tap 2 dan 1
    print("\n3-bit LFSR (x^3 + x^2 + 1), initial state 111:")
    print("-" * 50)
    print("Iteration | State | Output Bit")
    print("-" * 50)

    lfsr2 = GeneralLFSR(size=3, initial_state="111", taps=[2, 1])

    for i in range(10):
        state = lfsr2.get_state()
        bit = lfsr2.get_next_bit()
        print(f"{i+1:9} | {state} | {bit}")


if __name__ == "__main__":
    test_general_lfsr()
    test_different_configurations()
