import discord
import asyncio
import datetime
import sqlite3
import os
import random


from util import config_loader as cf
from core import sql_manager as sql
from core import game_animator, sql_manager, guild as guildObj
from core import permissions_manager as permm
from core import xp_manager as xp


#from commands.info import cmd_help
from commands.botowner import cmd_servers
#from commands.info import cmd_uptime
#from commands.info import cmd_serverinfo
#from commands.info import cmd_userinfo
#from commands.info import cmd_invite
#from commands.info import cmd_membercount
#from commands.info import cmd_info
from commands.info import cmd_xp

#from commands.test import test

#from commands.fun import cmd_rps
#from commands.fun import cmd_gangster
#from commands.fun import cmd_music

from commands.administrator import cmd_permission
from commands.administrator import cmd_prefix

from commands.moderator import cmd_clear

#from commands.owner import cmd_restart
#from commands.owner import cmd_stop
#from commands.owner import cmd_cls
#from commands.owner import cmd_getinvite
#from commands.owner import cmd_createchannel
#from commands.owner import cmd_addcmd
#from commands.owner import cmd_poop


from events import event_server_join
from events import event_member_join

client = discord.Client()
now = datetime.datetime.now()
os.system('cls')

commands = {

    #"rps": cmd_rps,
    #"rock-paper-scissor": cmd_rps,
    #"gangster": cmd_gangster,
    #"music": cmd_music,


    #"serverinfo": cmd_serverinfo,
    #"userinfo": cmd_userinfo,
    #"uptime": cmd_uptime,
    #"help": cmd_help,
    #"invite": cmd_invite,
    #"membercount": cmd_membercount,
    #"info": cmd_info,
    "xp": cmd_xp,


    "permission": cmd_permission,
    "perm": cmd_permission,
    "prefix": cmd_prefix,


    "clear": cmd_clear,

    "servers": cmd_servers,
    #"restart": cmd_restart,
    #"rs": cmd_restart,
    #"cls": cmd_cls,
    #"stop": cmd_stop,
    #"test": test,
    #"getinvite": cmd_getinvite,
    #"createchannel": cmd_createchannel,
    #"addcmd": cmd_addcmd,
    #"poop": cmd_poop,
}

sql_manager.init()


async def delete_message(self, msg):
    if not msg.channel.is_private:
        if msg.server.me.permissions_in(msg.channel).manage_messages or msg.author == self.user:
            await discord.Client.delete_message(self, msg)
            return True
    return False


#@client.event
#@asyncio.coroutine
#def on_server_join(server):
#    yield from event_server_join.execute(server, client)


@client.event
@asyncio.coroutine
def on_ready():
    db = sqlite3.connect('data/datas.db')
    c = db.cursor()

    print(now.strftime("%Y.%m.%d - %H:%M:%S"))
    time = now.strftime("%Y.%m.%d - %H:%M:%S")

    cf.set_cmd_count(len(commands))

    sql.update_config_table("last_restart", time)
    print("Der Bot wurde ergolgreich geatartet auf:\n")
    [(lambda s: print("  - %s (%s)" % (s.name, s.id)))(s) for s in client.servers]

    for s in client.servers:
        print("\t- %s (%s)  " % (s.name, s.id))
    game_animator.GameAnimator(client)

    if not cf.get_restart_message() == "None":
        embed = discord.Embed(description="Neugestartet!", color=0x5bfc58)
        embed.set_author(name="Bot wurde erfolgreich neu gestartet!!!!!")
        embed.set_thumbnail(url='https://goo.gl/wLUTz7')
        embed.set_footer(text=now.strftime("%Y.%m.%d - %H:%M:%S"))

        msg = yield from client.send_message(client.get_channel(cf.get_restart_channel()), embed=embed)
        yield from asyncio.sleep(10)
        yield from client.delete_message(msg)

        cf.set_restart_channel(None)
        cf.set_restart_message(None)


@client.event
@asyncio.coroutine
def on_member_join(member):
    yield from client.send_message(member, "Willkommen auf %s" % (member.server.name))


@client.event
@asyncio.coroutine
def on_message(message):
    level_up = xp.add_xp(message.server.id, message.author.id, random.randint(15, 25))
    if level_up != None:
        print("Jemand ist nun ein Level höher")


    now = datetime.datetime.now()

    guild = guildObj.Guild(message.server.id)
    if message.content.lower().startswith("bot"):
        yield from client.send_message(message.channel,
                                       message.author.mention + " Yeah 1 Bot sowas in der Art bin ich mache %shelp um mit mir zu spielen^^" % guildObj.Guild(
                                           message.server.id).get_prefix())
    elif message.content.startswith(guild.get_prefix()):
        yield from client.add_reaction(message, "a:alert:409012520171339793")
        invoke = message.content[len(guild.get_prefix()):].split(" ")[0]
        invoke = invoke.lower()
        args = message.content.split(" ")[1:]
        if commands.__contains__(invoke):
            yield from client.delete_message(message)

            '''embed=discord.Embed(title=guild.get_prefix() + invoke, str(" ".join(args)), color=0x36f36f)
			embed.set_author(name=message.author, icon_url=message.author.avatar_url)
			embed.set_footer(text=now.strftime("[%d.%m.%Y - %H:%M:%S]"))
			yield from client.send_message(client.get_channel("360798768385490944"), embed=embed)'''

            if (permm.user_has_permissions(client, message.server.id, message.author.id, invoke) == True):
                embeds = yield from commands.get(invoke).execute(args, message, client, invoke)
                try:
                    embed = embeds[0]
                    delete_after = int(embeds[1])
                except:
                    embed = embeds
                    delete_after = 20

                if not embed == None:
                    embed.set_footer(text=now.strftime("%Y.%m.%d - %H:%M:%S"))
                    yield from client.send_message(message.channel, embed=embed)
                    if delete_after != 0:
                        yield from asyncio.sleep(delete_after)
                        #yield from client.delete_message(msg)
            else:
                msg = yield from client.send_message(message.channel, embed=discord.Embed(color=discord.Color.red(),
                                                                                          description=(
                                                                                              "Du hast keine Rechte für %s" % (
                                                                                                  guild.get_prefix() + invoke))))
                yield from asyncio.sleep(20)
                yield from client.delete_message(msg)
        else:
            msg = yield from client.send_message(message.channel, embed=discord.Embed(color=discord.Color.red(),
                                                                                      description=(
                                                                                          "%s ist kein Command mache %shelp für eine Liste der Commands!" % (
                                                                                              guild.get_prefix() + invoke,
                                                                                              guild.get_prefix()))))
            yield from asyncio.sleep(20)
            yield from client.delete_message(msg)


client.run(cf.get_token())
