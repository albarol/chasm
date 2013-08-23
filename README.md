---------------------------------
| OPCODE | MNEMONICO            |
---------------------------------
| 0NNN   |    SYS               |
| 00E0   |    CLS               |
| 00EE   |    RET               |
| 1NNN   |  JMP <addr>          |
| 2NNN   |  CALL <addr>         |
| 3XNN   |  SE <Vx, byte>       |
| 4XNN   | SNE <Vx, byte>       |
| 5XY0   | SE <Vx, Vy>          |
| 6XNN   | LD <Vx, byte>        |
| 7XNN   | ADD <Vx, byte>       |
| 8XY0   | LD  <Vx, Vy>         |
| 8XY1   | OR  <Vx, Vy>         |
| 8XY2   | AND <Vx, Vy>         |
| 8XY3   | XOR <Vx, Vy>         |
| 8XY4   | ADD <Vx, Vy>         |
| 8XY5   | SUB <Vx, Vy>         |
| 8XY6   | SHR <Vx, Vy>         |
| 8XY7   | SUBC <Vx, Vy>        |
| 8XYE   | SHL <Vx, Vy>         |
| 9XY0   | SNE <Vx, Vy>         |
| ANNN   | LDI <addr>           |
| BNNN   | JMP <addr, V0>       |
| CXNN   | RND <Vx, byte>       |
| DXYN   | DRW <Vx, Vy, nibble> |
| EX9E   | SKP <Vx>             |
| EXA1   | SKNP <Vx>            |
| FX07   | LD <Vx>, DT          |
| FX0A   | LD <Vx>, K           |
| FX15   | LD DT, <Vx>          |
| FX18   | LD ST, <Vx>          |
| FX1E   | LD I, <Vx>           |
| FX29   | LD F, <Vx>           |
| FX33   | LD B, <Vx>           |
| FX55   | STR <Vx>             |
| FX65   | FIL <Vx>             |
---------------------------------
