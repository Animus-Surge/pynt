; Example LC-3 assembly code

.ORIG x3000
     LD R0, #10
     LD R1, #20
     ADD R2, R0, R1
     TRAP x25
.END
