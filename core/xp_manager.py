import discord
import asyncio
from core import sql_manager as sql

def add_xp(server_id, entity_id, xp):
	current_xp = sql.get_xp(server_id, entity_id)

	level = get_level_from_xp(current_xp)

	sql.update_xp_table(server_id, entity_id, str(int(current_xp) + int(xp)))
	new_level = get_level_from_xp(int(current_xp) + int(xp))

	return new_level if level != new_level else None

def get_level(server_id, entity_id):
	return get_level_from_xp(sql.get_xp(server_id, entity_id))

def get_xp(server_id, entity_id):
	return sql.get_xp(server_id, entity_id)

def get_level_xp(n):
	return 5*(n**2)+50*n+100


def get_level_from_xp(xp):
	remaining_xp = int(xp)
	level = 0
	while remaining_xp >= get_level_xp(level):
		remaining_xp -= get_level_xp(level)
		level += 1
	return level
