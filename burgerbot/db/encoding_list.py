# encode list of ints into hex bytes
def encode(array):
    result = b''.join((hex(i)[2:].zfill(16).encode()) for i in array)
    # print(f"{array} -> {result}")
    return result


# decode hex bytes to list of ints
def decode(string):
    result = [int(string[i * 16:(i+1) * 16], 16) for i in range(len(string) // 16)]
    # print(f"{string} -> {result}")
    return result
