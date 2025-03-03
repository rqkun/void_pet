from datetime import datetime
import logging
import streamlit as st
import discord
from discord.ext import commands
import threading
import asyncio

from config.classes.vendors import VaultTraider, VoidTraider
from config.constants import Warframe
from utils import data_manage, tools

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
            activity = discord.Game(name="Warframe")
            await self.bot.change_presence(status=discord.Status.online, activity=activity)
            logging.info("Bot presence set to playing 'Warframe'")
            
        @self.bot.event
        async def on_message(message):
            if message.author == self.bot.user:
                return

            ctx = await self.bot.get_context(message)
            if ctx.valid:
                await self.bot.process_commands(message)

        async def send_invasions(destination):
            """Helper function to send invasion rewards."""
            data = data_manage.get_invasions_rewards(data_manage.get_world_state()["invasions"])
            if data:
                embed = discord.Embed(title="Invasion Rewards", color=discord.Color.blue())
                embed.set_footer(icon_url=Warframe.MODE_ICONS.value["INVASION"], text="via Voidpet | Hosted on Streamlit")
                for item, amount in data.items():
                    embed.add_field(name=item, value=amount, inline=False)
                await destination.send(embed=embed)
            else:
                await destination.send("❌ No active invasions.")

        async def send_worldstate(destination):
            """Helper function to send world state info."""
            data = data_manage.get_cycles()
            if data:
                embed = discord.Embed(title="Worldstate", color=discord.Color.blue(), url=f"""{st.secrets.host.cloud}""")
                embed.set_footer(icon_url=Warframe.MODE_ICONS.value["OPEN_WORLD"], text="via Voidpet | Hosted on Streamlit")
                for item in data:
                    span = datetime.strptime(item["data"]["expiry"], "%Y-%m-%dT%H:%M:%S.%fZ") - datetime.today()
                    time = tools.format_timedelta(span, day=False) if span.total_seconds() > 0 else "Expired"
                    embed.add_field(name=item["name"], value=f"""{item["data"]["state"].title()}: {time}""", inline=True)
                await destination.send(embed=embed)
            else:
                await destination.send("❌ No active world state.")

        async def send_alerts(destination):
            """Helper function to send alert rewards."""
            data = data_manage.get_alerts_data()
            if data:
                embed = discord.Embed(title="Alert Rewards", color=discord.Color.blue(), url=f"""{st.secrets.host.cloud}""")
                embed.set_footer(icon_url=Warframe.MODE_ICONS.value["ALERT"], text="via Voidpet | Hosted on Streamlit")
                for alert in data:
                    if alert["active"]:
                        time = tools.format_timedelta(datetime.strptime(alert["expiry"], "%Y-%m-%dT%H:%M:%S.%fZ") - datetime.today(), day=True)
                        rewards = ", ".join(f"""{reward["amount"]:,} {reward["item"]}""" for reward in data_manage.get_alert_reward(alert))
                        embed.add_field(name=alert["mission"]["node"], value=rewards, inline=False)
                await destination.send(embed=embed)
            else:
                await destination.send("❌ No active alerts.")

        async def send_void_trader(destination):
            """Helper function to send Void Trader info."""
            data = VoidTraider().check()
            embed = discord.Embed(title="Baro Ki'teer", color=discord.Color.blue(), url=f"""{st.secrets.host.cloud}void""")
            embed.set_footer(icon_url=Warframe.DUCAT.value["image"], text="via Voidpet | Hosted on Streamlit")
            embed.add_field(name="Active", value=data["active"], inline=True)
            embed.add_field(name="Time", value=data["message"], inline=True)
            await destination.send(embed=embed)

        async def send_vault_trader(destination):
            """Helper function to send Vault Trader info."""
            data = VaultTraider().check()
            embed = discord.Embed(title="Varzia", color=discord.Color.blue(), url=f"""{st.secrets.host.cloud}vault""")
            embed.set_footer(icon_url=Warframe.AYA.value["image"], text="via Voidpet | Hosted on Streamlit")
            embed.add_field(name="Active", value=data["active"], inline=True)
            embed.add_field(name="Time", value=data["message"], inline=True)
            await destination.send(embed=embed)

        # Text Commands (Send in Channel)
        @self.bot.command()
        async def invasions(ctx): await send_invasions(ctx)
        @self.bot.command()
        async def worldstate(ctx): await send_worldstate(ctx)
        @self.bot.command()
        async def alerts(ctx): await send_alerts(ctx)
        @self.bot.command()
        async def void(ctx): await send_void_trader(ctx)
        @self.bot.command()
        async def vault(ctx): await send_vault_trader(ctx)

        # Context Menu Commands (Send in DM)
        @self.bot.tree.context_menu(name="Run Invasions")
        async def run_invasions(interaction: discord.Interaction, user: discord.User):
            await handle_context_menu(interaction, user, send_invasions)

        @self.bot.tree.context_menu(name="Run Worldstate")
        async def run_worldstate(interaction: discord.Interaction, user: discord.User):
            await handle_context_menu(interaction, user, send_worldstate)

        @self.bot.tree.context_menu(name="Run Alerts")
        async def run_alerts(interaction: discord.Interaction, user: discord.User):
            await handle_context_menu(interaction, user, send_alerts)

        @self.bot.tree.context_menu(name="Run Void Trader")
        async def run_void_trader(interaction: discord.Interaction, user: discord.User):
            await handle_context_menu(interaction, user, send_void_trader)

        @self.bot.tree.context_menu(name="Run Vault Trader")
        async def run_vault_trader(interaction: discord.Interaction, user: discord.User):
            await handle_context_menu(interaction, user, send_vault_trader)

        async def handle_context_menu(interaction, user, function):
            """Handles sending messages based on context menu."""
            if user == interaction.user or user == self.bot.user:
                try:
                    await function(user)  # DM the user
                    await interaction.response.send_message("✅ Check your DMs.", ephemeral=True)
                except discord.Forbidden:
                    await interaction.response.send_message("❌ I can't DM you. Check your privacy settings.", ephemeral=True)
            else:
                await interaction.response.send_message("❌ You can only run this command on yourself or the bot.", ephemeral=True)

        
        try:
            self.loop.run_until_complete(self.bot.start(self.token))
        except asyncio.CancelledError:
            pass
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