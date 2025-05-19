limport os
from engine.flame_interface import get_crk_balance
from vault.vault import log_event, current_nav

CRK_MINT = os.getenv("CRK_MINT_ADDRESS")

def handle_balance_query():
    try:
        if not CRK_MINT:
            raise ValueError("CRK_MINT_ADDRESS not set.")
        crk_balance = get_crk_balance(CRK_MINT)
        nav = current_nav()
        log_event("quanta_balance_check", {
            "crk_balance": crk_balance,
            "nav": nav
        })
        return f"[QUANTA] CRK: {crk_balance}, NAV: ${nav:.2f}"
    except Exception as e:
        log_event("quanta_error", {"error": str(e)})
        return f"[QUANTA ERROR] {str(e)}"