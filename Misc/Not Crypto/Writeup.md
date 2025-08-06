## Not Crypto (Misc)

> It can't be in the crypto category... everything is there for you to grab. Also don't try brute forcing&#x20;
>
> File link: [https://drive.google.com/file/d/1NH\_rCjNcHHgcA5EJhJoA5X3dsepBLW5s/view?usp=sharing](https://drive.google.com/file/d/1NH_rCjNcHHgcA5EJhJoA5X3dsepBLW5s/view?usp=sharing)

Sadly, this challenge remained unsolved till the end as I believe most people were spending time on trying to find an exploit in the cryptography part. That was the reason I kept the challenge **Not Crypto**.&#x20;

To solve this challenge the first step could be figured out from the fact that you are provided with a `.pyc` file instead of a normal `.py` file. Usually in this case you should think of something related to steganography, the password used to encrypt data was unknown so probably that was hidden. By doing some digging you come across:

> A steganography tool for embedding payloads within Python bytecode, [stegosaurus](https://github.com/AngelKitty/stegosaurus)

Simply running the extraction command reveals the hidden password:

```bash
./stegosaurus encrypt.cpython-36.pyc -x

Output:
Extracted payload: whoevenputsthepasswordhereandwhyisitsooooooLONG?
```

To figure out the encryption used you can use [https://github.com/rocky/python-uncompyle6](https://github.com/rocky/python-uncompyle6) to uncompile the `.pyc` file and get the orginal code. Then with basic crypto knowledge or even ChatGPT write the decryption script. On decryption you get the flag:

```
Blitz{h0ly_whY_w0uLd_u_puT_tH3_p4ssw0rd_th3re?}
```
