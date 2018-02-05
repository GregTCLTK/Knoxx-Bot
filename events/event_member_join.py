import discord

client = discord.Client()

def execute(member):
	yield from client.send_message(member, "Willkommen auf %s" % (member.server.name))

