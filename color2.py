#!/bin/env python
import sys
from termcolor import colored, cprint

text = colored('hello world.','red',attrs=['reverse','blink'])
print(text)
cprint('hello world.','green','on_red')

print_red_on_cyan = lambda x: cprint(x,'red','on_cyan')
print_red_on_cyan('hello world.')
print_red_on_cyan('this is a test.')

for i in range(10):
    cprint(i,'magenta',end=' ')

cprint('attention!','red',attrs=['bold'],file=sys.stderr)




