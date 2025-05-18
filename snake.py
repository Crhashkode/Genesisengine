class Snake:
    def fallback(self, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"[SNAKE RECOVERY] {str(e)}")
            return None