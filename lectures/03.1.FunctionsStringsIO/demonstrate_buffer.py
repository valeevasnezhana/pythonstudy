import sys
from time import sleep

print('test', end='')
# uncomment to fix!
sys.stdout.flush()
print('err', file=sys.stderr)

sleep(1)
