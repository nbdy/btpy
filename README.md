## btpy

[![asciicast](https://asciinema.org/a/299826.svg)](https://asciinema.org/a/299826)

### how to ..
#### .. install
```shell
pip3 install btpy
```

#### .. to use it
```
Python 3.7.5rc1 (default, Oct  8 2019, 16:47:45) 
Type 'copyright', 'credits' or 'license' for more information
IPython 7.9.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: from btpy import Scanner, ClassicDevice                                                                                                                                        

In [2]: Scanner.scan_for()                                                                                                                                                             
Permission Denied
Set scan parameters failed (are you root?)
found 1 devices
Out[2]: [<btpy.libs.bt.classic.ClassicDevice at 0x7f3427045210>]

In [3]: c = ClassicDevice.scan()                                                                                                                                                       

In [4]: c                                                                                                                                                                              
Out[4]: [<btpy.libs.bt.classic.ClassicDevice at 0x7f3425559d50>]

In [5]: c[0].__dict__                                                                                                                                                                  
Out[5]: 
{'address': 'A8:B8:6E:C1:6A:28',
 'timestamp': '03.11.2019 16:48:06',
 'name': 'Nexus 5X'}

```

or check [bt.py](https://github.com/nbdy/btpy/blob/master/bt.py)
