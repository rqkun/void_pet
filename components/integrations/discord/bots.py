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
        self.bot = commands.Bot(command_prefix="!", intents=intents)
        self.bot.remove_command('help')
        
        @self.bot.event
        async def on_ready():
            await self.bot.tree.sync()
            logging.info(f"Bot logged in as {self.bot.user}")
            activity = discord.Game(name="Warframe",platform="PC",start=datetime.now())
            await self.bot.change_presence(status=discord.Status.online, activity=activity)
            logging.info("Bot presence set to playing 'Warframe'")
            
        @self.bot.event
        async def on_message(message):
            if message.author == self.bot.user:
                return

            ctx = await self.bot.get_context(message)
            if ctx.valid:
                await self.bot.process_commands(message)

        
        # Text Commands (Send in Channel)
        @self.bot.command()
        async def invasions(ctx:commands.Context): await functions.send_invasions(ctx)
        @self.bot.command()
        async def worldstate(ctx:commands.Context): await functions.send_worldstate(ctx)
        @self.bot.command()
        async def alerts(ctx:commands.Context): await functions.send_alerts(ctx)
        @self.bot.command()
        async def void(ctx:commands.Context): await functions.send_void_trader(ctx)
        @self.bot.command()
        async def vault(ctx:commands.Context): await functions.send_vault_trader(ctx)
        @self.bot.command()
        async def help(ctx:commands.Context): await functions.send_command_list(ctx)

        # Context Menu Commands (Send in DM)
        @self.bot.tree.context_menu(name="Invasions")
        async def run_invasions(interaction: discord.Interaction, user: discord.User):
            await functions.handle_context_menu(interaction, user, functions.send_invasions, self.bot.user.id)

        @self.bot.tree.context_menu(name="Worldstate")
        async def run_worldstate(interaction: discord.Interaction, user: discord.User):
            await functions.handle_context_menu(interaction, user, functions.send_worldstate, self.bot.user.id)

        @self.bot.tree.context_menu(name="Alerts")
        async def run_alerts(interaction: discord.Interaction, user: discord.User):
            await functions.handle_context_menu(interaction, user, functions.send_alerts, self.bot.user.id)

        @self.bot.tree.context_menu(name="Baro Ki'ter")
        async def run_void_trader(interaction: discord.Interaction, user: discord.User):
            await functions.handle_context_menu(interaction, user, functions.send_void_trader, self.bot.user.id)

        @self.bot.tree.context_menu(name="Varzia")
        async def run_vault_trader(interaction: discord.Interaction, user: discord.User):
            await functions.handle_context_menu(interaction, user, functions.send_vault_trader, self.bot.user.id)

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
            logging.info(f"Bot stopped")
            

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
def get_discord():
    bot_instance = DiscordBot(st.secrets["discord"]["key"])
    bot_instance.start()
    return bot_instance
