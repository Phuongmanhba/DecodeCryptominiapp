class MiniAppCrypto:
    def __init__(self, data):
        if isinstance(data, str):
            self.data = data.encode('latin-1')
        else:
            self.data = data
        self.history = [{"step": "Input", "output": self.text}]

    @property
    def text(self):
        return self.data.decode('latin-1')

    def log(self, stepname):
        self.history.append({"step": stepname, "output": self.text})
        return self

    def hextobytes(self):
        cleanhex = self.text.replace(" ", "").strip()
        self.data = bytes.fromhex(cleanhex)
        return self.log("Hex to Bytes")

    def tobinary(self):
        bits = []
        for b in self.data:
            bits.append(f"{b:08b}")
        self.data = " ".join(bits).encode('latin-1')
        return self.log("To Binary")

    def xor(self, key):
        if isinstance(key, int):
            keybytes = bytes([key])
        elif isinstance(key, str):
            keystr = key.strip()
            if keystr.startswith("0x") or keystr.startswith("0X"):
                keybytes = bytes.fromhex(keystr[2:])
            else:
                keybytes = keystr.encode('latin-1')
        else:
            keybytes = key

        if not keybytes:
            raise ValueError("Khóa XOR không được để trống")

        res = []
        for i in range(len(self.data)):
            b = self.data[i]
            k = keybytes[i % len(keybytes)]
            res.append(b ^ k)

        self.data = bytes(res)
        return self.log(f"XOR (key={key})")

    def shiftbytes(self, raw, k):
        res = []
        for b in raw:
            if 65 <= b <= 90:
                res.append((b - 65 + k) % 26 + 65)
            elif 97 <= b <= 122:
                res.append((b - 97 + k) % 26 + 97)
            else:
                res.append(b)
        return bytes(res)

    def caesar(self, shift, mode="decrypt"):
        if mode == "encrypt":
            k = shift
        elif mode == "decrypt":
            k = -shift
        else:
            raise ValueError("Mode phải là encrypt hoặc decrypt")

        self.data = self.shiftbytes(self.data, k)
        return self.log(f"Caesar ({mode}, k={shift})")

    def rot(self):
        lines = []
        for k in range(1, 26):
            out = self.shiftbytes(self.data, k).decode('latin-1')
            lines.append(f"ROT-{k}: {out}")
        self.data = "\n".join(lines).encode('latin-1')
        return self.log("ROT 1 -> 25")

    def vigenere(self, keyword, mode="decrypt"):
        if mode != "encrypt" and mode != "decrypt":
            raise ValueError("Mode phải là encrypt hoặc decrypt")

        shifts = []
        for c in keyword:
            if c.isalpha():
                shifts.append(ord(c.upper()) - 65)

        if not shifts:
            raise ValueError("Từ khóa phải có ít nhất 1 chữ cái")

        res = []
        keyidx = 0
        for b in self.data:
            if (65 <= b <= 90) or (97 <= b <= 122):
                if b <= 90:
                    base = 65
                else:
                    base = 97
                k = shifts[keyidx % len(shifts)]
                if mode == "decrypt":
                    k = -k
                res.append((b - base + k) % 26 + base)
                keyidx += 1
            else:
                res.append(b)

        self.data = bytes(res)
        return self.log(f"Vigenere ({mode}, key={keyword})")