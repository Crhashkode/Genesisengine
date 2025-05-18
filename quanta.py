
class Quanta:
    def __init__(self, bot):
        self.bot = bot

    async def respond(self, ctx, message):
        try:
            await ctx.send(f"[Quanta]: {message}")
        except Exception as e:
            print(f"[QUANTA ERROR] {str(e)}")