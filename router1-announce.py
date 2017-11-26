#!/usr/bin/env python3

import sys
import time

messages = [
    'announce route 10.10.1.0/24 next-hop 10.0.0.1',
    'announce route 10.10.11.0/24 next-hop 10.0.0.1',
]

time.sleep(2)

while messages:
	message = messages.pop(0)
	sys.stdout.write( message + '\n')
	sys.stdout.flush()
	time.sleep(1)

while True:
	time.sleep(1)
