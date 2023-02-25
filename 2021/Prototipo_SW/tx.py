#!/usr/bin/python3

from serial import Serial
import sys

try:
  porta = sys.argv[1]
except:
  print('Uso: %s porta_serial' % sys.argv[0])
  sys.exit(0)

try:
  p = Serial(porta, 9600, timeout=10)
except Exception as e:
  print('Não conseguiu acessar a porta serial', e)
  sys.exit(0)

msg = 'um teste ...\r\n'

n = p.write(msg.encode('ascii'))
print('Enviou %d bytes' % n)

print('Digite ENTER para terminar:', end='')
sys.stdout.readline()

sys.exit(0)
