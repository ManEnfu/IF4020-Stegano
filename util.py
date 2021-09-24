def read_file_binary(path: str) -> bytes:
    f = open(path, 'rb')
    b = f.read()
    f.close()
    return b

def write_file_binary(path: str, b: bytes):
    f = open(path, 'wb')
    f.write(b)
    f.close()

if __name__ == '__main__':
    b = read_file_binary('rc4.py')
    print(b)
