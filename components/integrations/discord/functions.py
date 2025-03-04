from datetime import datetime
from typing import Union
import streamlit as st
import discord
from discord.ext import commands
import urllib

from config.classes.vendors import VaultTraider, VoidTraider
from config.constants import Warframe
from utils import data_manage, tools

async def send_command_list(ctx:commands.Context):
    embed = discord.Embed(title="Commands", color=discord.Color.blue())
    embed.set_footer(icon_url=Warframe.MODE_ICONS.value["ALERT"],text="via Voidpet | Hosted on Streamlit")
    embed.add_field(name="!help", value="A command that show you this!", inline=False)
    embed.add_field(name="!worldstate", value="A command that show the ingame planet cycles!", inline=False)
    embed.add_field(name="!invasions", value="A command that show potential invasion rewards!", inline=False)
    embed.add_field(name="!alerts", value="A command that show alert info and rewards!", inline=False)
    embed.add_field(name="!void", value="A command that show Prime Resurgent duration!", inline=False)
    embed.add_field(name="!vault", value="A command that show Baro Ki'ter ETA!", inline=False)
    try:
        await ctx.author.send(embed=embed)
        await ctx.message.add_reaction("📩")
    except discord.Forbidden:
        await ctx.send("❌ I can't DM you! Please check your privacy settings.")


async def send_invasions(destination:Union[discord.User, discord.Member]):
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


async def send_worldstate(destination:Union[discord.User, discord.Member]):
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


async def send_alerts(destination:Union[discord.User, discord.Member]):
    """Helper function to send alert rewards."""
    data = data_manage.get_alerts_data()
    if data:
        embed = discord.Embed(title="Alert Rewards", color=discord.Color.blue(), url=f"""{st.secrets.host.cloud}""")
        embed.set_footer(icon_url=Warframe.MODE_ICONS.value["ALERT"], text="via Voidpet | Hosted on Streamlit")
        for alert in data:
            if alert["active"]:
                time = tools.format_timedelta(datetime.strptime(alert["expiry"], "%Y-%m-%dT%H:%M:%S.%fZ") - datetime.today(), day=True)
                rewards = ", ".join(f"""{reward["amount"]:,} {reward["item"]}""" for reward in data_manage.get_alert_reward(alert))
                embed.add_field(name=f"""{alert["mission"]["node"]}: {time}""", value=rewards, inline=False)
        await destination.send(embed=embed)
    else:
        await destination.send("❌ No active alerts.")


async def send_void_trader(destination:Union[discord.User, discord.Member]):
    """Helper function to send Void Trader info."""
    data = VoidTraider().check()
    embed = discord.Embed(title="Baro Ki'teer", color=discord.Color.blue(), url=f"""{st.secrets.host.cloud}void""")
    embed.set_footer(icon_url=Warframe.DUCAT.value["image"], text="via Voidpet | Hosted on Streamlit")
    embed.add_field(name="Active", value=data["active"], inline=True)
    embed.add_field(name="Time", value=data["message"], inline=True)
    await destination.send(embed=embed)


async def send_vault_trader(destination:Union[discord.User, discord.Member]):
    """Helper function to send Vault Trader info."""
    data = VaultTraider().check()
    embed = discord.Embed(title="Varzia", color=discord.Color.blue(), url=f"""{st.secrets.host.cloud}vault""")
    embed.set_footer(icon_url=Warframe.AYA.value["image"], text="via Voidpet | Hosted on Streamlit")
    embed.add_field(name="Active", value=data["active"], inline=True)
    embed.add_field(name="Time", value=data["message"], inline=True)
    await destination.send(embed=embed)


async def handle_context_menu(interaction: discord.Interaction, user: discord.User, function, bot_id:int):
    """Handles sending messages based on context menu."""
    # if user == interaction.user or user == self.bot.user:
    if user == interaction.user or user.id == bot_id:
        try:
            await function(interaction.user)  # DM the user
            await interaction.response.send_message("✅ Check your DMs.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("❌ I can't DM you. Check your privacy settings.", ephemeral=True)
    else:
        await interaction.response.send_message("❌ You can only run this command on yourself or the bot.", ephemeral=True)