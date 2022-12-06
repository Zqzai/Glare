import discord
import json
import requests, random
import os
import httpx, base64, time, subprocess, re, datetime, asyncio, discord_webhook, threading
from discord.ext import commands, tasks
from discord.ui import Select, View, Button
from discord import *
from colorama import Fore, init

init(convert=True)
os.system("cls")

bot = commands.Bot(intents=discord.Intents.all(), command_prefix="=", help_command=None, case_insensitive=True)

prefix = f"{Fore.RESET}[{Fore.MAGENTA}>{Fore.RESET}]"
botPrefix = ","
cross = "<:warning:1047607177096999025>"
tick = "<:tick:1047607173632499754>"
warning = "<:warning:1047607177096999025>"
moderation = "<:moderation:1046536063658766377>"
utility = "<:utility:1046539927485153391>"
fun = "<:fun:1046540187083223120>"
other = "<:other:1046540392683802744>"
helpE = "<:tick:1047607173632499754>"
home = "<:home:1046542126403555368>"
upstart = datetime.datetime.utcnow()

guilds = []
with open("authorised.txt", "r") as f:
    for line in f:
        guilds.append(line.strip())

@bot.event
async def on_guild_join(guild):
    if not os.path.exists(f"C:\\Users\\aklam\\Music\\\\Soul\\Guilds\\{guild.id}"):
        os.mkdir(f"C:\\Users\\aklam\\Music\\\\Soul\\Guilds\\{guild.id}")
        with open(f"C:\\Users\\aklam\\Music\\\\Soul\\Guilds\\{guild.id}\\config.json", "w") as f:
            json.dump({"muterole": None}, f, indent=4)

        with open(f"C:\\Users\\aklam\\Music\\\\Soul\\Guilds\\{guild.id}\\muted.json", "w") as f:
            json.dump({}, f, indent=4)

@bot.event
async def on_guild_remove(guild):
    if os.path.exists(f"C:\\Users\\aklam\\Music\\\\Soul\\Guilds\\{guild.id}"):
        os.rmdir(f"C:\\Users\\aklam\\Music\\\\Soul\\Guilds\\{guild.id}")

@bot.command()
async def muterole(ctx, role: discord.Role=None): 
    if ctx.author.guild_permissions.manage_roles:
        if role:
            try:
                with open(f"C:\\Users\\aklam\\Music\\\\Soul\\Guilds\\{ctx.guild.id}\\config.json", "r") as f:
                    config = json.load(f)
                config["muterole"] = role.id
                with open(f"C:\\Users\\aklam\\Music\\\\Soul\\Guilds\\{ctx.guild.id}\\config.json", "w") as f:
                    json.dump(config, f, indent=4)
                embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: Successfully set the **mute role** to `{role.name}`.")
                await ctx.send(embed=embed)
            except:
                embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: An error occurred while setting the **mute role** to `{role.name}`.")
                await ctx.send(embed=embed)
        else:
            try:
                with open(f"C:\\Users\\aklam\\Music\\\\Soul\\Guilds\\{ctx.guild.id}\\config.json", "r") as f:
                    config = json.load(f)
                if config["muterole"]:
                    role = ctx.guild.get_role(config["muterole"])
                    embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: The **mute role** is set to `{role.name}`.")
                    await ctx.send(embed=embed)
                else:
                   embed = discord.Embed(color=0xec4245, description=f"{cross} {message.author.mention}: The **mute role** for this server is not set.")
                   await ctx.send(embed=embed)
            except:
                embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: An error occurred while retrieving the **mute role**.")
                await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=0xec4245, description=f"{warning} {message.author.mention}: You **do not** have the `manage_roles` permission.")
        await ctx.send(embed=embed)

@bot.command()
async def authorise(ctx):
    if ctx.author.id == 550752995458023427:
        if ctx.guild.id not in guilds:
            with open("authorised.txt", "a") as f:
                f.write(f"{ctx.guild.id}\n")
            embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: Successfully **authorised** the server `{ctx.guild.name}` to use glare.")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: The server `{ctx.guild.name}` is already **authorised**.")
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: You **do not** have the `bot owner` permission.")
        await ctx.send(embed=embed)

@bot.command()
async def deauthorise(ctx):
    if ctx.author.id == 550752995458023427:
        for guild in guilds:
            if ctx.guild.id == guild:
                with open("authorised.txt", "r") as f:
                    lines = f.readlines()
                with open("authorised.txt", "w") as f:
                    for line in lines:
                        if line.strip("\n") != ctx.guild.id:
                            f.write(line)
                embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: Successfully **deauthorised** the server `{ctx.guild.name}` to use glare.")
                await ctx.send(embed=embed)
                break
        
        embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: The server `{ctx.guild.name}` is already **deauthorised**.")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: You **do not** have the `bot owner` permission.")
        await ctx.send(embed=embed)


@bot.command()
async def mute(ctx, member: discord.Member=None, duration: str=None, reason: str=None):
    if member == None:
        embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: Please specify a **member** to mute.")
        await ctx.send(embed=embed)
        return

    measurement = None
    mutedby = ctx.author
    if duration:
        if duration.endswith("s"):
            duration = int(duration[:-1])
            measurement = "seconds"
        elif duration.endswith("m"):
            duration = int(duration[:-1]) * 60
            measurement = "minutes"
        elif duration.endswith("h"):
            duration = int(duration[:-1]) * 3600
            measurement = "hours"
        elif duration.endswith("d"):
            duration = int(duration[:-1]) * 86400
            measurement = "days"
        elif duration.endswith("w"):
            duration = int(duration[:-1]) * 604800
            measurement = "weeks"
        else:
            embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: Please specify a valid **duration**.")
            await ctx.send(embed=embed)
            return

    if ctx.author.guild_permissions.manage_roles:
        try:
            with open(f"C:\\Users\\aklam\\Music\\\\Soul\\Guilds\\{ctx.guild.id}\\config.json", "r") as f:
                config = json.load(f)
            if config["muterole"]:
                role = ctx.guild.get_role(config["muterole"])
                if role in member.roles:
                    embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: The member `{member.name}` is already **muted**.")
                    await ctx.send(embed=embed)
                else:
                    await member.add_roles(role)
                    if duration:
                        if measurement == "seconds":
                            embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: Successfully **muted** the member `{member.name}` for `{duration}s`.")
                            await ctx.send(embed=embed)
                        elif measurement == "minutes":
                            embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: Successfully **muted** the member `{member.name}` for `{int(duration / 60)}m`.")
                            await ctx.send(embed=embed)
                        elif measurement == "hours":
                            embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: Successfully **muted** the member `{member.name}` for `{int(duration / 3600)}h`.")
                            await ctx.send(embed=embed)
                        elif measurement == "days":
                            embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: Successfully **muted** the member `{member.name}` for `{int(duration / 86400)}d`.")
                            await ctx.send(embed=embed)
                        elif measurement == "weeks":
                            embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: Successfully **muted** the member `{member.name}` for `{int(duration / 604800)}w`.")
                            await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: Successfully **muted** the member `{member.name}`.")
                    with open(f"C:\\Users\\aklam\\Music\\\\Soul\\Guilds\\{ctx.guild.id}\\muted.json", "r") as f:
                        muted = json.load(f)
                    
                    if duration and reason:
                        timetobeunmuted = time.time() + duration
                        muted[member.id] = {"duration": duration, "reason": reason, "time": int(time.time()), "mutedby": mutedby.id, "unmutedin":  timetobeunmuted}
                    elif duration:
                        timetobeunmuted = time.time() + duration
                        muted[member.id] = {"duration": duration, "reason": None, "time": int(time.time()), "mutedby": mutedby.id, "unmutedin":  timetobeunmuted}
                    elif reason:
                        muted[member.id] = {"duration": None, "reason": reason, "time": int(time.time()), "mutedby": mutedby.id}
                    else:
                        muted[member.id] = {"duration": None, "reason": None, "time": int(time.time()), "mutedby": mutedby.id}
                    with open(f"C:\\Users\\aklam\\Music\\\\Soul\\Guilds\\{ctx.guild.id}\\muted.json", "w") as f:
                        json.dump(muted, f, indent=4)
            else:
                embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: The server does not have a **mute role** set.")
                await ctx.send(embed=embed)
        except:
            embed = discord.Embed(color=0xec4245, description=f"{cross} {ctx.author.mention}: The server does not have a **mute role** set.")
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: You **do not** have the `manage roles` permission.")
        await ctx.send(embed=embed)

