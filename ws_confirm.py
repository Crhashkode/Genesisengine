import asyncio
import websockets
import json

async def confirm_signature(signature: str) -> bool:
    try:
        async with websockets.connect("wss://api.mainnet-beta.solana.com/") as ws:
            await ws.send(json.dumps({
                "jsonrpc": "2.0",
                "id": 1,
                "method": "signatureSubscribe",
                "params": [signature, {"commitment": "finalized"}]
            }))
            while True:
                response = await ws.recv()
                data = json.loads(response)
                if "result" in data and "value" in data["result"]:
                    return data["result"]["value"]["err"] is None
    except Exception as e:
        print(f"[WS ERROR] {e}")
        return False