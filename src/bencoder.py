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

def decoder(data: bytes):

    if not isinstance(data, bytes):
        raise TypeError("The file data should be in bytes")

    value, pos = _decode_value(data, 0)

    if(pos!=len(data)):
        raise ValueError("Unexpected data field encountered")

    return value

def _decode_value(data: bytes, pos: int):
    identifier = data[pos:pos+1]
    
    if identifier == b"i":
        return _decode_int(data, pos)
    
    if identifier.isdigit():
        return _decode_strbytes(data,pos)
    
    if identifier == b"l":
        return _decode_list(data, pos)
    
    if identifier == b"d":
        return _decode_dict(data,pos)

    raise ValueError(f"Invalid Token found at {pos}")

def _decode_int(data: bytes, pos: int):
    end = data.index(b"e", pos+1)
    dataint = (data[pos+1:end]).decode()
    if dataint == "-0":
        raise ValueError("No negative zeros allowed in bencode")
    if dataint != "0" and (dataint.lstrip("-")).startswith("0"):
        raise ValueError("Leading zero not allowed in bencode")
    return int(dataint), end+1

def _decode_strbytes(data: bytes, pos: int):
    colon = data.index(b":",pos)
    length = int((data[pos:colon]).decode())
    start = colon+1
    end = start +length
    if end > len(data):
        raise ValueError("Data out of bounds")
    return data[start:end],end

def _decode_list(data:bytes, pos:int):
    result_list = []
    pos = pos+1
    while(data[pos:pos+1] != b"e"):
        itemtoappend, pos = _decode_value(data, pos)
        result_list.append(itemtoappend)
    return result_list, pos+1

def _decode_dict(data:bytes, pos:int):
    result_dict = {}
    pos += 1
    while(data[pos:pos+1] != b"e"):
        keytoappend, pos = _decode_value(data, pos)
        valuetoappend, pos = _decode_value(data, pos)
        result_dict[keytoappend] = valuetoappend
    return result_dict, pos+1

# decoder test
#
# print(type(decoder(b"i42e")))
# print(decoder(b"i42e"))
# testa =b"5:apple"
# print(type(decoder(testa)))
# print(decoder(testa))
# print(decoder(b"li1ei2ee"))
# print(decoder(b"d4:infod4:name10:ubuntu.iso6:lengthi1048576e12:piece lengthi262144e6:pieces20:abcdefghijklmnopqrste8:announce29:http://tracker.local/announce7:comment12:Test torrente"))

with open("tests/ubuntu-26.04-desktop-amd64.iso.torrent", "rb") as f:
    raw = f.read()

decoded = decoder(raw)

print(decoded.keys())
print(decoded[b"info"].keys())