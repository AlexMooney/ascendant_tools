import json
from random import randint

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

from ascendant_roller import AscendantRoller
from amalgam_roller import AmalgamRoller

PUBLIC_KEY = "PUBLIC_KEY_HERE"
PING_PONG = {"type": 1}
RESPONSE_TYPES =  {
        "PONG": 1,
        "ACK_NO_SOURCE": 2,
        "MESSAGE_NO_SOURCE": 3,
        "MESSAGE_WITH_SOURCE": 4,
        "ACK_WITH_SOURCE": 5
    }


def verify_signature(event):
    raw_body = event.get("rawBody")
    auth_sig = event['params']['header'].get('x-signature-ed25519')
    auth_ts  = event['params']['header'].get('x-signature-timestamp')

    message = auth_ts.encode() + raw_body.encode()
    verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
    verify_key.verify(message, bytes.fromhex(auth_sig)) # raises an error if unequal

def ping_pong(body):
    if body.get("type") == 1:
        return True
    return False

def _get_int_argument(body):
    return int(body['data']['options'][0]['value'])

def lambda_handler(event, context):
    try:
        verify_signature(event)
    except Exception as e:
        raise Exception(f"[UNAUTHORIZED] Invalid request signature: {e}")

    body = event.get('body-json')
    if ping_pong(body):
        return PING_PONG

    content = "Failed to figure out what you asked!  Please report bug to @malex."
    name = body.get("data", {}).get("name")

    if body.get("type") != 2:
        pass
    elif name == "attack":
        rv = _get_int_argument(body)
        content = AscendantRoller().roll_attack(rv)
    elif name == "chart":
        rv = _get_int_argument(body)
        content = AscendantRoller().roll_chart(rv)
    elif name == "init":
        initiative = _get_int_argument(body)
        content = f"Initiative roll with {initiative}.  Result: {initiative + randint(1, 10)}"
    elif name == "opposed":
        rv = _get_int_argument(body)
        content = AmalgamRoller().roll_opposed(rv)
    elif name == "check":
        rv = _get_int_argument(body)
        content = AmalgamRoller().roll_check(rv)

    return {
            "type": RESPONSE_TYPES['MESSAGE_WITH_SOURCE'],
            "data": {
                "tts": False,
                "content": content,
                "embeds": [],
                "allowed_mentions": []
            }
        }
