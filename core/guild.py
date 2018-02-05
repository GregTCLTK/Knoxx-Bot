import sqlite3
import os
import os.path
import asyncio
from core import sql_manager as sql
from util import config_loader as cf

tbl_prefix = "knoxx_prefix"

class Guild:
    def __init__(self, guild_id):
        self.guildID = guild_id

    def get_prefix(self):
        try:
            db = sqlite3.connect('data/datas.db')
            c = db.cursor()
            c.execute("SELECT prefix FROM %s WHERE server_id='%s'" % (tbl_prefix, self.guildID))
            data = c.fetchone()
            db.close()
            return data[0]
        except:
            return cf.get_prefix()

    def set_prefix(self, client, prefix):
        sql.update_prefix_table(self.guildID, prefix)
        #await client.change_nickname(client.user, "test")