@bot.command()
async def unmute(ctx, member: discord.Member=None, reason: str=None):
    if member == None:
        embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: Please specify a **member** to unmute.")
        await ctx.send(embed=embed)
        return

    if ctx.author.guild_permissions.manage_roles:
        try:
            with open(f"C:\\Users\\aklam\\Music\\\\Soul\\Guilds\\{ctx.guild.id}\\config.json", "r") as f:
                config = json.load(f)
            if config["muterole"]:
                role = ctx.guild.get_role(config["muterole"])
                await member.remove_roles(role)
                embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: Successfully **unmuted** the member `{member.name}`.")
                await ctx.send(embed=embed)
                with open(f"C:\\Users\\aklam\\Music\\\\Soul\\Guilds\\{ctx.guild.id}\\muted.json", "r") as f:
                    muted = json.load(f)
                if member.id in muted:
                    del muted[member.id]
                with open(f"C:\\Users\\aklam\\Music\\\\Soul\\Guilds\\{ctx.guild.id}\\muted.json", "w") as f:
                    json.dump(muted, f, indent=4)
            else:
                embed = discord.Embed(color=0xec4245, description=f"{cross} {ctx.author.mention}: The server does not have a **mute role** set.")
                await ctx.send(embed=embed)
        except:
            embed = discord.Embed(color=0xec4245, description=f"{cross} {ctx.author.mention}: The server does not have a **mute role** set.")
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: You **do not** have the `manage roles` permission.")
        await ctx.send(embed=embed)

@bot.command()
async def muteinfo(ctx, member: discord.Member=None):
    if member == None:
        embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: Please specify a **member** to check.")
        await ctx.send(embed=embed)
        return

    if ctx.author.guild_permissions.manage_roles:
        try:
            with open(f"C:\\Users\\aklam\\Music\\\\Soul\\Guilds\\{ctx.guild.id}\\muted.json", "r") as f:
                muted = json.load(f)
            if str(member.id) in muted:
                if muted[str(member.id)]["duration"]:
                    duration = muted[str(member.id)]["duration"]
                    try:
                        unmutedin = f"<t:{int(muted[str(member.id)]['unmutedin'])}:R>"
                    except:
                        unmutedin = "Never"
                    if duration >= 86400:
                        duration = int(duration / 86400)
                        measurement = "days"
                    elif duration >= 3600:
                        duration = int(duration / 3600)
                        measurement = "hours"
                    elif duration >= 60:
                        duration = int(duration / 60)
                        measurement = "minutes"
                    else:
                        measurement = "seconds"
                    duration = str(duration) + " " + measurement
                else:
                    duration = "None"
                if muted[str(member.id)]["reason"]:
                    reason = muted[str(member.id)]["reason"]
                else:
                    reason = "None"
                embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: The member `{member.name}` is **muted** for `{duration}` with the reason `{reason}`. They will be unmuted {unmutedin}.")
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: The member `{member.name}` is **not muted**.")
                await ctx.send(embed=embed)
        except:
            embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: The member `{member.name}` is **not muted**.")
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: You **do not** have the `manage roles` permission.")
        await ctx.send(embed=embed)

@bot.command()
async def convert(ctx, amount: float=None, from_: str=None, to: str=None):
    if amount == None:
        embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: Please specify an **amount** to convert.")
        await ctx.send(embed=embed)
        return
    if from_ == None:
        embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: Please specify a **from** currency to convert from.")
        await ctx.send(embed=embed)
        return
    if to == None:
        embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: Please specify a **to** currency to convert to.")
        await ctx.send(embed=embed)
        return

    from_ = from_.upper()
    to = to.upper()
    if from_ == to:
        embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: You cannot convert from the same currency to the same currency.")
        await ctx.send(embed=embed)
        return

    if from_ == "$":
        from_ = "USD"
    if to == "$":
        to = "USD"
    if from_ == "£":
        from_ = "GBP"
    if to == "£":
        to = "GBP"
    if from_ == "€":
        from_ = "EUR"
    if to == "€":
        to = "EUR"
    if from_ == "¥":
        from_ = "JPY"
    if to == "¥":
        to = "JPY"
    if from_ == "₹":
        from_ = "INR"
    if to == "₹":
        to = "INR"
    if from_ == "₽":
        from_ = "RUB"
    if to == "₽":
        to = "RUB"
    if from_ == "₩":
        from_ = "KRW"
    if to == "₩":
        to = "KRW"
    if from_ == "₺":
        from_ = "TRY"
    if to == "₺":
        to = "TRY"
    if from_ == "₴":
        from_ = "UAH"
    if to == "₴":
        to = "UAH"
    if from_ == "₦":
        from_ = "NGN"
    if to == "₦":
        to = "NGN"
    if from_ == "₱":
        from_ = "PHP"
    if to == "₱":
        to = "PHP"
    if from_ == "฿":
        from_ = "THB"
    if to == "฿":
        to = "THB"
    if from_ == "₮":
        from_ = "MNT"
    if to == "₮":
        to = "MNT"
    
    req = requests.get(f"https://api.fastforex.io/fetch-one?from={from_}&to={to}&api_key=e168421f33-ada20504de-rm2lsn")
    if req.status_code == 200:
        converted = amount * req.json()["result"][f"{to}"]
        converted = str(f"{converted:.2f}")
        amount = str(f"{amount:.2f}")
        embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: `{amount}` {from_} is `{converted}` {to}.")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: The currency `{from_}` is **invalid**.")
        await ctx.send(embed=embed)

@bot.command()
async def uptime(ctx):
    global upstart
    hours = int(datetime.datetime.now().timestamp() - upstart) // 3600
    minutes = int(datetime.datetime.now().timestamp() - upstart) // 60
    seconds = int(datetime.datetime.now().timestamp() - upstart) % 60
    if hours >= 24:
        days = int(hours / 24)
        hours = hours % 24
        uptime = f"{days} days, {hours} hours, {minutes} minutes and {seconds} seconds"
    else:
        uptime = f"{hours} hours, {minutes} minutes and {seconds} seconds"
    embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: I have been **online** for `{uptime}`.")
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: Pong! `{round(bot.latency * 1000)}ms`")
    await ctx.send(embed=embed)

