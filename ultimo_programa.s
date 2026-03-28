.text
.global _start
_start:
    @ Linha 1
    ldr r0, =const_3_5
    vldr.f64 d0, [r0]
    vpush {d0}
    ldr r0, =const_2_5
    vldr.f64 d0, [r0]
    vpop {d1}
    vadd.f64 d0, d1, d0
    ldr r0, =resultado_0
    vstr.f64 d0, [r0]
    @ Linha 2
    ldr r0, =const_10
    vldr.f64 d0, [r0]
    vpush {d0}
    ldr r0, =const_3
    vldr.f64 d0, [r0]
    vpop {d1}
    vsub.f64 d0, d1, d0
    ldr r0, =resultado_1
    vstr.f64 d0, [r0]
    @ Linha 3
    ldr r0, =const_4
    vldr.f64 d0, [r0]
    vpush {d0}
    ldr r0, =const_6
    vldr.f64 d0, [r0]
    vpop {d1}
    vmul.f64 d0, d1, d0
    ldr r0, =resultado_2
    vstr.f64 d0, [r0]
    @ Linha 4
    ldr r0, =const_8
    vldr.f64 d0, [r0]
    vpush {d0}
    ldr r0, =const_2
    vldr.f64 d0, [r0]
    vpop {d1}
    vdiv.f64 d0, d1, d0
    vpush {d0}
    ldr r0, =const_5
    vldr.f64 d0, [r0]
    vpush {d0}
    ldr r0, =const_3
    vldr.f64 d0, [r0]
    vpop {d1}
    vadd.f64 d0, d1, d0
    vpop {d1}
    vadd.f64 d0, d1, d0
    ldr r0, =resultado_3
    vstr.f64 d0, [r0]
    @ Linha 5
    ldr r0, =const_17
    vldr.f64 d0, [r0]
    vpush {d0}
    ldr r0, =const_5
    vldr.f64 d0, [r0]
    vpop {d1}
    vcvt.s32.f64 s2, d1
    vmov r1, s2
    vcvt.s32.f64 s0, d0
    vmov r2, s0
    bl divmod_i32
    vmov s0, r3
    vcvt.f64.s32 d0, s0
    ldr r0, =resultado_4
    vstr.f64 d0, [r0]
    @ Linha 6
    ldr r0, =const_17
    vldr.f64 d0, [r0]
    vpush {d0}
    ldr r0, =const_5
    vldr.f64 d0, [r0]
    vpop {d1}
    vcvt.s32.f64 s2, d1
    vmov r1, s2
    vcvt.s32.f64 s0, d0
    vmov r2, s0
    bl divmod_i32
    vmov s0, r0
    vcvt.f64.s32 d0, s0
    ldr r0, =resultado_5
    vstr.f64 d0, [r0]
    @ Linha 7
    ldr r0, =const_2
    vldr.f64 d0, [r0]
    vpush {d0}
    ldr r0, =const_5
    vldr.f64 d0, [r0]
    vpop {d1}
    vcvt.s32.f64 s0, d0
    vmov r0, s0
    vmov.f64 d0, d1
    bl pow_f64_i32
    ldr r0, =resultado_6
    vstr.f64 d0, [r0]
    @ Linha 8
    ldr r0, =const_42_75
    vldr.f64 d0, [r0]
    ldr r0, =mem_saldo
    vstr.f64 d0, [r0]
    ldr r0, =resultado_7
    vstr.f64 d0, [r0]
    @ Linha 9
    ldr r0, =mem_saldo
    vldr.f64 d0, [r0]
    vpush {d0}
    ldr r0, =const_7_25
    vldr.f64 d0, [r0]
    vpop {d1}
    vadd.f64 d0, d1, d0
    ldr r0, =resultado_8
    vstr.f64 d0, [r0]
    @ Linha 10
    ldr r0, =resultado_7
    vldr.f64 d0, [r0]
    vpush {d0}
    ldr r0, =resultado_8
    vldr.f64 d0, [r0]
    vpop {d1}
    vadd.f64 d0, d1, d0
    ldr r0, =resultado_9
    vstr.f64 d0, [r0]
    b fim_programa

divmod_i32:
    @ Entrada: r1=dividendo, r2=divisor
    @ Saida  : r3=quociente, r0=resto
    push {r5, r6, lr}
    mov r3, #0
    mov r0, #0
    cmp r2, #0
    beq fim_divmod_i32
    mov r5, #0
    mov r6, #0
    cmp r1, #0
    bge div_i32_dividendo_ok
    rsb r1, r1, #0
    mov r6, #1
    eor r5, r5, #1
div_i32_dividendo_ok:
    cmp r2, #0
    bge div_i32_divisor_ok
    rsb r2, r2, #0
    eor r5, r5, #1
div_i32_divisor_ok:
    mov r0, r1
div_i32_loop:
    cmp r0, r2
    blt div_i32_loop_fim
    sub r0, r0, r2
    add r3, r3, #1
    b div_i32_loop
div_i32_loop_fim:
    cmp r5, #0
    beq div_i32_sinal_resto
    rsb r3, r3, #0
div_i32_sinal_resto:
    cmp r6, #0
    beq fim_divmod_i32
    rsb r0, r0, #0
fim_divmod_i32:
    pop {r5, r6, pc}

pow_f64_i32:
    push {r4, lr}
    vmov.f64 d2, d0
    ldr r4, =const_1_0
    vldr.f64 d0, [r4]
    cmp r0, #0
    ble fim_pow
loop_pow:
    vmul.f64 d0, d0, d2
    subs r0, r0, #1
    bgt loop_pow
fim_pow:
    pop {r4, pc}

fim_programa:
    b fim_programa

.data
.align 3
const_0_0: .double 0.0
const_1_0: .double 1.0
const_10: .double 10
const_17: .double 17
const_2: .double 2
const_2_5: .double 2.5
const_3: .double 3
const_3_5: .double 3.5
const_4: .double 4
const_42_75: .double 42.75
const_5: .double 5
const_6: .double 6
const_7_25: .double 7.25
const_8: .double 8
mem_saldo: .double 0.0
resultado_0: .double 0.0
resultado_1: .double 0.0
resultado_2: .double 0.0
resultado_3: .double 0.0
resultado_4: .double 0.0
resultado_5: .double 0.0
resultado_6: .double 0.0
resultado_7: .double 0.0
resultado_8: .double 0.0
resultado_9: .double 0.0
