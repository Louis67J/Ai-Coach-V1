import discord
from discord.ext import commands
from openai import OpenAI
from config import DISCORD_BOT_TOKEN, DISCORD_CHANNEL_ID, OPENAI_API_KEY, OPENAI_MODEL

client_ai = OpenAI(api_key=OPENAI_API_KEY)

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f"Bot connecté : {bot.user}")

@bot.command()
async def coach(ctx, *, message):
    """
    Commande : !coach ton texte
    Discute avec ton IA.
    """

    response = client_ai.responses.create(
        model=OPENAI_MODEL,
        input=message
    )

    await ctx.send(response.output_text)

def run_discord_bot():
    bot.run(DISCORD_BOT_TOKEN)
