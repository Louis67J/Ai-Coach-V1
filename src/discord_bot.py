# src/discord_bot.py
import os
import discord
from discord.ext import commands
from pathlib import Path
from coach import ask_ai_freeform, ask_ai_for_plan

DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID", "0"))
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot ready: {bot.user}")

@bot.command(name="coach")
async def cmd_coach(ctx):
    # load last summary
    p = OUTPUT_DIR / "summary.txt"
    if p.exists():
        await ctx.send("Résumé coach:\n" + p.read_text()[:1900])
    else:
        await ctx.send("Aucun résumé disponible. Lance le pipeline d'abord.")

@bot.command(name="plan")
async def cmd_plan(ctx, days: int = 7):
    # build plan using profile file
    from analysis.profile_utils import load_profile
    profile = load_profile()
    plan = ask_ai_for_plan(profile, horizon_days=days)
    # cut to message size
    for chunk in [plan[i:i+1900] for i in range(0, len(plan), 1900)]:
        await ctx.send(chunk)

@bot.command(name="ask")
async def cmd_ask(ctx, *, question: str):
    await ctx.send("Interroge l'IA...")
    ans = ask_ai_freeform(question)
    for chunk in [ans[i:i+1900] for i in range(0, len(ans), 1900)]:
        await ctx.send(chunk)

@bot.command(name="plot")
async def cmd_plot(ctx, which: str):
    if which.lower() == "ctl":
        p = OUTPUT_DIR / "ctl_atl.png"
    elif which.lower() == "power":
        p = OUTPUT_DIR / "power_curve.png"
    elif which.lower() == "zones":
        p = OUTPUT_DIR / "zone_dist.png"
    else:
        await ctx.send("Usage: !plot ctl|power|zones")
        return
    if p.exists():
        await ctx.send(file=discord.File(str(p)))
    else:
        await ctx.send("Graph not found. Génère le pipeline d'abord.")

def run_bot():
    if not DISCORD_TOKEN:
        print("No DISCORD_TOKEN set.")
        return
    bot.run(DISCORD_TOKEN)

if __name__ == "__main__":
    run_bot()
