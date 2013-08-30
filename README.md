# Chasm - Chip8 Assembler

This project define a basic ISA to CHIP8 and generate code based on ISA.
Transform asm in binary code:
```
./compiler.py -i pong.asm -o pong.c8
```

Transform binary code in asm:
```
./decompiler.py -i pong.c8 -o pong.asm
```

### All opcodes supported by ISA

| OPCODE  |      MNEMONIC        |
| ------- | -------------------- |
| 00E0    | CLS                  |
| 00EE    | RET                  |
| 0NNN    | SYS (addr)           |
| 1NNN    | JP (addr)            |
| 2NNN    | CALL (addr)          |
| 3XNN    | SE (Vx, byte)        |
| 4XNN    | SNE (Vx, byte)       |
| 5XY0    | SE (Vx, Vy)          |
| 6XNN    | LD (Vx, byte)        |
| 7XNN    | ADD (Vx, byte)       |
| 8XY0    | LD  (Vx, Vy)         |
| 8XY1    | OR  (Vx, Vy)         |
| 8XY2    | AND (Vx, Vy)         |
| 8XY3    | XOR (Vx, Vy)         |
| 8XY4    | ADD (Vx, Vy)         |
| 8XY5    | SUB (Vx, Vy)         |
| 8XY6    | SHR (Vx, Vy)         |
| 8XY7    | SUBN (Vx, Vy)        |
| 8XYE    | SHL (Vx, Vy)         |
| 9XY0    | SNE (Vx, Vy)         |
| ANNN    | LD I, (addr)         |
| BNNN    | JP (addr, V0)        |
| CXNN    | RND (Vx, byte)       |
| DXYN    | DRW (Vx, Vy, nibble) |
| EX9E    | SKP (Vx)             |
| EXA1    | SKNP (Vx)            |
| FX07    | LD (Vx), DT          |
| FX0A    | LD (Vx), K           |
| FX15    | LD DT, (Vx)          |
| FX18    | LD ST, (Vx)          |
| FX1E    | ADD I, (Vx)          |
| FX29    | LD F, (Vx)           |
| FX33    | LD B, (Vx)           |
| FX55    | LD [I], (Vx)         |
| FX65    | LD (Vx), [I]         |
|         | DB #NN               |
|         | DW #NNNN             |

### Super chip8

| OPCODE  |      MNEMONIC        |
| ------- | -------------------- |
| 00CN    | SCD (nibble)         |
| 00FB    | SCR                  |
| 00FC    | SCL                  |
| 00FD    | EXIT                 |
| 00FE    | LOW                  |
| 00FF    | HIGH                 |
| FX30    | LD HF, Vx            |
| FX75    | LD R, Vx             |
| FX85    | LD Vx, R             |
