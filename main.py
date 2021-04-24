#import discord package
import discord
from discord import embeds
from discord.colour import Color
from discord.ext import commands
from random import choice, randint
from typing import Optional
from datetime import datetime

from aiohttp import request
from discord import Member, Embed
from discord.ext.commands import Cog, BucketType
from discord.ext.commands import BadArgument
from discord.ext.commands import command, cooldown

intents = discord.Intents.all()
intents.members = True  # Subscribe to the privileged members intent.
bot= discord.Client(intents=intents)

#client
client=commands.Bot(command_prefix='..',intents=intents)



@client.command(name="fact")
async def animal_fact(ctx, animal: str):
    if (animal := animal.lower()) in ("dog", "cat", "panda", "fox", "bird", "koala"):
        fact_url = f"https://some-random-api.ml/facts/{animal}"
        image_url = f"https://some-random-api.ml/img/{'birb' if animal == 'bird' else animal}"

        async with request("GET", image_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                image_link = data["link"]

            else:
                image_link = None

        async with request("GET", fact_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()

                embed = Embed(title=f"{animal.title()} fact",
                                description=data["fact"],
                                colour=ctx.author.colour)
                if image_link is not None:
                    embed.set_image(url=image_link)
                await ctx.send(embed=embed)

            else:
                await ctx.send(f"API returned a {response.status} status.")

    else:
        await ctx.send("No facts are available for that animal.")

@client.command(name="echo", aliases=["say"])
async def echo_message(ctx, *, message):
		await ctx.message.delete()
		await ctx.send(message)	

@client.command(name="slap", aliases=["hit"])
async def slap_member(ctx, member: Member, *, reason: Optional[str] = "for no reason"):
		await ctx.send(f"{ctx.author.display_name} slapped {member.mention} {reason}!")

@slap_member.error
async def slap_member_error(ctx, exc):
		if isinstance(exc, BadArgument):
			await ctx.send("I can't find that member.")

@client.command(name="userinfo", aliases=["memberinfo", "ui", "mi"])           ##wrong number
async def user_info(ctx, target: Optional[Member]):
		target = target or ctx.author

		embed = Embed(title="User information",
					  colour=target.colour,
					  timestamp=datetime.utcnow())

		embed.set_thumbnail(url=target.avatar_url)

		fields = [("Name", str(target), True),
				  ("ID", target.id, True),
				  ("Bot?", target.bot, True),
				  ("Top role", target.top_role.mention, True),
				  ("Status", str(target.status).title(), True),
				  ("Activity", f"{str(target.activity.type).split('.')[-1].title() if target.activity else 'N/A'} {target.activity.name if target.activity else ''}", True),
				  ("Created at", target.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
				  ("Joined at", target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True),
				  ("Boosted", bool(target.premium_since), True)]

		for name, value, inline in fields:
			embed.add_field(name=name, value=value, inline=inline)

		await ctx.send(embed=embed)



@client.command(name="serverinfo", aliases=["guildinfo", "si", "gi"])
async def server_info(ctx):
		print(ctx.guild.owner)
		embed = Embed(title="Server information",
					  colour=ctx.guild.owner.colour,
					  timestamp=datetime.utcnow())

		embed.set_thumbnail(url=ctx.guild.icon_url)

		statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]

		fields = [("ID", ctx.guild.id, True),
				  ("Owner", ctx.guild.owner, True),
				  ("Region", ctx.guild.region, True),
				  ("Created at", ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
				  ("Members", len(ctx.guild.members), True),
				  ("Humans", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
				  ("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
				  ("Banned members", len(await ctx.guild.bans()), True),
				  ("Statuses", f"🟢 {statuses[0]} 🟠 {statuses[1]} 🔴 {statuses[2]} ⚪ {statuses[3]}", True),
				  ("Text channels", len(ctx.guild.text_channels), True),
				  ("Voice channels", len(ctx.guild.voice_channels), True),
				  ("Categories", len(ctx.guild.categories), True),
				  ("Roles", len(ctx.guild.roles), True),
				  ("Invites", len(await ctx.guild.invites()), True),
				  ("\u200b", "\u200b", True)]

		for name, value, inline in fields:
			embed.add_field(name=name, value=value, inline=inline)

		await ctx.send(embed=embed)


@client.event
async def on_ready():
    #do stuff.....
    general_chanel = client.get_channel(753250363016216627)
    await general_chanel.send('bot online')


client.run('ODMzNjg3Mjk5Njg1NjEzNTY4.YH19zQ.ji46gcZjA_R8ff8wEMpQWoYnkxI')