# <:thinking:263a7f4eeb6f69e46d969fa479188592>



# bot.py
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

import pprint as pp


intents = discord.Intents()
intents = intents.all()


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_NAME = os.getenv('DISCORD_GUILD')
VERBOSE = eval(os.getenv('VERBOSE'))




#initialize globals
glob_guild = None
glob_members = None
if "debug" in VERBOSE:
	glob_test = None


#initialize client
bot = commands.Bot(command_prefix="nick!", intents=intents)

@bot.event
@commands.bot_has_permissions(manage_nicknames=True)
async def on_ready():
	#set globs
	for guild in bot.guilds:
		if guild.name == GUILD_NAME:
			glob_guild = guild
			print(f'{bot.user} is listening to guild {guild.name}')
			break 
	#members = await glob_guild.chunk()
	#glob_members = await glob_guild.fetch_members().flatten()

	if "debug" in VERBOSE:
		pass

@bot.command(name="name", ignore_extra=False)
async def nick_user(ctx, username, nickname):
	guild = ctx.guild
	user_id = int("".join( [i for i in list(username) if i.isdigit()] ))
	members = guild.members
	member_to_change = None
	for member in members:
		if member.id == user_id:
			member_to_change = member
	print(f"Changing @{member_to_change}'s nickname to {nickname}")
	await member_to_change.edit(nick=nickname)
	return


bot.run(TOKEN)