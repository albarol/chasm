
LD V1, 0x08 ; height of letter
LD V2, 0x00 ; height of current letter


LD Va, 0x05     ; Start position of X
LD Vb, 0x01     ; Start position of Y

Draw_Line_C:
    ADD Vb, 0x01
    LD I, Line      ; Load line sprite
    DRW Va, Vb, 0x1 ; Draw line sprite
    SE Vb, V1       ; Skip if C has height of letter
    JP Draw_Column_C
    JP Draw_H

Draw_Column_C:

    ADD Vb, 0x01    ; Add position to Y
    LD I, Columm   ; Load column sprite
    DRW Va, Vb, 0x1
    SE Vb, 0x07       ; Skip repeate
    JP Draw_Column_C  ; Repeate Draw_Column
    JP Draw_Line_C

Draw_H:
    ADD Va, 0x05
    LD Vb, 0x01

Draw_Column_H:
    ADD Vb, 0x01    ; Add position to Y
    LD I, Columm   ; Load column sprite
    DRW Va, Vb, 0x1
    SE Vb, V1       ; Skip repeate
    JP Draw_Column_H  ; Repeate Draw_Column

RET


Line:
    DW 0x7000

Columm:
    DW 0x8000



