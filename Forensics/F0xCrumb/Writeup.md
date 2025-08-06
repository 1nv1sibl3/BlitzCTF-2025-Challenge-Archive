## F0xCrumb

> Don't keep the jar of cookies in the open...
>
> File link: [https://drive.google.com/file/d/1oLiJ9NQH9UFv-W1iFvlXbUB4k-0X8e7L/view?usp=sharing](https://drive.google.com/file/d/1oLiJ9NQH9UFv-W1iFvlXbUB4k-0X8e7L/view?usp=sharing)

This was a relatively easy forensics challenge. The name hints towards **Firefox** and the description has the word **cookies**, indicating that we have to find a certain cookie in the Firefox browser.

Let's start by analysing the memory dump that we have, it can be easily done using volatility3 and running the following command:

```bash
vol -f firefoxchall windows.info
```
<img width="1525" height="533" alt="image" src="https://github.com/user-attachments/assets/d9b0c3f4-2a06-419f-8f14-e9488327f64b" />



On a windows machine we know that user data of Firefox would be stored in `\AppData\Roaming\Mozilla\Firefox\Profiles\` . We use the following  command to find it:

```bash
vol -f firefoxchall windows.filescan | grep -i "firefox"
```

We find the exact location of the sqlite file storing the cookies:

```bash
0xe1811368d590  \Users\jennie\AppData\Roaming\Mozilla\Firefox\Profiles\qxjsnlmd.default-release\cookies.sqlite
```

Now we have to dump this file which can be done by specifying the virtual address we found:

```bash
vol -f firefoxchall windows.dump --virtaddr 0xe1811368d590
```

Using any sqlite viewer we can then explore the cookie table, I used **sqlite3** and got this output:


```
1||totallynormalcookie|QmxpdHp7ZjFyM2YweF81aDB1bGRfM25jcnlwdF9jMDBrMTM1fQo%3D|military-candle-elephant.glitch.me|/|1742710132|1742623732174000|1742623723377000|0|1|0|1|0|2|0
```


The string `QmxpdHp7ZjFyM2YweF81aDB1bGRfM25jcnlwdF9jMDBrMTM1fQo` stands out and base64 decoding it gives us the flag:

```
Blitz{f1r3f0x_5h0uld_3ncrypt_c00k135}
```
