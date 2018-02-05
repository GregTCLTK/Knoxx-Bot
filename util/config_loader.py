import sqlite3
from core import sql_manager as sql

tbl_config = "knoxx_config"

def get_prefix():
    db = sqlite3.connect('data/datas.db')
    c = db.cursor()

    c.execute("SELECT value FROM %s WHERE key='prefix'" % (tbl_config))
    data = c.fetchone()
    db.close()
    return data[0]



def get_token():
	db = sqlite3.connect('data/datas.db')
	c = db.cursor()

	c.execute("SELECT value FROM %s" % (tbl_config))
	data = c.fetchone()
	db.close()
	return data[0]

def set_token(token):
   sql.update_config_table("token", token)



def get_restart_channel():
	db = sqlite3.connect('data/datas.db')
	c = db.cursor()

	c.execute("SELECT value FROM %s WHERE key='restart_channel'" % (tbl_config))
	data = c.fetchone()
	db.close()
	return data[0]

def set_restart_channel(channel_id):
	sql.update_config_table("restart_channel", channel_id)



def get_restart_message():
	db = sqlite3.connect('data/datas.db')
	c = db.cursor()

	c.execute("SELECT value FROM %s WHERE key='restart_message'" % (tbl_config))
	data = c.fetchone()
	db.close()
	return data[0]

def set_restart_message(message_id):
	sql.update_config_table("restart_message", message_id)



def get_cmd_count():
	db = sqlite3.connect('data/datas.db')
	c = db.cursor()

	c.execute("SELECT value FROM %s WHERE key='cmd_count'" % (tbl_config))
	data = c.fetchone()
	db.close()
	return data[0]

def set_cmd_count(cmd_count):
	sql.update_config_table("cmd_count", cmd_count)



def get_version():
	db = sqlite3.connect('data/datas.db')
	c = db.cursor()

	c.execute("SELECT value FROM %s WHERE key='version'" % (tbl_config))
	data = c.fetchone()
	db.close()
	return data[0]

def set_version(version):
	sql.update_config_table("version", version)