def encode_decode_sequence(seq, symbol_assignments, encode=True):

    if encode:
        sequence = ''
    else:
        symbol_assignments = {y: x for x, y in symbol_assignments.items()}
        sequence = ''

    for symbol in seq:
        if symbol in symbol_assignments:
            sequence += symbol_assignments[symbol]
        else:
            pass
    return sequence