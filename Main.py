import os
from engine.flame_interface import mint_crk_token, get_crk_balance, transfer_crk
from engine.trade import get_best_swap_route, execute_swap
from engine.withdraw_crk import withdraw_crk_token
from vault import log_event

# === Load Environment ===
CRK_MINT = os.getenv("CRK_MINT_ADDRESS")
SOL_MINT = "So11111111111111111111111111111111111111112"

def main():
    print("\n=== GENESIS ENGINE CONTROL PANEL ===")
    print("1. Mint CRK")
    print("2. Check Balance")
    print("3. Withdraw CRK")
    print("4. Swap CRK → SOL")
    print("====================================")

    choice = input("Select option: ").strip()

    try:
        if choice == "1":
            mint_address = mint_crk_token()
            if mint_address:
                print(f"[MINTED] CRK Token: {mint_address}")
                log_event("mint", {"mint_address": mint_address})
            else:
                raise Exception("Mint failed.")

        elif choice == "2":
            if not CRK_MINT:
                raise EnvironmentError("CRK_MINT_ADDRESS not set.")
            balance = get_crk_balance(CRK_MINT)
            print(f"[BALANCE] {balance} CRK")
            log_event("balance_check", {"mint": CRK_MINT, "balance": balance})

        elif choice == "3":
            recipient = input("Recipient Wallet Address: ").strip()
            amount = float(input("Amount of CRK to Send: ").strip())
            tx = withdraw_crk_token(recipient, amount)
            if tx and "signature" in tx:
                sig = tx["signature"]
                print(f"[WITHDRAWN] {amount} CRK → {recipient}")
                print(f"TX: https://solscan.io/tx/{sig}")
                log_event("withdraw", {"to": recipient, "amount": amount, "tx": sig})
            else:
                raise Exception(tx.get("message", "Withdraw failed."))

        elif choice == "4":
            amount = float(input("CRK Amount to Swap: "))
            raw = int(amount * 10**6)
            route = get_best_swap_route(CRK_MINT, SOL_MINT, raw)
            tx = execute_swap(route)
            if tx:
                print(f"[SWAPPED] {amount} CRK → SOL")
                print(f"TX: https://solscan.io/tx/{tx}")
                log_event("swap", {"amount": amount, "tx": tx})
            else:
                raise Exception("Swap failed.")

        else:
            raise ValueError("Invalid selection.")

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        log_event("error", {"action": choice, "reason": str(e)})

if __name__ == "__main__":
    main()
