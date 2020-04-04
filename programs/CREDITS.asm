; Show the name of the creator
; Author: Alexandre Barbieri (fakeezz@gmail.com)

; VA = Position X
; VB = Position Y
; VC = Current Sprite
; VD = Flow Control

; Load Default values
LD V1, #32 ; Sprite A
LD V2, #4B ; Sprite F
LD V3, #46 ; Sprite E
LD VA, 15
LD VB, 15

; Load F
LD F, V2
DRW VA, VB, 5

; Load A
ADD VA, 5
LD F, V1
DRW VA, VB, 5

; Load K
ADD VA, 1
LD I, Sprite_K
DRW VA, VB, 5

; Load E
ADD VA, 9
LD F, V3
DRW VA, VB, 5

; Load E
ADD VA, 5
LD F, V3
DRW VA, VB, 5

; Load Z
ADD VA, 1
LD I, Sprite_Z
DRW VA, VB, 5

; Load Z
ADD VA, 5
LD I, Sprite_Z
DRW VA, VB, 5

Exit:
    JP Exit

Sprite_Line:
    DW #FF00

Sprite_K:
    DW #090A
    DW #0C0A
    DW #0900

Sprite_Z:
    DW #0F02
    DW #0408
    DW #0f00
