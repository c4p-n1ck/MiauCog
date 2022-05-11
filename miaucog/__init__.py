from .miaucog import MiauCog


def setup(bot):
    bot.add_cog(MiauCog(bot))
