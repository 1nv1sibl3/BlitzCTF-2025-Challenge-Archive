FILENAME = "magic.mrf"

def decode_flag(filename):
    with open(filename, "rb") as f:
        data = f.read()

    if data[:4] != b"\x5A\xA5\x5A\xA5":
        print("Warning: Unexpected magic header")

    # Extract high nibbles every 10 bytes
    nibbles = [(data[i] >> 4) for i in range(4, len(data), 10)]

    # Combine nibbles into ASCII characters
    chars = []
    for i in range(0, len(nibbles) - 1, 2):
        c = (nibbles[i] << 4) | nibbles[i+1]
        if 32 <= c <= 126:
            chars.append(chr(c))
        else:
            break

    print("Recovered flag:", "".join(chars))

if __name__ == "__main__":
    decode_flag(FILENAME)