@bot.command()
async def role(ctx, member: discord.Member=None, role: discord.Role=None):
    if ctx.author.guild_permissions.manage_roles:
        if role.position > ctx.guild.me.top_role.position:
                embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: The role `{role.name}` is **higher** than my highest role.")
                await ctx.send(embed=embed)
                return
        if ctx.author != ctx.guild.owner:
            if role.position > ctx.author.top_role.position:
                embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: The role `{role.name}` is **higher** than your highest role.")
                await ctx.send(embed=embed)
                return
            if member.top_role.position > ctx.author.top_role.position:
                embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: The member `{member.name}` has a **higher** role than you.")
                await ctx.send(embed=embed)
                return 
        if member == None:
            embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: Please specify a **member** to add the role to.")
            await ctx.send(embed=embed)
            return
        if role == None:
            embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: Please specify a **role** to add to the member.")
            await ctx.send(embed=embed)
            return
        if role in member.roles:
            await member.remove_roles(role)
            embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: Removed the role `{role.name}` from `{member.name}`.")
            await ctx.send(embed=embed)
            return
        await member.add_roles(role)
        embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: The role `{role.name}` has been added to the member `{member.name}`.")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: You **do not** have the `manage roles` permission.")
        await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: Here is the server info for `{guild.name}`.")
    embed.set_thumbnail(url=guild.icon.url)
    embed.add_field(name="Server Name", value=f"`{guild.name}`", inline=False)
    embed.add_field(name="Server ID", value=f"`{guild.id}`", inline=False)
    embed.add_field(name="Server Owner", value=f"`{guild.owner}`", inline=False)
    embed.add_field(name="Server Owner ID", value=f"`{guild.owner_id}`", inline=False)
    embed.add_field(name="Server Boost Level", value=f"`{guild.premium_tier}`", inline=False)
    embed.add_field(name="Server Boost Count", value=f"`{guild.premium_subscription_count}`", inline=False)
    embed.add_field(name="Server Member Count", value=f"`{guild.member_count}`", inline=False)
    embed.add_field(name="Server Verification Level", value=f"`{str(guild.verification_level).capitalize()}`", inline=False)
    guildcreated = guild.created_at.strftime("%d/%m/%Y %H:%M:%S")
    embed.add_field(name="Server Created At", value=f"`{guildcreated}`", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def userinfo(ctx, member: discord.Member=None):
    if member == None:
        member = ctx.author
    embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: Here is the user info for `{member.name}`.")
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name="User Name", value=f"`{member.name}`", inline=False)
    embed.add_field(name="User ID", value=f"`{member.id}`", inline=False)
    embed.add_field(name="User Status", value=f"`{str(member.status).capitalize()}`", inline=False)
    embed.add_field(name="User Activity", value=f"`{str(member.activity)}`", inline=False)
    embed.add_field(name="User Top Role", value=f"`{member.top_role}`", inline=False)
    embed.add_field(name="User Joined At", value=f"`{member.joined_at.strftime('%d/%m/%Y %H:%M:%S')}`", inline=False)
    embed.add_field(name="User Created At", value=f"`{member.created_at.strftime('%d/%m/%Y %H:%M:%S')}`", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(color=0x2F3136, description=f"{question}")
    embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar.url)
    embed.set_footer(text="React to vote!")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    if ctx.author.guild_permissions.kick_members:
        if member == None:
            embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: Please specify a **member** to kick.")
            await ctx.send(embed=embed)
            return
        if member == ctx.author:
            embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: You **cannot** kick yourself.")
            await ctx.send(embed=embed)
            return
        if member.top_role.position > ctx.author.top_role.position:
            embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: The member `{member.name}` has a **higher** role than you.")
            await ctx.send(embed=embed)
            return
        if reason == None:
            reason = "No reason provided."
        await member.kick(reason=reason)
        embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: Kicked `{member.name}` for `{reason}`.")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: You **do not** have the `kick members` permission.")
        await ctx.send(embed=embed)

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    if ctx.author.guild_permissions.ban_members:
        if member == None:
            embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: Please specify a **member** to ban.")
            await ctx.send(embed=embed)
            return
        if member == ctx.author:
            embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: You **cannot** ban yourself.")
            await ctx.send(embed=embed)
            return
        if member.top_role.position > ctx.author.top_role.position:
            embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: The member `{member.name}` has a **higher** role than you.")
            await ctx.send(embed=embed)
            return
        if reason == None:
            reason = "No reason provided."
        await member.ban(reason=reason)
        embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: Banned `{member.name}` for `{reason}`.")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: You **do not** have the `ban members` permission.")
        await ctx.send(embed=embed)

@bot.command()
async def unban(ctx, *, member):
    if ctx.author.guild_permissions.ban_members:
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: Unbanned `{user.name}`.")
                await ctx.send(embed=embed)
                return
    else:
        embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: You **do not** have the `ban members` permission.")
        await ctx.send(embed=embed)

@bot.command(aliases=['delete', 'purge'])
async def clear(ctx, amount: int=None):
    if ctx.author.guild_permissions.manage_messages:
        if amount == None:
            embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: Please specify an **amount** of messages to delete.")
            await ctx.send(embed=embed)
            return
        if amount > 500:
            embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: You **cannot** delete more than 500 messages at a time.")
            await ctx.send(embed=embed)
            return
        if amount < 1:
            embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: You **cannot** delete less than 1 message.")
            await ctx.send(embed=embed)
            return
        await ctx.channel.purge(limit=amount + 1)
        if amount != 1:
            embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: Deleted `{amount}` messages.")
        else:
            embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: Deleted `{amount}` message.")
        await ctx.send(embed=embed, delete_after=5)
    else:
        embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: You **do not** have the `manage messages` permission.")
        await ctx.send(embed=embed)

@bot.command()
async def lock(ctx, channel: discord.TextChannel=None):
    if ctx.author.guild_permissions.manage_channels:
        if channel == None:
            channel = ctx.channel
        if channel.overwrites_for(ctx.guild.default_role).send_messages == False:
            embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: The channel `{channel.name}` is **already** locked.")
            await ctx.send(embed=embed)
            return
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: Locked `{channel.name}`.")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: You **do not** have the `manage channels` permission.")
        await ctx.send(embed=embed)

@bot.command()
async def unlock(ctx, channel: discord.TextChannel=None):
    if ctx.author.guild_permissions.manage_channels:
        if channel == None:
            channel = ctx.channel
        if channel.overwrites_for(ctx.guild.default_role).send_messages == True:
            embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: The channel `{channel.name}` is **already** unlocked.")
            await ctx.send(embed=embed)
            return
        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: Unlocked `{channel.name}`.")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: You **do not** have the `manage channels` permission.")
        await ctx.send(embed=embed)

@bot.command()
async def slowmode(ctx, seconds: int=None, channel: discord.TextChannel=None):
    if ctx.author.guild_permissions.manage_channels:
        if channel == None:
            channel = ctx.channel
        if seconds == None:
            embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: Please specify a **number** of seconds for the slowmode.")
            await ctx.send(embed=embed)
            return
        if seconds > 21600:
            embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: You **cannot** set the slowmode to more than 21600 seconds.")
            await ctx.send(embed=embed)
            return
        if seconds < 0:
            embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: You **cannot** set the slowmode to less than 0 seconds.")
            await ctx.send(embed=embed)
            return
        await channel.edit(slowmode_delay=seconds)
        if seconds != 1:
            embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: Set the slowmode of `{channel.name}` to `{seconds}` seconds.")
        else:
            embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: Set the slowmode of `{channel.name}` to `{seconds}` second.")

