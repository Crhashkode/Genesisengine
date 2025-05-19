import os
from engine.flame_interface import mint_crk_token
from engine.withdraw_crk import withdraw_crk_token
from engine.trade import get_best_swap_route, execute_swap
from vault.vault import log_event

CRK_MINT = os.getenv("CRK_MINT_ADDRESS")
SOL_MINT = "So11111111111111111111111111111111111111112"

def handle_mint_request():
    mint_address = mint_crk_token()
    log_event("forge_mint", {"mint_address": mint_address})
    return f"[FORGE] CRK Minted: {mint_address}"

def handle_withdrawal_request(wallet: str, amount: float):
    tx = withdraw_crk_token(wallet, amount)
    log_event("forge_withdraw", {"to": wallet, "amount": amount, "tx": tx})
    return f"[FORGE] Withdrawn {amount} CRK to {wallet}\nTX: https://solscan.io/tx/{tx}"

def handle_swap_request(amount: float):
    raw = int(amount * 10**6)
    route = get_best_swap_route(CRK_MINT, SOL_MINT, raw)
    tx = execute_swap(route)
    log_event("forge_swap", {"amount": amount, "tx": tx})
    return f"[FORGE] Swapped {amount} CRK to SOL\nTX: https://solscan.io/tx/{tx}"