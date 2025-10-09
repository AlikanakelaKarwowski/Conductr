# interactions/main.py
import os
import json
from fastapi import FastAPI, Request, HTTPException
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="interactions")

PUBLIC_KEY = os.environ.get("DISCORD_PUBLIC_KEY")
if not PUBLIC_KEY:
    raise RuntimeError("Set DISCORD_PUBLIC_KEY in env.")
verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))


# simple health check
@app.get("/healthz")
def healthz():
    return {"ok": True}


def verify_discord_request(request: Request, body: bytes):
    sig = request.headers.get("x-signature-ed25519")
    ts = request.headers.get("x-signature-timestamp")
    if not sig or not ts:
        raise HTTPException(status_code=401, detail="missing signature headers")
    try:
        verify_key.verify(ts.encode() + body, bytes.fromhex(sig))
    except BadSignatureError:
        raise HTTPException(status_code=401, detail="invalid request signature")


@app.post("/interactions")
async def interactions(request: Request):
    body = await request.body()
    verify_discord_request(request, body)
    payload = json.loads(body)

    t = payload.get("type")
    # 1 = PING
    if t == 1:
        return {"type": 1}

    # 2 = APPLICATION_COMMAND
    data = payload.get("data", {})
    name = data.get("name")

    if name == "ping":
        # 4 = CHANNEL_MESSAGE_WITH_SOURCE (immediate response)
        return {"type": 4, "data": {"content": "pong 🏓"}}

    return {"type": 4, "data": {"content": "Unknown command."}}
