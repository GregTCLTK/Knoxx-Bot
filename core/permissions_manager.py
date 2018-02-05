import sqlite3

tbl_permission = "knoxx_permissions"

commands_whitelist = {
	"help",
	"invite",
	"serverinfo",
	"userinfo",
	"servers",
	"rps",
	"uptime",
	"membercount",
	"xp",
}

commands_blacklist = {
	"restart",
	"rs",
	"cls",
	"stop",
	"test",
	"getinvite",
	"createchannel",
	"addcmd",
	"poop",
	"servers",
}

#getter
def user_has_permissions(client, server_id, user_id, command):
	if user_is_bot_owner(user_id) == True:
		return True
	if commands_blacklist.__contains__(command):
		return False
	if commands_whitelist.__contains__(command):
		return True
	else:
		if user_is_server_owner(client, server_id, user_id) == True:
			return True
		else:
			db = sqlite3.connect('data/datas.db')
			c = db.cursor()
			c.execute("SELECT commands FROM %s WHERE server_id='%s' AND entity_id='%s' AND type='user'" % (tbl_permission, server_id, user_id))
			entry = c.fetchone()
			if entry == None:
				c.execute("INSERT INTO %s (server_id, entity_id, type, commands) VALUES (?, ?, ?, ?)" % tbl_permission, (str(server_id), str(user_id), "user", ""))
				return False
			if "*" in entry[0] and user_is_bot_owner(user_id) == True:
				return True
			if command in entry[0]:
				return True
			else:
				return False

def user_is_bot_owner(user_id):
	Greg = "362270177712275491"
	if user_id == Greg:
		return True
	else:
		return False

def user_is_server_owner(client, server_id, user_id):
	if client.get_server(server_id).owner.id == user_id:
		return True
	else:
		return False

def add_perm_to_user(server_id, user_id, command):
	db = sqlite3.connect('data/datas.db')
	c = db.cursor()
	try:
		c.execute("SELECT commands FROM %s WHERE server_id='%s' AND entity_id='%s' AND type='user'" % (tbl_permission, server_id, user_id))
		entry = c.fetchone()
		if not entry:
			c.execute("INSERT INTO %s (server_id, entity_id, type, commands) VALUES (?, ?, ?, ?)" % tbl_permission, (str(server_id), str(user_id), "user", str(command + ";")))
			db.commit()
		else:
			commands = entry[0] + "%s;" % command
			c.execute("UPDATE %s SET commands='%s' WHERE server_id='%s' AND entity_id='%s' AND type='user'" % (tbl_permission, commands, server_id, user_id))
			db.commit()
	except:
		print("Error beim Permission adden ;(!")
	db.close()
def remove_perm_from_user(server_id, user_id, command):
	db = sqlite3.connect('data/datas.db')
	c = db.cursor()
	c.execute("SELECT commands FROM %s WHERE server_id='%s' AND entity_id='%s' AND type='user'" % (tbl_permission, server_id, user_id))
	entry = c.fetchone()
	if entry:
		command_new = entry[0].replace(command + ";", "")
		c.execute("UPDATE %s SET commands='%s' WHERE server_id='%s' AND entity_id='%s' AND type='user'" % (tbl_permission, command_new, server_id, user_id))
		db.commit()
	db.close()
