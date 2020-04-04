; This program just show all sprites previous loaded in memory
; Author: Alexandre Barbieri (fakeezz@gmail.com)

; VA = Position X
; VB = Position Y
; VC = Current Sprite

; Load Default values
LD VA, 0
LD VB, 0
LD VC, 0

; Loop program
Loop:
    SNE VA, 50 ; if position x has not reached column 60 do not go to jump line
    CALL Jump_Line ; call jump line
    SNE VC, 80 ; if has loaded all sprite just end the program
    JP Exit ; exit program
    CALL Draw_Sprite
    JP Loop

Draw_Sprite:
    ADD VA, 5 ; shift cursor 5 pixels
    LD F, VC ; set register I to VC sprite
    ADD VC, 5 ; move to next sprite
    DRW VA, VB, 5 ; draw sprite
    RET

; Jump line routine
Jump_Line:
    LD VA, 0
    ADD VB, 5
    RET

; End of program
Exit:
    JP Exit