@bot.command(aliases=['av', 'pfp'])
async def avatar(ctx, member: discord.Member=None):
    if member == None:
        member = ctx.author
    embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: Here is the avatar for `{member.name}`.")
    try:
        embed.set_image(url=member.avatar.url)
    except:
        embed.set_image(url="https://cdn.discordapp.com/embed/avatars/0.png")
    select = Select(
        placeholder = "Choose a category...",
        options=[
            discord.SelectOption(label='Profile Picture', description='View the user\'s profile picture.', emoji='👤'),
            discord.SelectOption(label='Banner', description='View the user\'s banner.', emoji='🏠'),
         ])

    async def my_callback(interaction):
        if interaction.user != ctx.author:
            return await interaction.response.send_message("This isn't your command!", ephemeral=True)
        if select.values[0] == "Profile Picture":
            embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: Here is the avatar for `{member.name}`.")
            try:
                embed.set_image(url=member.avatar.url)
            except:
                embed.set_image(url="https://cdn.discordapp.com/embed/avatars/0.png")
            await message1.edit(embed=embed, view=view)
            await interaction.response.defer()
        if select.values[0] == "Banner":
            req = await bot.http.request(discord.http.Route("GET", f"/users/{member.id}"))
            banner_id = req["banner"]
            # If statement because the user may not have a banner
            if banner_id:
                banner_url = f"https://cdn.discordapp.com/banners/{member.id}/{banner_id}?size=1024"
                embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: Here is the avatar for `{member.name}`.")
            else:
                embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: This user does not have a banner.")

            embed.set_image(url=banner_url)

            await message1.edit(embed=embed, view=view)
            await interaction.response.defer()
    select.callback = my_callback
    view = View()
    view.add_item(select)
    message1 = await ctx.send(embed=embed, view=view)
    
@bot.command()
async def invite(ctx):
    embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: Here is the invite link for the bot.")
    embed.add_field(name="Invite Link", value=f"[Click Here](https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot)", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def roles(ctx):
    roles = ctx.guild.roles
    # put the roles in pages of 10
    pages = [roles[i:i+5] for i in range(0, len(roles), 5)]
    total = len(pages)
    # create the embeds
    embeds = []
    for page in pages:
        embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: Here are the roles in `{ctx.guild.name}`.")
        for role in page:
            embed.add_field(name=role.name, value=f"ID: {role.id}", inline=False)

        embeds.append(embed)
    # create the view
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="Previous", style=discord.ButtonStyle.grey, disabled=True))
    view.add_item(discord.ui.Button(label="Next", style=discord.ButtonStyle.grey))
    
    async def next_page(interaction):
        if interaction.user != ctx.author:
            return await interaction.response.send_message("This isn't your command!", ephemeral=True)
        # change the page
        view.children[0].disabled = False
        view.children[1].disabled = False
        view.page_number += 1
        if view.page_number == total - 1:
            view.children[1].disabled = True
        await interaction.message.edit(embed=embeds[view.page_number], view=view)
        await interaction.response.defer()

    async def previous_page(interaction):
        if interaction.user != ctx.author:
            return await interaction.response.send_message("This isn't your command!", ephemeral=True)
        # change the page
        view.children[0].disabled = False
        view.children[1].disabled = False
        view.page_number -= 1
        if view.page_number == 0:
            view.children[0].disabled = True
        await interaction.message.edit(embed=embeds[view.page_number], view=view)
        await interaction.response.defer()

    view.children[0].callback = previous_page
    view.children[1].callback = next_page
    view.page_number = 0
    await ctx.send(embed=embeds[0], view=view)

def getUserData(user):
    with open("users.json", "r") as f:
        try:
            users = json.load(f)
            return users[str(user.id)]
        except:
            users[str(user.id)] = {}
            users[str(user.id)]["wallet"] = 0
            users[str(user.id)]["bank"] = 0
            users[str(user.id)]["bank_limit"] = 1000
            with open("users.json", "w") as f:
                json.dump(users, f, indent=4)
            return users[str(user.id)]

@bot.command(aliases=["store", "sh"])
async def shop(ctx):
    items = [
        "Xi's Amulet",
        "Rusty Sword",
        "Dragon's Claw",
        "Golden Apple",
        "Potion of Banking",
    ]

    prices = [
        1000,
        2500,
        5000,
        10000,
        25000,
    ]

    descriptions = [
        "A magical amulet that can give you anywhere from $1 - $2500.",
        "A rusty sword that can rob players with a 90% chance of success.",
        "A claw from a dragon that can rob players with a 100% chance of success.",
        "A golden apple that can give you anywhere from $1 - $25000.",
        "A potion that can boost your bank limit by 10.",
    ]

    pages = [items[i:i+1] for i in range(0, len(items), 1)]
    total = len(pages)

    embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: Here is the shop.")

    view = discord.ui.View()
    view.add_item(discord.ui.Button(style=discord.ButtonStyle.blurple, disabled=True, custom_id="previous", emoji="<:left:1047607175717068830>"))
    view.add_item(discord.ui.Button(style=discord.ButtonStyle.green, custom_id="buy", emoji="<:approve:1047942586964385815>"))
    view.add_item(discord.ui.Button(style=discord.ButtonStyle.blurple, custom_id="next", emoji="<:right:1047607172802023514>"))

    async def next_page(interaction):
        # get the next item
        view.page_number += 1
        if view.page_number == total - 1:
            view.children[2].disabled = True
        view.children[0].disabled = False
        item = pages[view.page_number][0]
        # change the embed
        embed.clear_fields()
        embed.add_field(name=item, value=f"Price: ${prices[items.index(item)]}\nDescription: {descriptions[items.index(item)]}", inline=False)
        await interaction.message.edit(embed=embed, view=view)
        await interaction.response.defer()

    async def previous_page(interaction):
        # get the previous item
        view.page_number -= 1
        if view.page_number == 0:
            view.children[0].disabled = True
        view.children[2].disabled = False
        item = pages[view.page_number][0]
        # change the embed
        embed.clear_fields()
        embed.add_field(name=item, value=f"Price: ${prices[items.index(item)]}\nDescription: {descriptions[items.index(item)]}", inline=False)
        await interaction.message.edit(embed=embed, view=view)
        await interaction.response.defer()

    async def buy_item(interaction):
        # get the item
        item = pages[view.page_number][0]
        # get the user's data
        users = getUserData(ctx.author)
        # check if they have enough money
        if users["wallet"] < prices[items.index(item)]:
            embed2 = discord.Embed(color=0xec4245, description=f"{cross} {ctx.author.mention}: You don't have enough money to buy this item.")
            return await interaction.response.send_message(embed=embed2, ephemeral=True)
        # remove the money from their wallet
        users["wallet"] -= prices[items.index(item)]
        # give them the item
        if item == "Xi's Amulet":
            try:
                with open("users.json", "r") as f:
                    users = json.load(f)
                    users[str(ctx.author.id)]["amulet"] += 1
                    users[str(ctx.author.id)]["wallet"] = users[str(ctx.author.id)]["wallet"] - prices[items.index(item)]
                    with open("users.json", "w") as f:
                        json.dump(users, f, indent=4)
            except:
                with open("users.json", "r") as f:
                    users = json.load(f)
                    users[str(ctx.author.id)]["amulet"] = 1
                    users[str(ctx.author.id)]["wallet"] = users[str(ctx.author.id)]["wallet"] - prices[items.index(item)]
                    with open("users.json", "w") as f:
                        json.dump(users, f, indent=4)
        elif item == "Rusty Sword":
            try:
                with open("users.json", "r") as f:
                    users = json.load(f)
                    users[str(ctx.author.id)]["rusty_sword"] += 1
                    users[str(ctx.author.id)]["wallet"] = users[str(ctx.author.id)]["wallet"] - prices[items.index(item)]
                    with open("users.json", "w") as f:
                        json.dump(users, f, indent=4)
            except:
                with open("users.json", "r") as f:
                    users = json.load(f)
                    users[str(ctx.author.id)]["rusty_sword"] = 1
                    users[str(ctx.author.id)]["wallet"] = users[str(ctx.author.id)]["wallet"] - prices[items.index(item)]
                    with open("users.json", "w") as f:
                        json.dump(users, f, indent=4)
        elif item == "Dragon's Claw":
            try:
                with open("users.json", "r") as f:
                    users = json.load(f)
                    users[str(ctx.author.id)]["dragon_claw"] += 1
                    users[str(ctx.author.id)]["wallet"] = users[str(ctx.author.id)]["wallet"] - prices[items.index(item)]
                    with open("users.json", "w") as f:
                        json.dump(users, f, indent=4)
            except:
                with open("users.json", "r") as f:
                    users = json.load(f)
                    users[str(ctx.author.id)]["dragon_claw"] = 1
                    users[str(ctx.author.id)]["wallet"] = users[str(ctx.author.id)]["wallet"] - prices[items.index(item)]
                    with open("users.json", "w") as f:
                        json.dump(users, f, indent=4)
        elif item == "Golden Apple":
            try:
                with open("users.json", "r") as f:
                    users = json.load(f)
                    users[str(ctx.author.id)]["golden_apple"] += 1
                    users[str(ctx.author.id)]["wallet"] = users[str(ctx.author.id)]["wallet"] - prices[items.index(item)]
                    with open("users.json", "w") as f:
                        json.dump(users, f, indent=4)
            except:
                with open("users.json", "r") as f:
                    users = json.load(f)
                    users[str(ctx.author.id)]["golden_apple"] = 1
                    users[str(ctx.author.id)]["wallet"] = users[str(ctx.author.id)]["wallet"] - prices[items.index(item)]
                    with open("users.json", "w") as f:
                        json.dump(users, f, indent=4)
        elif item == "Potion of Banking":
            try:
                with open("users.json", "r") as f:
                    users = json.load(f)
                    users[str(ctx.author.id)]["bank_limit"] += 10
                    users[str(ctx.author.id)]["wallet"] = users[str(ctx.author.id)]["wallet"] - prices[items.index(item)]
                    with open("users.json", "w") as f:
                        json.dump(users, f, indent=4)
            except:
                with open("users.json", "r") as f:
                    users = json.load(f)
                    users[str(ctx.author.id)]["bank_limit"] = 10
                    users[str(ctx.author.id)]["wallet"] = users[str(ctx.author.id)]["wallet"] - prices[items.index(item)]
                    with open("users.json", "w") as f:
                        json.dump(users, f, indent=4)
        # send a message
        embed2 = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: You have successfully bought {item}!")
        await interaction.response.send_message(embed=embed2, ephemeral=True)

    view.children[0].callback = previous_page
    view.children[1].callback = buy_item
    view.children[2].callback = next_page
    embed.add_field(name=pages[0][0], value=f"Price: ${prices[items.index(pages[0][0])]}\nDescription: {descriptions[items.index(pages[0][0])]}")
    view.page_number = 0
    await ctx.send(embed=embed, view=view)

