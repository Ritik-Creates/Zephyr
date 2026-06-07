from bencoder import encoder
from bencoder import decoder
from hashlib import sha1
from collections import namedtuple  

TorrentFile = namedtuple("TorrentFile", ["name", "length"])

def load(filename: str) -> dict:
    with open(filename, "rb") as f:
        return decoder(f.read())

def get_info_hash(meta: dict) -> bytes:
    return sha1(encoder(meta[b"info"])).digest()

def get_announce(meta: dict) -> str:
    return meta[b"announce"].decode()

def get_piece_length(meta: dict) -> int:
    return meta[b"info"][b"piece length"]

def get_pieces(meta: dict) -> list[bytes]:
    piece_data = meta[b"info"][b"pieces"]
    return [piece_data[i:i+20] for i in range(0, len(piece_data), 20)]

def is_multiple_files(meta: dict) -> bool:
    return b"files" in meta[b"info"]

def get_files(meta: dict) -> list[TorrentFile]:
    if (is_multiple_files(meta)):
        return [TorrentFile(name="/".join(p.decode() for p in f[b"path"]), length=f[b"length"]) for f in meta[b"info"][b"files"]]
    
    return [TorrentFile(name=(meta[b"info"][b"name"].decode()), length=meta[b"info"][b"length"])]

def get_total_size(meta: dict) -> int:
    return sum(f.length for f in get_files(meta))

def get_output_file(meta: dict) -> str:
    return meta[b"info"][b"name"].decode()

def torrent_format(meta: dict) -> str:
    files = get_files(meta)
    return (
        f"File Name:    {get_output_file(meta)}\n" 
        f"File Size:    {get_total_size(meta)}\n" 
        f"Tracker URL:  {get_announce(meta)}\n" 
        f"Info Hash:    {get_info_hash(meta).hex()}\n" 
        f"Pieces:       {len(get_pieces(meta))} x {get_piece_length(meta)} bytes\n" 
        f"All files:    {', '.join(f.name for f in files)}"
    )
