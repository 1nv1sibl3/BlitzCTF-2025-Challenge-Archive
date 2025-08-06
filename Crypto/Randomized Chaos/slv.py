def complex_encrypt_byte(f, k):
    k %= 256
    r = (f ^ k) & ((~k | f) & 0xFF)
    r = ((r << (k % 8)) | (r >> (8 - (k % 8)))) & 0xFF
    return r

from collections import Counter

def recover_flag_freq(ciphertexts, length):
    flag = bytearray()
    freq_list = [Counter(ct[i] for ct in ciphertexts) for i in range(length)]

    for freq in freq_list:
        best_f, best_score = 0, float('inf')
        total = sum(freq.values())

        for f_guess in range(256):
            sim = Counter(complex_encrypt_byte(f_guess, k) for k in range(256))
            for k in sim:
                sim[k] /= 256

            score = sum(
                (freq[c]/total - sim.get(c, 0))**2 for c in freq
            )
            if score < best_score:
                best_score, best_f = score, f_guess

        flag.append(best_f)
    return flag

# Load ciphertexts
with open("output_4.txt") as f:
    ciphertexts = [bytearray.fromhex(line.strip()) for line in f]

# Recover flag
flag = recover_flag_freq(ciphertexts, len(ciphertexts[0]))
print("Recovered flag:", flag.decode())