## Overview

The problem itself asks you to get know Object Linking and Embedding (OLE)` file. You can get know more about it from [here](https://en.wikipedia.org/wiki/Object_Linking_and_Embedding).

The oletools will help you to extract and analyze hidden link/text from the doc file.

Installation

``
pip install oletools
``

First of all, let’s use olevba to extract macros embedded in Word file. Output file shows below.

- [`output.txt`](./output.txt)


+ It runs AutoOpen to show some messages.

+ It calls EmbedDesktopZip which tries to embed a ZIP file named secret.zip located on the user’s Desktop (%USERPROFILE%\\Desktop\\secret.zip).

+ The ZIP filename is obfuscated as "zcrseet.ip" and unscrambled by reversing and fixing the extension.

+ If the ZIP is missing, it shows an error and exits.

If you seeks closely, there’ll be suspicious decimals denoted as a key of something.

``
Key & Chr(83) & Chr(117) & Chr(112) & Chr(51) & Chr(114) & Chr(83) & Chr(51) & Chr(99) & Chr(114) & Chr(101) & Chr(116) & Chr(80) & Chr(97) & Chr(115) & Chr(115) & Chr(87) & Chr(48) & Chr(82) & Chr(68)
``
Decryption gives you a password: `Sup3rS3cretPassW0RD`

Since there’s a password, there must be a file or something else associated with it.

Now, extract the hidden links of Doc file.

```
┌──(py310env)─(zwique㉿zwique)-[~/Downloads]
└─$ oleobj Essay.docm 
oleobj 0.60.1 - http://decalage.info/oletools
THIS IS WORK IN PROGRESS - Check updates regularly!
Please report any issue at https://github.com/decalage2/oletools/issues

-------------------------------------------------------------------------------
File: 'Essay.docm'
Found relationship 'hyperlink' with external link https://www.youtube.com/watch?v=dQw4w9WgXcQ
```