@bot.command()
async def inventory(ctx):
    embed = discord.Embed(color=0xec4245)
    embed.description = f"{cross} {ctx.author.mention}: This command is currently under development."
    await ctx.send(embed=embed)

@bot.command()
async def use(ctx, item, args=None):
    embed = discord.Embed(color=0xec4245)
    embed.description = f"{cross} {ctx.author.mention}: This command is currently under development."
    await ctx.send(embed=embed)

@bot.command(aliases=["pay", "give"])
async def send(ctx, member: discord.Member, amount):
    userInfo = getUserData(ctx.author.id)
    if int(amount) > userInfo["wallet"]:
        embed = discord.Embed(color=0xec4245)
        embed.description = f"{cross} {ctx.author.mention}: You do not have enough money to send ${amount}."
        await ctx.send(embed=embed)
    else:
        with open("users.json", "r") as f:
            users = json.load(f)
            users[str(ctx.author.id)]["wallet"] = users[str(ctx.author.id)]["wallet"] - int(amount)
            users[str(member.id)]["wallet"] = users[str(member.id)]["wallet"] + int(amount)
            with open("users.json", "w") as f:
                json.dump(users, f, indent=4)
        embed = discord.Embed(color=0x7dd386)
        embed.description = f"{tick} {ctx.author.mention}: You have successfully sent ${amount} to {member.mention}."
        await ctx.send(embed=embed)
            


# economy commands

@bot.command(aliases=['wallet', 'bal', 'cash', 'money'])
async def balance(ctx, member: discord.Member=None):
    if member == None:
        member = ctx.author
    userData = getUserData(member)
    embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: Here is the balance for `{member.name}`.")
    embed.add_field(name="Wallet", value=f"${int(userData['wallet'])}", inline=False)
    embed.add_field(name="Bank", value=f"${userData['bank']}/${userData['bank_limit']}", inline=False)
    await ctx.send(embed=embed)

@bot.command(aliases=['message', 'pm'])
async def gc(ctx, users: discord.Member):
    if users == ctx.author:
        embed = discord.Embed(color=0xec4245, description=f"{cross} {ctx.author.mention}: You cannot create a private channel with yourself.")
        await ctx.send(embed=embed)
        return

    for channel in ctx.guild.channels:
        if channel.name.startswith(f"private-{ctx.author.name}-"):
            embed = discord.Embed(color=0xec4245, description=f"{cross} {ctx.author.mention}: You already have a private channel open.")
            await ctx.send(embed=embed)
            return

    if users.bot:
        embed = discord.Embed(color=0xec4245, description=f"{cross} {ctx.author.mention}: You cannot create a private channel with a bot.")
        await ctx.send(embed=embed)
        return


    channel = await ctx.guild.create_text_channel(f"private-{ctx.author.name}-{users.name}")
    await channel.set_permissions(ctx.guild.default_role, read_messages=False)
    await channel.set_permissions(ctx.author, read_messages=True)
    await channel.set_permissions(users, read_messages=True)
    embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: You have successfully created a private channel with {users.mention}, this channel will be deleted in 60 seconds: <#{channel.id}>")
    embed2 = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: You have been invited to a private channel with {users.mention}, this channel will be deleted in 60 seconds: <#{channel.id}>")
    await users.send(f"{users.mention}", embed=embed2)   
    await users.send(f"{users.mention}", embed=embed)
    await ctx.send(embed=embed)
    await channel.send(f"{ctx.author.mention} {users.mention}", embed=embed)
    await asyncio.sleep(60)
    await channel.delete()
    embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: Private channel has been closed due to expiration.")
    await users.send(f"{users.mention}", embed=embed)
    await ctx.author.send(f"{ctx.author.mention}", embed=embed)

