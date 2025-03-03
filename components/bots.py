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
                return  # Ignore bot's own messages

            # Check if it's a DM and ensure only valid commands are processed
            if isinstance(message.channel, discord.DMChannel):
                ctx = await self.bot.get_context(message)
                if ctx.valid:
                    await self.bot.process_commands(message)  # Handle valid command
                else:
                    await message.channel.send("❌ Invalid command. Use `!help` for a list of commands.")

            else:
                await self.bot.process_commands(message)  # Handle server messages

        @self.bot.tree.context_menu(name="Run Invasions")
        async def run_invasions(interaction: discord.Interaction, user: discord.User):
            """Allows user to trigger the `!invasions` command from context menu."""
            if user == interaction.user:
                ctx = await self.bot.get_context(interaction)
                command = self.bot.get_command("invasions")
                if command:
                    await command.invoke(ctx)  # Run the invasion command
                    await interaction.response.send_message("✅ Running `!invasions`", ephemeral=True)
                else:
                    await interaction.response.send_message("❌ Command not found.", ephemeral=True)
            else:
                await interaction.response.send_message("❌ You can only run commands on yourself.", ephemeral=True)

        @self.bot.command()
        async def help(ctx):
            embed = discord.Embed(title="Commands", color=discord.Color.blue())
            embed.set_footer(icon_url=Warframe.MODE_ICONS.value["ALERT"],text="via Voidpet | Hosted on Streamlit")
            embed.add_field(name="!help", value="A command that show you this!", inline=False)
            embed.add_field(name="!worldstate", value="A command that show the ingame planet cycles!", inline=False)
            embed.add_field(name="!invasions", value="A command that show potential invasion rewards!", inline=False)
            embed.add_field(name="!alerts", value="A command that show alert info and rewards!", inline=False)
            embed.add_field(name="!void", value="A command that show Prime Resurgent duration!", inline=False)
            embed.add_field(name="!vault", value="A command that show Baro Kit'er ETA!", inline=False)
            try:
                await ctx.author.send(embed=embed)  # Send private message to the user
                await ctx.message.add_reaction("📩")  # Confirm with reaction
            except discord.Forbidden:
                await ctx.send("❌ I can't DM you! Please check your privacy settings.")
        
        @self.bot.command()
        async def invasions(ctx):
            data=data_manage.get_invasions_rewards(data_manage.get_world_state()["invasions"])
            if data is not None:
                embed = discord.Embed(title="Invasion Rewards", color=discord.Color.blue())
                embed.set_footer(icon_url=Warframe.MODE_ICONS.value["INVASION"],text="via Voidpet | Hosted on Streamlit")
                for item,amount in data.items():
                    embed.add_field(name=item, value=amount, inline=False)
                await ctx.send(embed=embed)
            else:
                ctx.send("None")

        @self.bot.command()
        async def worldstate(ctx):
            data=data_manage.get_cycles()
            if data is not None:
                embed = discord.Embed(title="Worldstate", color=discord.Color.blue(),url=f"""{st.secrets.host.cloud}""")
                embed.set_footer(icon_url=Warframe.MODE_ICONS.value["OPEN_WORLD"],text="via Voidpet | Hosted on Streamlit")
                for item in data:
                    span = datetime.strptime(item["data"]["expiry"],"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today()
                    if span.total_seconds() >0:
                        time = tools.format_timedelta(span,day=False)
                    else: time = tools.format_timedelta(datetime.today()-datetime.today(),day=False)
                    embed.add_field(name=item["name"], value=f"""{item["data"]["state"].title()}: {time}""", inline=True)
                await ctx.send(embed=embed)
            else:
                ctx.send("None")

        @self.bot.command()
        async def alerts(ctx):
            data=data_manage.get_alerts_data()
            if data is not None:
                embed = discord.Embed(title="Alert Rewards", color=discord.Color.blue(),url=f"""{st.secrets.host.cloud}""")
                embed.set_footer(icon_url=Warframe.MODE_ICONS.value["ALERT"],text="via Voidpet | Hosted on Streamlit")
                for alert in data:
                    if alert["active"] == True:
                        time = tools.format_timedelta(datetime.strptime(alert["expiry"],"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.today(),day=True)
                        rewards = data_manage.get_alert_reward(alert)
                    rewards_list = []
                    for reward in rewards:
                        rewards_list.append(f"""{reward["amount"]:,} {reward["item"]}""")
                    rewards_string = ", ".join(rewards_list)
                    embed.add_field(name=alert["mission"]["node"], value=rewards_string, inline=False)
                await ctx.send(embed=embed)
            else:
                ctx.send("None")
        
        @self.bot.command()
        async def void(ctx):
            data=VoidTraider()
            check=data.check()
            embed = discord.Embed(title="Baro Ki'ter", color=discord.Color.blue(),url=f"""{st.secrets.host.cloud}void""")
            embed.set_footer(icon_url=Warframe.DUCAT.value["image"],text="via Voidpet | Hosted on Streamlit")
            embed.add_field(name="Active", value=check["active"], inline=True)
            embed.add_field(name="Time", value=check["message"], inline=True)
            await ctx.send(embed=embed)
        
        @self.bot.command()
        async def vault(ctx):
            data=VaultTraider()
            check=data.check()
            embed = discord.Embed(title="Varzia", color=discord.Color.blue(),url=f"""{st.secrets.host.cloud}vault""")
            embed.set_footer(icon_url=Warframe.AYA.value["image"],text="via Voidpet | Hosted on Streamlit")
            embed.add_field(name="Active", value=check["active"], inline=True)
            embed.add_field(name="Time", value=check["message"], inline=True)
            await ctx.send(embed=embed)
        
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