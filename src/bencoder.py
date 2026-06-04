def encoder(value) -> bytes:
    if isinstance(value, bool):
        raise TypeError("Can't have bool in the torrent file")
    
    if isinstance(value, int):
        return _encode_int(value)
    
    if isinstance(value, str):
        return _encode_str(value)
    
    if isinstance(value, bytes):
        return _encode_bytes(value)
    
    if isinstance(value, list):
        return _encode_list(value)
    
    if isinstance(value, dict):
        return _encode_dict(value)
    
    raise TypeError("Not a valid type")

def _encode_int(value: int) -> bytes:
    return b"i" + (str(value)).encode() + b"e"

def _encode_str(value: str) -> bytes:
    return (str(len(value.encode()))).encode() + b":" + value.encode()
    # wrote encode two times here ^, since special characters like é have different length than e
    # therefore first encoded the string then checked the length of the encoded string
    # and then finally encoded it back gain
    
def _encode_bytes(value: bytes) -> bytes:
    return (str(len(value))).encode() + b":" + value

def _encode_list(value: list) -> bytes:
    result = b"l"
    for items in value:
        result += encoder(items)
    return result + b"e"

def _encode_dict(value: dict) -> bytes:
    final = b"d"
    for itemkey in sorted(value):
        if not isinstance(itemkey, (str, bytes)):
            raise TypeError("Dictionary keys must be strings or bytes")
        final += encoder(itemkey)
        final += encoder(value[itemkey])
    return final + b"e"

#  encoder testing
#
#  print(encoder(10)) 
# print(encoder("hello"))
# a = b"hi"
# print(encoder(a))
# testlist = [1, "applehai", [2,3,4], 23, b"thisabyte"]
# print(encoder(testlist))
# torrent = {
#     "announce": "http://tracker.example.com",
#     "info": {
#         "name": "ubuntu.iso",
#         "piece length": 262144,
#         "length": 1048576
#     }
# }
# print(encoder(torrent))