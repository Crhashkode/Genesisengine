from Trinode.quanta import handle_balance_query
from Trinode.forge import handle_mint_request, handle_withdrawal_request, handle_swap_request
from Trinode.snake import stealth_log
from vault.vault import log_event

def dispatch_command(command: str, *args):
    try:
        if command == "mint":
            return handle_mint_request()
        elif command == "balance":
            return handle_balance_query()
        elif command == "withdraw":
            if len(args) != 2:
                return "Usage: withdraw <wallet> <amount>"
            wallet, amount = args
            return handle_withdrawal_request(wallet, float(amount))
        elif command == "swap":
            if len(args) != 1:
                return "Usage: swap <amount>"
            return handle_swap_request(float(args[0]))
        elif command == "stealth":
            return stealth_log(*args)
        else:
            return f"Unknown command: {command}"
    except Exception as e:
        log_event("trinode_error", {"command": command, "error": str(e)})
        return f"[TRINODE ERROR] {str(e)}"