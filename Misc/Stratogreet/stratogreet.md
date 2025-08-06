## Challenge Overview
[BlitzCTF](https://ctf.blitzhack.xyz/) was proudly hosted and organized by my team [BlitzHack](https://blitzhack.xyz/), and this challenge was authored by me. This writeup provides an official solution to the **"Stratogreet"** challenge, which was in the Misc category of the CTF.

![Challenge Details](https://i.ibb.co/JWWZh7W6/s1.png)

In this challenge, a `.wav` file was provided named [stratogreet.wav](https://drive.google.com/file/d/1vpjd2a9_YpLPz9hzah64c5ZxiQYrPbGa/view).

# Part 1 - Decoding the Audio
Now after listening to the audio file & analyzing it, and further looking at the description we can easily guess that this is a Slow Scan TV (SSTV) file.

> Slow-scan television (SSTV) is a picture transmission method, used mainly by amateur radio operators, to transmit and receive static pictures via radio in monochrome or color. In the case of ISS, images are sent on 145.800 MHz FM using the SSTV mode PD120 mode with a (roughly) 2 minutes on, 2 minutes off schedule.[Read More](https://amsat-uk.org/beginners/iss-sstv/)

To decode this SSTV file, we can use various set of tools according to the operating system in use, some are listed below:

- Linux — [QSSTV](https://github.com/ON4QZ/QSSTV)
- Windows — [RX-SSTV](https://www.qsl.net/on6mu/rxsstv.htm)
- Mac — [MultiScan 3B](https://qsl.net/v/ve3elb/KD6CJI-MultiScan3B/)

In this case, I will be using RX-SSTV, to decode this SSTV file and retrieve the image, simply open RX-SSTV, play the audio file and it will decode the image simultaneously while the audio is playing.

![RX-SSTV Decoding Audio](https://i.ibb.co/mC83wyTn/Screenshot-18.png)

After decoding the SSTV in the RX-SSTV, we get the following image:

![Image](https://i.ibb.co/bMBnJ067/s2.jpg)

# Part 2 - Finding the date

We can clearly see that the mission mentioned in the image is [Appolo Soyuz](https://en.wikipedia.org/wiki/Apollo%E2%80%93Soyuz). A simple search on google for Apollo Soyuz launch date results in **July 15, 1975**.

So the final **flag** becomes: `Blitz{1975_07_15}`