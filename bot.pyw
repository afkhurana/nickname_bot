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
FILTER = eval(os.getenv('FILTER'))
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
	old_nickname = member_to_change.nick
	print(f"Changing @{member_to_change}'s nickname from \"{old_nickname}\" to \"{nickname}\"")
	channel_invoked = ctx.message.channel
	if ctx.message.author == member_to_change:
		error_text = "Hey! You can't change your own nickname!"
		print(f"@{member_to_change} tried to change their own nickname!")
		await channel_invoked.send(error_text)
		return
	for filter_text in FILTER:
		if filter_text in nickname:
			print(f"{filter_text} filter is on.")
			await channel_invoked.send("no.")
			return
	try:
		await member_to_change.edit(nick=nickname)
		success_text = f"Successfully changed @{member_to_change}'s nickname from \"{old_nickname}\" to \"{nickname}\""
		print(success_text)
		await channel_invoked.send(success_text)
	except commands.errors.TooManyArguments:
		error_text = "Too many arguments! Please use the following format: nick!name @user \"New Nickname\""
		print(error_text)
		await channel_invoked.send(error_text)
	except discord.errors.HTTPException as err:
		if err.status == 400 and err.code == 50035:
			if "In nick: Must be 32 or fewer in length." in err.text:
				error_text = "Nickname is too long! Nick must be 32 characters or fewer."
				print(error_text)
				await channel_invoked.send(error_text)
			else:
				raise err
		else:
			raise err
	except (discord.errors.Forbidden, commands.errors.CommandInvokeError):
		print("[ERROR] 403 Forbidden")
	return



@bot.command(name="filter")
@commands.has_role("admin")
async def add_filter(ctx, filter_text):
	guild = ctx.guild
	channel_invoked = ctx.message.channel

	FILTER.append(filter_text)

	beforeLines = []
	atFilter = False
	afterLines = []
	with open(".env", "r") as f:
		for line in f:
			if line.startswith("FILTER=") or line.startswith("export FILTER="):
				atFilter = True
				continue
			else:
				if not atFilter:
					beforeLines.append(line)
				else:
					afterLines.append(line)
	with open(".env", "w") as f:
		newEnv = beforeLines + ["FILTER=" + str(FILTER)] + afterLines
		f.writeLines(newEnv)

	success_text_0 = f"{filter_text} has been added to nickname filter."
	success_text_1 = f"Filter list is now {FILTER}"
	print(success_text_0)
	print(success_text_1)
	await channel_invoked.send(success_text_0)
	await channel_invoked.send(success_text_1)

	return

bot.run(TOKEN)