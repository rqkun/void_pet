from datetime import datetime
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
        self.bot = commands.Bot(command_prefix="!", intents=intents)

        @self.bot.event
        async def on_ready():
            print(f"Bot logged in as {self.bot.user}")

        @self.bot.command()
        async def greet(ctx):
            await ctx.send(f"Hello, {ctx.author.name}!")
            print(f"{ctx.author.name} invoke !greet")
        
        @self.bot.command()
        async def invasions(ctx):
            data=data_manage.get_invasions_rewards(data_manage.get_world_state()["invasions"])
            if data is not None:
                embed = discord.Embed(title="Invasion Rewards", color=discord.Color.blue())
                for item,amount in data.items():
                    embed.add_field(name=item, value=amount, inline=False)
                await ctx.send(embed=embed)
            else:
                ctx.send("None")

        @self.bot.command()
        async def worldstate(ctx):
            data=data_manage.get_cycles()
            if data is not None:
                embed = discord.Embed(title="Worldstate", color=discord.Color.blue())
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
                embed = discord.Embed(title="Alert Rewards", color=discord.Color.blue())
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
        async def baro(ctx):
            data=VoidTraider()
            check=data.check()
            embed = discord.Embed(title="Baro Ki'ter", color=discord.Color.blue())
            embed.set_thumbnail(url=Warframe.DUCAT.value["image"])
            embed.add_field(name="Active", value=check["active"], inline=False)
            embed.add_field(name="Time", value=check["message"], inline=False)
            await ctx.send(embed=embed)
        
        @self.bot.command()
        async def varzia(ctx):
            data=VaultTraider()
            check=data.check()
            embed = discord.Embed(title="Varzia", color=discord.Color.blue())
            embed.set_thumbnail(url=Warframe.AYA.value["image"])
            embed.add_field(name="Active", value=check["active"], inline=False)
            embed.add_field(name="Time", value=check["message"], inline=False)
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
            print(f"Bot stopped")
            

    async def send_message(self, channel_id, message):
        if self.bot is None:
            print("Bot is not running.")
            return
        channel = self.bot.get_channel(channel_id)
        if channel:
            await channel.send(message)
        else:
            print("Channel not found")

@st.cache_resource
def get_discord():
    bot_instance = DiscordBot(st.secrets["discord"]["key"])
    bot_instance.start()
    return bot_instance