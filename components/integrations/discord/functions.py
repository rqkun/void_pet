from datetime import datetime
from typing import Union
import streamlit as st
import discord
from discord.ext import commands
import urllib

from config.classes.vendors import VaultTraider, VoidTraider
from config.constants import Warframe
from utils import data_manage, tools

def commands_embed():
    embed = discord.Embed(title="Commands", color=discord.Color.blue())
    embed.set_footer(icon_url=Warframe.MODE_ICONS.value["ALERT"],text="via Voidpet | Hosted on Streamlit")
    embed.add_field(name="/help", value="A command that show you this!", inline=False)
    embed.add_field(name="/worldstate", value="A command that show the ingame planet cycles!", inline=False)
    embed.add_field(name="/invasions", value="A command that show potential invasion rewards!", inline=False)
    embed.add_field(name="/alerts", value="A command that show alert info and rewards!", inline=False)
    embed.add_field(name="/void", value="A command that show Prime Resurgent duration!", inline=False)
    embed.add_field(name="/vault", value="A command that show Baro Ki'ter ETA!", inline=False)
    return embed


def invasions_embed():
    """Helper function to send invasion rewards."""
    embed = discord.Embed(title="Invasion Rewards", color=discord.Color.blue())
    embed.set_footer(icon_url=Warframe.MODE_ICONS.value["INVASION"], text="via Voidpet | Hosted on Streamlit")
    data = data_manage.get_world_state()["invasions"]
    if data:
        for invasion in data:
            if not invasion.get("completed",True):
                attacker = invasion.get("attacker", None)
                
                if attacker:
                    atk_faction = attacker.get("faction","")
                    atk_rewards = attacker.get("reward", None)
                    if atk_rewards:
                        atk_reward = atk_rewards.get("asString","None")
                    else: atk_reward = "None"
                    
                defender = invasion.get("defender", None)
                if defender:
                    def_faction = defender.get("faction","")
                    def_rewards = defender.get("reward", "None")
                    if def_rewards:
                        def_reward = def_rewards.get("asString","None")
                    else: def_reward = "None"

                node = invasion.get("node","")
                completion = invasion.get("completion",0)
                atk_completion = 100 - int(completion)
                embed.add_field(name=f"{node}: ", value=f"{atk_completion:02d}%\
                                **{atk_faction}**: *{atk_reward}*\n{int(completion):02d}%\
                                **{def_faction}**: *{def_reward}*", inline=True)

        return embed
    else:
        embed.add_field(name="Empty",value="❌ No active invasions.")
        return embed


def worldstate_embed():
    """Helper function to send world state info."""
    data = data_manage.get_cycles()
    embed = discord.Embed(title="Worldstate", color=discord.Color.blue(), url=f"""{st.secrets.host.cloud}""")
    embed.set_footer(icon_url=Warframe.MODE_ICONS.value["OPEN_WORLD"], text="via Voidpet | Hosted on Streamlit")
    if data:
        for item in data:
            span = datetime.strptime(item["data"]["expiry"], "%Y-%m-%dT%H:%M:%S.%fZ") - datetime.today()
            time = tools.format_timedelta(span, day=False) if span.total_seconds() > 0 else "Expired"
            embed.add_field(name=item["name"], value=f"""{item["data"]["state"].title()}: {time}""", inline=True)
        return embed
    else:
        embed.add_field(name="Empty",value="❌ No active invasions.")
        return embed


def alerts_embed():
    """Helper function to send alert rewards."""
    embed = discord.Embed(title="Alert Rewards", color=discord.Color.blue(), url=f"""{st.secrets.host.cloud}""")
    embed.set_footer(icon_url=Warframe.MODE_ICONS.value["ALERT"], text="via Voidpet | Hosted on Streamlit")
    data = data_manage.get_alerts_data()
    if data:
        for alert in data:
            if alert["active"]:
                time = tools.format_timedelta(datetime.strptime(alert["expiry"], "%Y-%m-%dT%H:%M:%S.%fZ") - datetime.today(), day=True)
                rewards = ", ".join(f"""{reward["amount"]:,} {reward["item"]}""" for reward in data_manage.get_alert_reward(alert))
                embed.add_field(name=f"""{alert["mission"]["node"]}: {time}""", value=rewards, inline=False)
        return embed
    else:
        embed.add_field(name="Empty",value="❌ No active invasions.")
        return embed


def void_trader_embed():
    """Helper function to send Void Trader info."""
    data = VoidTraider().check()
    embed = discord.Embed(title="Baro Ki'teer", color=discord.Color.blue(), url=f"""{st.secrets.host.cloud}void""")
    embed.set_footer(icon_url=Warframe.DUCAT.value["image"], text="via Voidpet | Hosted on Streamlit")
    embed.add_field(name="Active", value=data["active"], inline=True)
    embed.add_field(name="Time", value=data["message"], inline=True)
    return embed


def vault_trader_embed():
    """Helper function to send Vault Trader info."""
    data = VaultTraider().check()
    embed = discord.Embed(title="Varzia", color=discord.Color.blue(), url=f"""{st.secrets.host.cloud}vault""")
    embed.set_footer(icon_url=Warframe.AYA.value["image"], text="via Voidpet | Hosted on Streamlit")
    embed.add_field(name="Active", value=data["active"], inline=True)
    embed.add_field(name="Time", value=data["message"], inline=True)
    return embed


async def handle_context(interaction: discord.Interaction, function):
    """Handles sending messages based on context menu."""
    # if user == interaction.user or user == self.bot.user:
    try:
        embed = function()  # DM the user
        interaction_type = False if interaction.channel.type == discord.ChannelType.private else True
        await interaction.response.send_message(embed=embed, ephemeral=interaction_type)
    except discord.Forbidden:
        await interaction.response.send_message("❌ I can't DM you. Check your privacy settings.", ephemeral=True)