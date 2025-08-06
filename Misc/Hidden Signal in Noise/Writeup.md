## Overview
This challenge involved recovering a flag from a corrupted `.mrf` file.  
The description clearly explained the corruption method, so I went straight to implementing the solution.

## Solution Script

- [`exp.py`](./exp.py)

This script works as follows:

File Header Check – The program verifies that the file starts with the expected magic header 0x5AA55AA5.

Nibble Extraction – It reads the high nibble (upper 4 bits) from every 10th byte, starting after the header.

Character Reconstruction – Pairs of extracted nibbles are combined to form ASCII character codes.

Flag Recovery – The script stops if a non-printable character is encountered, outputting the recovered flag.
