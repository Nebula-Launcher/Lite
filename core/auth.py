import hashlib
import uuid


def get_offline_uuid(username: str) -> str:
    digest = hashlib.md5(("OfflinePlayer:" + username).encode("utf-8")).digest()
    ba = bytearray(digest)
    ba[6] = (ba[6] & 0x0F) | 0x30
    ba[8] = (ba[8] & 0x3F) | 0x80
    return str(uuid.UUID(bytes=bytes(ba)))


def get_offline_options(username: str) -> dict:
    return {
        "username": username,
        "uuid": get_offline_uuid(username),
        "token": "0",
    }
