from vault.vault import log_event

def stealth_log(event: str, message: str):
    try:
        log_event("snake_log", {"event": event, "msg": message})
        return f"[SNAKE] Logged: {event} → {message}"
    except Exception as e:
        return f"[SNAKE ERROR] {str(e)}"