- [`slv.py`](./slv.py) – Solution Script

# Here is the explaination of `slv.py`

## Complex Byte Encryption & Flag Recovery

This script demonstrates a custom byte-level encryption algorithm and a frequency-analysis-based method for recovering an encrypted flag.

## How It Works

### 1. `complex_encrypt_byte(f, k)`
Encrypts a single byte (`f`) with a key byte (`k`) using:
- **Key normalization**: `k %= 256`
- **Bitwise mixing**:
  - XOR with key
  - AND with a mask based on key and original byte
- **Bit rotation**: Rotate left by `(k % 8)` bits

### 2. `recover_flag_freq(ciphertexts, length)`
Recovers the original flag by:
1. Collecting frequency statistics of each byte position from multiple ciphertexts.
2. Trying all possible plaintext byte guesses (`0–255`).
3. Simulating encryption for each guess and comparing distributions.
4. Picking the guess with the **lowest frequency difference** (Euclidean distance).
5. Building the flag byte-by-byte.

### 3. Main Script
- Reads ciphertexts from `output_4.txt` (hex-encoded lines).
- Runs `recover_flag_freq` to deduce the plaintext.
- Prints the recovered flag.

## Usage
```bash
python script.py
