import sqlite3
import sys
import datetime

now = datetime.datetime.now()

tbl_config = "knoxx_config"
tbl_cmd = "knoxx_cmd"
tbl_prefix = "knoxx_prefix"
tbl_permission = "knoxx_permissions"
tbl_autorole = "knoxx_autorole"
tbl_xp = "knoxx_xp"
tbl_automsg = "knoxx_automsg"

def init():
	db = sqlite3.connect('data/datas.db')
	c = db.cursor()

	c.execute("CREATE TABLE IF NOT EXISTS %s(key TEXT, value TEXT)" % tbl_config)
	c.execute("CREATE TABLE IF NOT EXISTS %s(cmd TEXT, info TEXT, usage TEXT, alias TEXT, perm_level TEXT, category TEXT)" % tbl_cmd)
	c.execute("CREATE TABLE IF NOT EXISTS %s(server_id TEXT, prefix TEXT)" % tbl_prefix)
	c.execute("CREATE TABLE IF NOT EXISTS %s(server_id TEXT, entity_id TEXT, type TEXT, commands TEXT)" % tbl_permission)
	c.execute("CREATE TABLE IF NOT EXISTS %s(server_id TEXT, roles TEXT)" % tbl_autorole)
	c.execute("CREATE TABLE IF NOT EXISTS %s(server_id TEXT, entity_id TEXT, xp TEXT)" % tbl_xp)
	c.execute("CREATE TABLE IF NOT EXISTS %s(server_id TEXT, on_join TEXT, on_leave TEXT)" % tbl_automsg)

	c.execute("SELECT * FROM %s" % tbl_config)
	if(c.fetchall() == "[]"):
		print("DATABASE IS EMPTY!\nClosing application...!")
		sys.exit(0)
	db.close()

	insert_restart_data()

def insert_restart_data():
	db = sqlite3.connect('data/datas.db')
	c = db.cursor()

	c.execute("SELECT value FROM %s WHERE key='restart_channel'" % tbl_config)
	if c.fetchall() == "[]":
		c.execute("INSERT INTO %s (key, value) VALUES (?, ?)" % tbl_config, ("restart_channel", "none"))
		db.commit()

	c.execute("SELECT value FROM %s WHERE key='restart_message'" % tbl_config)
	if c.fetchall() == "[]":
		c.execute("INSERT INTO %s (key, value) VALUES (?, ?)" % tbl_config, ("restart_message", "none"))
		db.commit()
	db.close()

def update_prefix_table(server_id, prefix):
	db = sqlite3.connect('data/datas.db')
	c = db.cursor()

	c.execute("SELECT prefix FROM %s WHERE server_id='%s'" % (tbl_prefix, server_id))
	if c.fetchone() == None:
		c.execute("INSERT INTO %s (server_id, prefix) VALUES (?, ?)" % tbl_prefix, (server_id, prefix))
		db.commit()
	else:
		c.execute("UPDATE %s SET prefix='%s' WHERE server_id='%s'" % (tbl_prefix, prefix, server_id))
		db.commit()
	db.close()

def update_config_table(key, value):
	db = sqlite3.connect('data/datas.db')
	c = db.cursor()

	c.execute("SELECT value FROM %s WHERE key='%s'" % (tbl_config, key))
	if c.fetchall() == "[]":
		c.execute("INSERT INTO %s (key, value) VALUES (?, ?)" % tbl_config, (key, value))
		db.commit()
	else:
		c.execute("UPDATE %s SET value='%s' WHERE key='%s'" % (tbl_config, value, key))
		db.commit()
	db.close()


def update_autorole_table(server_id, role_id):
	db = sqlite3.connect('data/datas.db')
	c = db.cursor()

	c.execute("SELECT roles FROM %s WHERE server_id='%s'" % (tbl_autorole, server_id))
	if c.fetchone() == None:
		c.execute("INSERT INTO %s (server_id, roles) VALUES (?, ?)" % tbl_autorole, (server_id, role_id))
		db.commit()
	else:
		c.execute("UPDATE %s SET roles='%s' WHERE server_id='%s'" % (tbl_autorole, role_id, server_id))
		db.commit()
	db.close()

def get_autorole(server_id):
	db = sqlite3.connect('data/datas.db')
	c = db.cursor()

	c.execute("SELECT roles FROM %s WHERE server_id='%s'" % (tbl_autorole, server_id))
	return c.fetchone()


def update_xp_table(server_id, entity_id, xp):
	db = sqlite3.connect('data/datas.db')
	c = db.cursor()

	c.execute("SELECT xp FROM %s WHERE server_id='%s' AND entity_id='%s'" % (tbl_xp, server_id, entity_id))
	if c.fetchone() == None:
		c.execute("INSERT INTO %s (server_id, entity_id, xp) VALUES (?, ?, ?)" % tbl_xp, (server_id, entity_id, xp))
		db.commit()
	else:
		c.execute("UPDATE %s SET xp='%s' WHERE server_id='%s' AND entity_id='%s'" % (tbl_xp, xp, server_id, entity_id))
		db.commit()
	db.close()

def get_xp(server_id, entity_id):
	db = sqlite3.connect('data/datas.db')
	c = db.cursor()

	try:
		c.execute("SELECT xp FROM %s WHERE server_id='%s' AND entity_id='%s'" % (tbl_xp, server_id, entity_id))
		return c.fetchone()[0]
	except:
		return 0


def update_automsg_table(server_id, on_join, on_leave):
	db = sqlite3.connect('data/datas.db')
	c = db.cursor()

	c.execute("SELECT on_join AND on_leave FROM %s WHERE server_id='%s'" % (tbl_automsg, server_id))
	if c.fetchone() == None:
		c.execute("INSERT INTO %s (server_id, on_join, on_leave) VALUES (?, ?, ?)" % tbl_automsg, (server_id, on_join. on_leave))
		db.commit()
	else:
		c.execute("UPDATE %s SET on_join='%s' AND on_leave='%s' WHERE server_id='%s'" % (tbl_automsg, on_join, on_leave, server_id))
		db.commit()
	db.close()

def get_automsg(server_id):
	db = sqlite3.connect('data/datas.db')
	c = db.cursor()

	try:
		c.execute("SELECT on_join AND on_leave FROM %s WHERE server_id='%s'" % (tbl_automsg, server_id))
		return c.fetchall()
	except:
		return 0