@bot.command()
@commands.cooldown(1, 25, commands.BucketType.user)
async def beg(ctx):
    begPeople = [
        "Miley Cyrus",
        "Donald Trump",
        "Joe Biden",
        "Kanye West",
        "Kim Kardashian",
        "Kendall Jenner",
        "Kylie Jenner",
        "your mom",
        "your dad",
        "your sister",
        "me",
        "Justin Bieber",
        "Selena Gomez",
        "Taylor Swift",
        "Beyonce",
        "Jay-Z",
        "Kendrick Lamar",
    ]
    if random.randint(0, 1) == 0:
        amount = 2 * random.randint(0, 75)
        with open("users.json", "r") as f:
            users = json.load(f)
            users[str(ctx.author.id)]["wallet"] += amount
            with open("users.json", "w") as f:
                json.dump(users, f, indent=4)
        embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: You begged `{random.choice(begPeople)}` and got `${amount}`.")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: You begged `{random.choice(begPeople)}` and got nothing.")
        await ctx.send(embed=embed)

@bot.command()
@commands.cooldown(1, 45, commands.BucketType.user)
async def search(ctx):
    searchPlaces = [
        "a dumpster",
        "a trash can",
        "a trash bag",
        "a trash bin",
        "a trash barrel",
        "your grandma's house",
        "your mom's house",
        "your dad's house",
        "your house",
        "your neighbor's house",
        "your taxi's car",
        "your car",
        "your truck",
        "your bike",
        "your scooter",
        "the street",
        "the sidewalk",
        "the road",
        "the highway",
        "the freeway",
        "the parking lot",
        "the parking garage",
        "the sewers",
    ]
    userData = getUserData(ctx.author)
    if random.randint(0, 1) == 0:
        earnings = 2 * random.randint(0, 300)
        userData["wallet"] += earnings
        with open("users.json", "r") as f:
            users = json.load(f)
            users[str(ctx.author.id)] = userData
            with open("users.json", "w") as f:
                json.dump(users, f, indent=4)
        embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: You searched `{random.choice(searchPlaces)}` and found `${earnings}`.")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: You searched `{random.choice(searchPlaces)}` and found nothing.")
        await ctx.send(embed=embed)

@bot.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def work(ctx):
    workPlaces = [
        "a restaurant",
        "a fast food restaurant",
        "a grocery store",
        "a gas station",
        "a movie theater",
        "a mall",
        "a clothing store",
        "a shoe store",
        "a toy store",
        "a supermarket",
        "a bakery",
        "a cafe",
        "a coffee shop",
        "a bar",
        "a nightclub",
        "a casino",
        "a bank",
        "a hospital",
        "a school",
        "a university",
        "a college",
        "a library",
        "a gym",
        "a park",
        "a zoo",
        "a museum",
        "a theater",
        "a concert hall",
        "a stadium",
        "a grocery store",
        "a gas station",
        "a movie theater",
        "a mall",
        "a clothing store",
        "a shoe store",
        "a toy store",
        "a supermarket",
        "a bakery",
        "a cafe",
        "a coffee shop",
        "a bar",
        "a nightclub",
        "a casino",
        "a bank",
        "a hospital",
        "a school",
        "a university",
        "a college",
        "a library",
        "a gym",
        "a park",
        "a zoo",
        "a museum",
        "a theater",
        "a concert hall",
        "a stadium",
        "a grocery store",
        "a gas station",
        "a movie theater",
        "a mall",
        "a clothing store",
        "a shoe store",
        "a toy store",
        "a supermarket",
        "a bakery",
        "a cafe",
        "a coffee shop",
        "a bar",
        "a nightclub",
        "a casino",
        "a bank",
        "a hospital",
        "a school",
        "a university",
        "a college",
        "a library",
        "a gym",
        "a park",
        "a zoo",
        "a museum",
        "a theater",
        "a concert hall",
        "a stadium",
        "a grocery store",
        "a gas station",
        "a movie theater",
        "a mall",
        "a clothing store",
        "a shoe store",
        "a toy store",
        "a supermarket",
        "a bakery",
    ]
    userData = getUserData(ctx.author)
    earnings = 2 * random.randint(50, 500)
    userData["wallet"] += earnings
    with open("users.json", "r") as f:
        users = json.load(f)
        users[str(ctx.author.id)] = userData
        with open("users.json", "w") as f:
            json.dump(users, f, indent=4)
    embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: You worked at `{random.choice(workPlaces)}` and earned `${earnings}`.")
    await ctx.send(embed=embed)

@bot.command(alias=['steal'])
@commands.cooldown(1, 180, commands.BucketType.user)
async def rob(ctx, member: discord.Member):
    userData = getUserData(ctx.author)
    if userData["wallet"] < 100:
        embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: You need atleast $100 in your wallet to rob someone.")
        return await ctx.send(embed=embed)
    if random.randint(0, 4) != 2:
        userData = getUserData(ctx.author)
        userData["wallet"] -= userData["wallet"] * 0.1
        with open("users.json", "r") as f:
            users = json.load(f)
            users[str(ctx.author.id)] = userData
            with open("users.json", "w") as f:
                json.dump(users, f, indent=4)
        embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: You got caught and paid a fine of 10% of your wallet.")
        await ctx.send(embed=embed)
    else:
        userData = getUserData(ctx.author)
        memberData = getUserData(member)
        if memberData["wallet"] == 0:
            embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: `{member.name}` has no money to steal.")
            await ctx.send(embed=embed)
        else:
            amount = random.randint(0, memberData["wallet"])
            userData["wallet"] += amount
            memberData["wallet"] -= amount
            with open("users.json", "r") as f:
                users = json.load(f)
                users[str(ctx.author.id)] = userData
                users[str(member.id)] = memberData
                with open("users.json", "w") as f:
                    json.dump(users, f, indent=4)
            embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: You robbed `{member.name}` and got `${amount}`.")
            await ctx.send(embed=embed)

@bot.command(aliases=["cf"])
@commands.cooldown(1, 5, commands.BucketType.user)
async def coinflip(ctx, amount: int, choice: str):
    if amount < 1:
        embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: You can't bet less than $1.")
        return await ctx.send(embed=embed)

    userData = getUserData(ctx.author)
    if userData["wallet"] < amount:
        embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: You don't have enough money in your wallet.")
        return await ctx.send(embed=embed)

    if choice.lower() not in ["heads", "tails"]:
        embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: You can only choose `heads` or `tails`.")
        return await ctx.send(embed=embed)

    embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: 🪙 Flipping the coin.")
    message = await ctx.send(embed=embed)
    await asyncio.sleep(1)
    embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: 🪙 Flipping the coin..")
    await message.edit(embed=embed)
    await asyncio.sleep(1)
    embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: 🪙 Flipping the coin...")
    await message.edit(embed=embed)
    await asyncio.sleep(1)
    result = random.choice(["heads", "tails"])
    if result == choice.lower():
        userData["wallet"] += amount
        embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: You won `${amount}`.")
        await message.edit(embed=embed)
    else:
        userData["wallet"] -= amount
        embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: You lost `${amount}`.")
        await message.edit(embed=embed)
        
    with open("users.json", "r") as f:
        users = json.load(f)
        users[str(ctx.author.id)] = userData
        with open("users.json", "w") as f:
            json.dump(users, f, indent=4)

@bot.command(aliases=['w', 'with'])
async def withdraw(ctx, amount):
    if amount.lower() == "all" or amount.lower() == "max":
        amount = getUserData(ctx.author)["bank"]
    else:
        amount = int(amount)
    userData = getUserData(ctx.author)
    if int(amount) > userData["bank"]:
        embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: You do not have that much money in your bank.")
        await ctx.send(embed=embed)
    else:
        userData["wallet"] += int(amount)
        userData["bank"] -= int(amount)
        with open("users.json", "r") as f:
            users = json.load(f)
            users[str(ctx.author.id)] = userData
            with open("users.json", "w") as f:
                json.dump(users, f, indent=4)
        embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: You withdrew `${amount}` from your bank.")
        await ctx.send(embed=embed)

