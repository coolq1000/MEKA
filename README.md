
# MEKA

The MEKA processor is a simplistic CPU intended for educational purposes.

# CPU Design

### Specs
|  Spec   |  Def   |
|---------|--------|
|  Memory |  64k   |
|  Speed  |min. 7Hz|
|Registers|   4    |

### Flags
|Flag|    Meaning     |
|----|----------------|
| C  |Conditional flag|

### Opcodes
|Opcode|ASM|
|------|----------------------|
| SET  | `mov vx, u8`         |
| ADD  | `add vx, vy`         |
| SUB  | `sub vx, vy`         |
| eql  | `eql vx, vy`         |
| JMP  | `jmp (u8 << 8) | u8` |
| JMC  | `jmc (u8 << 8) | u8` |

# This project 

This project includes a virtual machine along with a assembler.

It's all written in pure python.
