def validate_inputs(layer, fields):
    if layer is None:
        raise ValueError("Layer belum dipilih")

    if not fields:
        raise ValueError("Minimal satu field numerik dipilih")
