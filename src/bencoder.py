def encoder(value) -> bytes:
    if isinstance(value, int):
        return _encode_int(value)
    if isinstance(value, str):
        return _encode_str(value)
    if isinstance(value, list):
        return _encode_list(value)
    if isinstance(value, dict):
        return _encode_dict(value)
    raise TypeError("Not a valid type")