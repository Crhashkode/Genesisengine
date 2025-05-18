import json, os, time
from decimal import Decimal
from datetime import datetime
from pathlib import Path

VAULT_PATH = Path(__file__).parent / "vault.json"


# ════════════ low-level helpers ════════════
def _load():
    if not VAULT_PATH.exists():
        raise FileNotFoundError("vault.json not found")
    with open(VAULT_PATH, "r") as f:
        return json.load(f)


def _save(vault: dict):
    vault["updated"] = datetime.utcnow().isoformat()
    with open(VAULT_PATH, "w") as f:
        json.dump(vault, f, indent=2)


# ════════════ public API ═══════════════════
def log_event(event_type: str, data: dict):
    """Append an event to the rolling log."""
    v = _load()
    v.setdefault("logs", []).append({
        "ts":   datetime.utcnow().isoformat(),
        "type": event_type,
        "data": data
    })
    # keep last 500 entries max
    v["logs"] = v["logs"][-500:]
    _save(v)


def record_mint(mint_sig: str, crk_amount: int, usd_val: float):
    """Track freshly-minted CRK as revenue and update balances."""
    v = _load()
    # --- update revenue bucket
    rev = v.setdefault("revenue", {})
    rev["total_mined_usd"]  = float(Decimal(rev.get("total_mined_usd", 0))  + Decimal(usd_val))
    rev["total_mined_crk"]  = int(rev.get("total_mined_crk", 0) + crk_amount)
    rev.setdefault("streams", []).append({
        "date": datetime.utcnow().date().isoformat(),
        "source": "Engine Mint",
        "usd": usd_val,
        "crk": crk_amount,
        "tx":  mint_sig
    })
    # --- update liquid CRK balance
    crk = v["balances"]["CRK"]
    crk["raw"]    += crk_amount
    crk["amount"]  = crk["raw"] / 1_000_000    # 6-decimals
    _save(v)
    log_event("mint_recorded", {"tx": mint_sig, "crk_raw": crk_amount})


def update_balance(symbol: str, raw_amount: int, usd_price: float):
    """Overwrite a balance slot from on-chain fetch."""
    v = _load()
    slot = v["balances"].setdefault(symbol, {})
    slot["raw"]    = raw_amount
    slot["amount"] = raw_amount / (1_000_000 if symbol != "SOL" else 1_000_000_000)
    slot["usd"]    = float(slot["amount"] * Decimal(usd_price))
    _save(v)
    log_event("balance_sync", {"symbol": symbol, "raw": raw_amount})


def current_nav() -> float:
    """Return portfolio Net-Asset-Value in USD."""
    v = _load()
    return float(sum(b["usd"] for b in v["balances"].values()))