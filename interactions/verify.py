# interactions/verify.py
# Not used by the app itself—just a tiny util you can import later if you want.
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError


def verify(
    public_key_hex: str, timestamp: str, body: bytes, signature_hex: str
) -> bool:
    try:
        VerifyKey(bytes.fromhex(public_key_hex)).verify(
            f"{timestamp}{body.decode()}".encode(), bytes.fromhex(signature_hex)
        )
        return True
    except BadSignatureError:
        return False
