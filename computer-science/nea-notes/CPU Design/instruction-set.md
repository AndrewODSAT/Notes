This is the mapping of an instruction at a certain stage to its micro-operations. This can be used to decode instructions using a FSM where each stage is actually the state and the opcode is the input. Then store the stage to micro-operation in a non-volatile memory.
![[micro-op-table]]

The CPU design looks like this:
![[cpu-design]]