from bencoder import encoder
from bencoder import decoder
import torrent
import random
import socket
import logging
import aiohttp
from struct import unpack
from urllib.parse import urlencode


def generate_peer_ID() -> str:
    return "-ZEPHYR-" + "".join(str(random.randint(0, 9)) for i in range(12))


# generation test
# myid = generate_peer_ID()
# print(myid)

async def announce(torrent, peer_id: str, downloaded: int=0, uploaded: int=0, first: bool=false) -> dict:
    
