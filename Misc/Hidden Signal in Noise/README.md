# Hidden Signal in Noise

**Category:** Misc  
**Points:** 63  
**Solves:** 70  

## Description

The file magic.mrf starts with a 4-byte magic header. After the header, the flag is hidden by splitting each character into two parts, each stored in the high nibble of bytes spaced roughly every X bytes. The low nibble contains random noise. The flag begins with Blitz{. Recover the flag by extracting and decoding these bytes.

Author: `Zwique`

## Files

- [magic.mrf](https://github.com/1nv1sibl3/BlitzCTF-2025/blob/main/files/5f6fc19409e7512980ebf44700690bd5/magic.mrf)

## Flag

`Blitz{H1dd3n_4n4lyt1c_Ch4ll3ng3}`

## Writeup

[View Writeup](https://github.com/1nv1sibl3/BlitzCTF-2025/blob/main/writeups/Hidden Signal in Noise_writeup.md)