@bot.command(aliases=['d', 'dep'])
async def deposit(ctx, amount):
    if amount.lower() == "all" or amount.lower() == "max":
        bankLim = getUserData(ctx.author)["bank_limit"]
        bank = getUserData(ctx.author)["bank"]
        amount = getUserData(ctx.author)["wallet"]
        if amount > bankLim - bank:
            amount = bankLim - bank
    else:
        amount = int(amount)
    userData = getUserData(ctx.author)
    if int(amount) > userData["wallet"]:
        embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: You do not have that much money in your wallet.")
        await ctx.send(embed=embed)
    else:
        if userData["bank"] + int(amount) > userData["bank_limit"]:
            embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: You cannot deposit that much money.")
            await ctx.send(embed=embed)
        else:
            userData["wallet"] -= int(amount)
            userData["bank"] += int(amount)
            with open("users.json", "r") as f:
                users = json.load(f)
                users[str(ctx.author.id)] = userData
                with open("users.json", "w") as f:
                    json.dump(users, f, indent=4)
            embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: You deposited `${amount}` into your bank.")
            await ctx.send(embed=embed)

@bot.command(aliases=['topbal', 'lb'])
async def leaderboard(ctx):
    with open("users.json", "r") as f:
        users = json.load(f)
    users = sorted(users.items(), key=lambda x: x[1]["wallet"], reverse=True)
    embed = discord.Embed(color=0x7dd386, title="Top Balance Leaderboard")
    for i, user in enumerate(users):
        if i == 10:
            break
        embed.add_field(name=f"{i+1}. {bot.get_user(int(user[0])).name}", value=f"${int(user[1]['wallet'])}", inline=False)
    await ctx.send(embed=embed)


@bot.command(aliases=['bl'])
async def banklimit(ctx):
    userData = getUserData(ctx.author)
    embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: Your bank limit is `${userData['bank_limit']}`. You can upgrade your bank limit by using `=upgrade`.")
    await ctx.send(embed=embed)

@bot.command(aliases=['up'])
async def upgrade(ctx):
    userData = getUserData(ctx.author)
    if userData["bank_limit"] == 100000:
        embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: You cannot upgrade your bank limit anymore.")
        await ctx.send(embed=embed)
    else:
        if userData["wallet"] < 3000:
            embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: You need atleast $3000 in your wallet to upgrade your bank limit.")
            await ctx.send(embed=embed)
        else:
            userData["wallet"] -= 3000
            userData["bank_limit"] += 1000
            with open("users.json", "r") as f:
                users = json.load(f)
                users[str(ctx.author.id)] = userData
                with open("users.json", "w") as f:
                    json.dump(users, f, indent=4)
            embed = discord.Embed(color=0x7dd386, description=f"{tick} {ctx.author.mention}: You upgraded your bank limit by $1,000.")
            await ctx.send(embed=embed)
        

@bot.command()
async def help(ctx):
    category = None
    if category == None:
        embed = discord.Embed(color=0x2F3136)
        embed.set_author(name="Glare Help", icon_url="https://cdn.discordapp.com/avatars/1041333675452813312/f84faaff39047f9a00fb6fd6551f8be7.png?size=1024")
        embed.description = f'{helpE} {ctx.author.mention}: Here are the available **commands** for Glare.'
        select = Select(
        placeholder = "Choose a category...",
        options=[
            discord.SelectOption(label='Home', emoji=f'{home}', description='Return to the home page of the help command.'),
            discord.SelectOption(label='Moderation', emoji=f'{moderation}', description='Preview all of the moderation commands.'),
            discord.SelectOption(label='Utility', emoji=f'{utility}', description='Preview all of the utility commands.'),
            discord.SelectOption(label='Economy', emoji=f'{fun}', description='Preview all of the economy commands.'),
            discord.SelectOption(label='Other', emoji=f'{other}', description='Preview all of the uncategorized commands.'),
         ])

        async def my_callback(interaction):
            if interaction.user != ctx.author:
                return await interaction.response.send_message("This isn't your command!", ephemeral=True)
            if select.values[0] == "Home":
                embed = discord.Embed(color=0x2F3136)
                embed.set_author(name="Glare Help", icon_url="https://cdn.discordapp.com/avatars/1041333675452813312/f84faaff39047f9a00fb6fd6551f8be7.png?size=1024")
                embed.description = f'{helpE} {ctx.author.mention}: here are the available **commands** for Glare.'
                await message1.edit(embed=embed, view=view)
                await interaction.response.defer()
            if select.values[0] == "Moderation":
                embed = discord.Embed(color=0x2F3136)
                embed.set_author(name="Glare Help", icon_url="https://cdn.discordapp.com/avatars/1041333675452813312/f84faaff39047f9a00fb6fd6551f8be7.png?size=1024")
                embed.description = f'{helpE} {ctx.author.mention}: here are the available **moderation** commands for Glare.\n\n`,muterole` - Sets the muterole for the server the command is used in.\n`,mute` - Mutes a member in the server the command is used in.\n`,muteinfo` - Gets the mute info of a member in the server the command is used in.\n`,unmute` - Unmutes a member in the server the command is used in.\n`,kick` - Kicks a member from the server the command is used in.\n`,ban` - Bans a member from the server the command is used in.\n`,unban` - Unbans a member from the server the command is used in.\n`,purge` - Purges messages from the channel the command is used in.\n`,slowmode` - Sets the slowmode of the channel the command is used in.\n`,lock` - Locks the channel the command is used in.\n`,unlock` - Unlocks the channel the command is used in.'
                await message1.edit(embed=embed, view=view)
                await interaction.response.defer()
            if select.values[0] == "Utility":
                embed = discord.Embed(color=0x2F3136)
                embed.set_author(name="Glare Help", icon_url="https://cdn.discordapp.com/avatars/1041333675452813312/f84faaff39047f9a00fb6fd6551f8be7.png?size=1024")
                embed.description = f'{helpE} {ctx.author.mention}: here are the available **utility** commands for Glare.\n\n`,help` - Shows the help command.\n`,convert` - Converts a currency to another currency.\n`,ping` - Shows the bot\'s latency.\n`,serverinfo` - Shows the server\'s info.\n`,userinfo` - Shows the user\'s info.\n`,avatar` - Shows the user\'s avatar.\n`,invite` - Shows the bot\'s invite link.'
                await message1.edit(embed=embed, view=view)
                await interaction.response.defer()
            if select.values[0] == "Economy":
                embed = discord.Embed(color=0x2F3136)
                embed.set_author(name="Glare Help", icon_url="https://cdn.discordapp.com/avatars/1041333675452813312/f84faaff39047f9a00fb6fd6551f8be7.png?size=1024")
                embed.description = f'{helpE} {ctx.author.mention}: here are the available **economy** commands for Glare.\n\n`,balance` - Shows the user\'s balance.\n`,beg` - Begs for money.\n`,work` - Works for money.\n`,deposit` - Deposits money into the bank.\n`,withdraw` - Withdraws money from the bank.\n`,send` - Sends money to another user.\n`,rob` - Robs another user.\n`,shop` - Shows the shop.\n`,search` - Searches for money.\n`,send` - Sends money to another user.\n`,coinflip` - Coinflips for money.'
                await message1.edit(embed=embed, view=view)
                await interaction.response.defer()
            if select.values[0] == "Other":
                embed = discord.Embed(color=0x2F3136)
                embed.set_author(name="Glare Help", icon_url="https://cdn.discordapp.com/avatars/1041333675452813312/f84faaff39047f9a00fb6fd6551f8be7.png?size=1024")
                embed.description = f'{helpE} {ctx.author.mention}: here are the available **other** commands for Glare.\n\n`Coming soon!`'
                await message1.edit(embed=embed, view=view)
                await interaction.response.defer()

        select.callback = my_callback
        view = View()
        view.add_item(select)
        message1 = await ctx.send(embed=embed, view=view)

