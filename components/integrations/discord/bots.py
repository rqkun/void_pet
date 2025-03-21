from datetime import datetime
import logging
import streamlit as st
import discord
from discord.ext import commands
import threading
import asyncio

from components.integrations.discord import functions

class DiscordBot:
    def __init__(self, token):
        self.token = token
        self.bot = None
        self.thread = None
        self.loop = None

    def start(self):
        if self.thread is None or not self.thread.is_alive():
            self.thread = threading.Thread(target=self._run_bot, daemon=True)
            self.thread.start()

    def _run_bot(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        intents = discord.Intents.default()
        intents.message_content = True
        intents.dm_messages = True
        self.bot = commands.Bot(command_prefix="/", intents=intents)
        self.bot.remove_command('help')

        @self.bot.event
        async def on_ready():
            await self.bot.tree.sync()
            logging.warning(f"Bot logged in as {self.bot.user}")
            activity = discord.Game(name="Warframe",platform="PC",start=datetime.now())
            await self.bot.change_presence(status=discord.Status.online, activity=activity)
            logging.info("Bot presence set to playing 'Warframe'")

        @self.bot.tree.command(name="help", description="Get the commands list.")
        async def help(interaction: discord.Interaction): 
            await functions.handle_context(interaction, functions.commands_embed)

        @self.bot.tree.command(name="worldstate", description="Get the planet cycles list.")
        async def worldstate(interaction: discord.Interaction): 
            await functions.handle_context(interaction, functions.worldstate_embed)

        @self.bot.tree.command(name="alerts", description="Get the alerts list.")
        async def alerts(interaction: discord.Interaction): 
            await functions.handle_context(interaction, functions.alerts_embed)

        @self.bot.tree.command(name="invasions", description="Get the invasion rewards list.")
        async def invasions(interaction: discord.Interaction): 
            await functions.handle_context(interaction, functions.invasions_embed)
        
        @self.bot.tree.command(name="void", description="Get the Baro Ki'ter info.")
        async def void(interaction: discord.Interaction): 
            await functions.handle_context(interaction, functions.void_trader_embed)

        @self.bot.tree.command(name="vault", description="Get the Varzia (Prime Resurgent) info.")
        async def vault(interaction: discord.Interaction): 
            await functions.handle_context(interaction, functions.vault_trader_embed)   

        try:
            self.loop.run_until_complete(self.bot.start(self.token))
        except asyncio.CancelledError:
            pass
        except discord.errors.LoginFailure as err:
            logging.error("Invalid Discord bot token.")
        finally:
            self.loop.run_until_complete(self.bot.close())
            self.loop.close()

    def stop(self):
        
        if self.loop and self.loop.is_running():
            asyncio.run_coroutine_threadsafe(self.bot.close(), self.loop)
            self.thread.join()
            self.thread = None
            self.loop = None
            self.bot = None
            logging.warning(f"Bot stopped")
            

    async def send_message(self, channel_id, message):
        if self.bot is None:
            logging.error("Bot is not running.")
            return
        channel = self.bot.get_channel(channel_id)
        if channel:
            await channel.send(message)
        else:
            logging.error("Channel not found")


@st.cache_resource
def start_bot():
    bot_instance = DiscordBot(st.secrets["discord"]["key"])
    bot_instance.start()
    return bot_instance
