class RC4KeyStream:

    def __init__(self, K: bytes):
        self.S = [x for x in range(256)]
        self.i = 0
        self.j = 0
        if K is not None:
            self.init_key(K)

    def init_key(self, K: bytes):
        self.S = [x for x in range(256)]
        self.i = 0
        self.j = 0
        j = 0
        for i in range(255):
            j = (j + self.S[i] + K[i % len(K)]) % 256
            temp = self.S[i]
            self.S[i] = self.S[j]
            self.S[j] = temp

    def get(self):
        self.i = (self.i + 1) % 256
        self.j = (self.j + self.S[self.i]) % 256
        temp = self.S[self.i]
        self.S[self.i] = self.S[self.j]
        self.S[self.j] = temp
        t = (self.S[self.i] + self.S[self.j]) % 26
        u = self.S[t]
        return u

class ModifiedRC4KeyStream:

    def __init__(self, K: bytes):
        self.S = [x for x in range(256)]
        self.i = 0
        self.j = 0
        if K is not None:
            self.init_key(K)

    def init_key(self, K: bytes):
        self.S = [x for x in range(256)]
        self.i = 0
        self.j = 0
        j = 0
        for i in range(255):
            j = (j + self.S[i] + K[i % len(K)]) % 256
            temp = self.S[i]
            self.S[i] = self.S[j]
            self.S[j] = temp

    def get(self):
        self.i = (self.i + 1) % 256
        self.j = (self.j + self.S[self.i]) % 256
        a = self.i
        b = self.j
        if a > b:
            b += 256
        # reverse the ordering from S[i] to S[j]
        while a < b:
            temp = self.S[a % 256]
            self.S[a % 256] = self.S[b % 256]
            self.S[b % 256] = temp
            a += 1
            b -= 1
        t = (self.S[self.i] + self.S[self.j]) % 26
        u = self.S[t]
        return u
        
def encrypt(P: bytes, K: bytes):
    ks = RC4KeyStream(K)
    return bytes([p ^ ks.get() for p in P])

def decrypt(C: bytes, K: bytes):
    ks = RC4KeyStream(K)
    return bytes([c ^ ks.get() for c in C])

def moencrypt(P: bytes, K: bytes):
    ks = ModifiedRC4KeyStream(K)
    return bytes([p ^ ks.get() for p in P])

def modecrypt(C: bytes, K: bytes):
    ks = ModifiedRC4KeyStream(K)
    return bytes([c ^ ks.get() for c in C])

if __name__ == '__main__':
    p = b'Hello World'
    k = b'key'
    c = encrypt(p, k)
    p2 = decrypt(c, k)
    print(p)
    print(c)
    print(p2)
    c = moencrypt(p, k)
    p2 = modecrypt(c, k)
    print(c)
    print(p2)
