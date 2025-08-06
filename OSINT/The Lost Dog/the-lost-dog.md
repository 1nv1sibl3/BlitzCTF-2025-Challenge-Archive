## Challenge Overview
[BlitzCTF](https://ctf.blitzhack.xyz/) was proudly hosted and organized by my team [BlitzHack](https://blitzhack.xyz/), and this challenge was authored by me. This writeup provides an official solution to **"The Lost Dog"** challenge, which was in the OSINT category of the CTF.

![Challenge Details](https://i.ibb.co/RGKT3BkD/1.png)

# Part 1 - Finding the language
After reading the description, it is hence clear that the challenge requires the name of a certain dog which was looked after by the owner's friend who built a fast, statically typed **language** with systems-level access and C-like syntax.

On google dorking the keywords that are provided about the language in the description, and analyzing the top results it is very obvious that the language described is hence nothing else but **D lang**.

`intext:"fast" AND intext:"statically typed" AND intext:"systems-level access" AND intext:"C-like syntax"`

![Search Results - 1](https://i.ibb.co/7tvSny8N/2.jpg)

![Search Results - 2](https://i.ibb.co/Q7GVhfRb/2-1.jpg)

And for further confirmation we can visit the official website of [D lang](https://dlang.org/) and read the about section.

![D Lang](https://i.ibb.co/qMLYHjbd/3.jpg)

Hence, the description from the website matches with the challenge description, so we now know that the language is indeed **D lang**.

# Part 2 - Finding the dog

Now the friend is indeed the creator of the D lang, hence **Walter Bright** is the friend. Now we just have to find the dog's name. 🕵️

Running a short [Sherlock](https://www.kali.org/tools/sherlock/) scan shows Walter's account on various sites *(including some false positives)* but after analyzing the results, I discovered that Walter is very active on [HackerNews](https://news.ycombinator.com/user?id=WalterBright) so I should give it a try here.

So I searched for "HackerNews Search Engine" and this [site](https://hn.algolia.com/) came up. I became more curious and searched this dork: `"WalterBright" "Dog"`

Boom! The results were interesting.

![HN Algolia Results](https://i.ibb.co/bgPKRcdq/4.png)

And the third comment in the result matched the challenge description i.e. " Rover reveled in being the top dog in the neighborhood. One of his favorite methods to assert dominance was hilarious. We'd pass one yard that had a fence made from vertical planks butted against each other. The yard contained one of the beta dogs.

Rover found a knothole at just the right height, put his butt against it, and emptied through the hole into the beta dog's territory."

So I entered the flag Rover and boom it worked!!

**Flag:** `Blitz{Rover}`
