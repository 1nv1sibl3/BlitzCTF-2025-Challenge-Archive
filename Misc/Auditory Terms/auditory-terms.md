## Challenge Overview
[BlitzCTF](https://ctf.blitzhack.xyz/) was proudly hosted and organized by my team [BlitzHack](https://blitzhack.xyz/), and this challenge was authored by me. This writeup provides an official solution to the **"Auditory Terms"** challenge, which was in the Misc category of the CTF.

![Challenge Details](https://i.ibb.co/8gTZ38zT/at1.png)

This challenge involves a `.txt` file named [terms_of_use.txt](https://drive.google.com/file/d/1Yfof6jhLLQPvbWeA3v52gU_EE6pdIRNx/view).

# Part 1 - Getting the audio file
By running a simple `file terms_of_use.txt` command we can see that it outputs data rather than ASCII indicating something fishy here.

```
 ~ file terms_of_use.txt                                                                      
terms_of_use.txt: data

 ~ file file.txt                                                                             
file.txt: ASCII text
```

To investigate further, let's search for the RIFF header (52494646 in hex, common for WAV files) inside the file using xxd and grep:

`xxd -p terms_of_use.txt | tr -d '\n' | grep -bo "52494646"`

This command converts the file to a plain hex dump `(-p)`, strips newlines to make it a single continuous stream, and then searches for the byte offset of the string `52494646`, which marks the start of a possible WAV file embedded in the data.

```
 ~  xxd -p terms_of_use.txt | tr -d '\n' | grep -bo "52494646"
1140:52494646
```

Running this command results in `1140` but since `xxd -p` outputs hex characters (2 characters per byte), the `grep -bo` result (1140) had to be divided by 2 to get the correct byte offset: `570`.

Now we use `dd` to extract the embedded file starting from that offset:

`dd if=terms_of_use.txt bs=1 skip=570 of=audio.wav`

This command extracts data from `terms_of_use.txt` starting at byte 570 and saves it as `fixed.wav`. It reads the file byte by byte `(bs=1)`, skips the first 570 bytes (where the WAV header begins), and writes the rest to create a clean WAV file.

Now, running the `file audio.wav` command confirms our extraction was successful:

`audio.wav: RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, mono 24000 Hz`

This shows that the extracted data is a valid WAV file with standard audio formatting, confirming the presence of embedded audio within the original text file.

# Part 2 - Reading the audio file

Listening to the `audio.wav` file confirms that it was extracted correctly. Toward the end of the audio, there's a voice that appears to be speaking the flag, but it's played too fast to understand. To fix this, we can open the file in [Audacity](https://www.audacityteam.org/) and slow it down to make the speech clear and extract the flag.

![Audacity](https://i.ibb.co/8Dy4DCnF/audacity.png)

To slow down the audio in Audacity, first select the portion where the flag is spoken - near the end. Then, navigate to Effect → Pitch and Tempo → Change Pitch and lower the pitch to slow down the voice. You can also apply Effect → Delay & Reverb → Reverb to reduce echo and enhance clarity. With these adjustments, the speech becomes easier to understand, allowing you to clearly hear and extract the flag.

**Flag:** `Blitz{r0b0t1c_v0ice}`




