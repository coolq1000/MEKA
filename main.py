
from CPU import CPU
from Assembler import Assembler

Assembler('example/example.asm', 'example/example.bin')
CPU('example/example.bin')
