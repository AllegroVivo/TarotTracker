from __future__ import annotations

import logging
import os

from discord import Intents
from dotenv import load_dotenv

from Classes.Core.Bot import TarotTracker
################################################################################

load_dotenv()
DEBUG = os.getenv("DEBUG") == "True"

################################################################################

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

################################################################################

bot = TarotTracker(
    description="Track your tarot results and get daily readings!",
    intents=Intents.default(),
    debug_guilds=[
        955933227372122173,  # Bot Resources
        1273061765831458866,  # Kupo Nutz
    ] if DEBUG else None
)

################################################################################

for filename in os.listdir("Cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        bot.load_extension(f"Cogs.{filename[:-3]}")

################################################################################

token = os.getenv(("DEV" if DEBUG else "DISCORD") + "_TOKEN")
bot.run(token)

################################################################################