@bot.command()
async def meme(ctx):
    links = [
        "https://cdn.discordapp.com/attachments/1045197850847490098/1047978331049570408/670fb195927de864a04471417ad1779f.mp4-2.mp4",
        "https://cdn.discordapp.com/attachments/1045197850847490098/1047977665191219260/CiX2yysxP25rg-aM.mp4",
        "https://cdn.discordapp.com/attachments/1045197850847490098/1047977369064980590/trim.1DA0C696-A87B-4757-AC43-12EDEF9F3993.mov",
        "https://cdn.discordapp.com/attachments/1046842382739582986/1047988831355412560/unknown.png",
        "https://cdn.discordapp.com/attachments/1045197850847490098/1047988721275904020/ihatethisstupidphone.mp4",
        "https://media.discordapp.net/attachments/1045197850847490098/1047988754620629012/FB960A42-502E-43CB-A18B-9CDBE1DFF513.jpg?width=697&height=671",
        "https://cdn.discordapp.com/attachments/1045197850847490098/1047988766624723074/IMG_2389.jpg",
        "https://cdn.discordapp.com/attachments/1045197850847490098/1047988824061513768/596666AC-5DEA-4F06-AA08-D1C29093C511.mov",
        "https://cdn.discordapp.com/attachments/1045197850847490098/1047978725964255292/SOLOLEO_IS_A_FUCKING_CREEP.mp4",
        "https://cdn.discordapp.com/attachments/1045197850847490098/1047972522039201893/trim.E0E6C7DE-BEB4-4C08-8E80-474DC139C47F.mov",
        "https://cdn.discordapp.com/attachments/1045197850847490098/1047969787973750804/trim.D4E6335F-6FF7-4181-9F40-34F00EE844DE.mov",
        "https://cdn.discordapp.com/attachments/1045197850847490098/1047950583635644436/v12044gd0000ce3d50bc77u07i1vgmvg.mp4",
        "https://cdn.discordapp.com/attachments/1045197850847490098/1047947096285794394/trim.1C35024C-5BAB-4BD5-A91B-7DC0761099C1.mov",
        "https://cdn.discordapp.com/attachments/1045197850847490098/1047946383233138728/small_ass_house_1.mp4",
        "https://cdn.discordapp.com/attachments/1045197850847490098/1047942104887869460/trim.6B585B0C-5413-467D-97BF-8E33D348A519.mov",
        "https://cdn.discordapp.com/attachments/1045197850847490098/1047941785307066408/trim.389B5D13-0FC6-4693-8BF9-241392C3937D.mov",
    ]

    randomLink = random.choice(links)
    await ctx.reply(randomLink)

@bot.command()
async def mCache(ctx):
    if ctx.author.id == 550752995458023427:
        await ctx.message.attachments[0].save("cache.png")
        await ctx.reply("Done!")
    else:
        await ctx.reply("You don't have permission to use this command!")

@bot.command()
async def mFetch(ctx):
    if ctx.author.id == 550752995458023427:
        await ctx.reply(file=discord.File("cache.png"))
    else:
        await ctx.reply("You don't have permission to use this command!")
        
@bot.event
async def on_ready():
    os.system('cls')
    channels = 0
    guilds = 0
    members = 0

    for folder in os.listdir("C:\\Users\\aklam\\Music\\\\Soul\\Guilds"):
        guilds += 1

    for guild in bot.guilds:
        if not os.path.exists(f"C:\\Users\\aklam\\Music\\\\Soul\\Guilds\\{guild.id}"):
            os.mkdir(f"C:\\Users\\aklam\\Music\\\\Soul\\Guilds\\{guild.id}")
            guilds += 1
            with open(f"C:\\Users\\aklam\\Music\\\\Soul\\Guilds\\{guild.id}\\config.json", "w") as f:
                json.dump({"muterole": None}, f, indent=4)

            with open(f"C:\\Users\\aklam\\Music\\\\Soul\\Guilds\\{guild.id}\\muted.json", "w") as f:
                json.dump({}, f, indent=4)

        for channel in guild.channels:
            channels += 1

        for member in guild.members:
            members += 1
    print(f"{prefix} Logged in as {bot.user.name}#{bot.user.discriminator}")
    print(f"{prefix} Connected to {guilds} guilds, {channels} channels, and {members} members.")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{members} members"), status=discord.Status.idle)
    for guild in bot.guilds:
        try:
            invite = await guild.text_channels[0].create_invite(max_age=0)
            print(f"{prefix} Invite for {guild.name}: {invite}")
        except:
            print(f"{prefix} Couldn't create invite for {guild.name}")

    while True:
        for guild in bot.guilds:
            config = json.load(open(f"C:\\Users\\aklam\\Music\\\\Soul\\Guilds\\{guild.id}\\config.json", "r"))
            with open(f"C:\\Users\\aklam\\Music\\\\Soul\\Guilds\\{guild.id}\\muted.json", "r") as f:
                muted = json.load(f)

            try:
                if muted:
                    for member in muted:
                        if muted[member]["duration"]:
                            if time.time() > muted[member]["time"] + muted[member]["duration"]:
                                role = guild.get_role(config["muterole"])
                                await guild.get_member(int(member)).remove_roles(role)
                                del muted[member]
                                with open(f"C:\\Users\\aklam\\Music\\\\Soul\\Guilds\\{guild.id}\\muted.json", "w") as f:
                                    json.dump(muted, f, indent=4)
            except:
                pass
        await asyncio.sleep(5)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.author.id == 550752995458023427:
        return await bot.process_commands(message)

    with open("authorised.txt", "r") as f:
        for line in f:
            if line.strip() == str(message.guild.id):
                await bot.process_commands(message)
                return
        else:
            pass

    if message.content.startswith(botPrefix):
        embed = discord.Embed(color=0xec4245, description=f"{warning} {message.author.mention}: This server is not `authorised` to use **glare**.")
        return await message.channel.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(color=0xec4245, description=f"{warning} {ctx.author.mention}: You are on cooldown. Try again in `{error.retry_after:.2f}` seconds.")
        return await ctx.send(embed=embed)

@bot.event
async def on_member_update(before, after):
    with open(f"C:\\Users\\aklam\\Music\\\\Soul\\Guilds\\{before.guild.id}\\muted.json", "r") as f:
        muted = json.load(f)
    if str(before.id) in muted:
        if muted[str(before.id)]["duration"]:
            if muted[str(before.id)]["unmutedin"] <= time.time():
                mutedrole = discord.utils.get(before.guild.roles, name="Muted")
                await before.remove_roles(mutedrole)
                del muted[str(before.id)]
                with open(f"C:\\Users\\aklam\\Music\\\\Soul\\Guilds\\{before.guild.id}\\muted.json", "w") as f:
                    json.dump(muted, f, indent=4)
bot.run('')