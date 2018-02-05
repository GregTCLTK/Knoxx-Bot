from threading import Thread
import discord
import asyncio
import logging

class GameAnimator():
    def __init__(self, client):
        self.client = client
        self.currentGame = 0
        self.gameList = {
            0: "mit Usern von %s Servern" % len(client.servers),
            1: "mit RTL 2",
            2: "Dome auf Facebook stalken",
            3: "mit seinem nicht tollen Discriminator",
            4: "leider nicht mit Schokolade",
            5: "mit Skidder aka. Greg",
            6: "nichts LOL!",
            7: "Coded by Greg",

        }
        self.loop = asyncio.new_event_loop()
        t = Thread(target=self.run, args=(self.loop,))
        t.start()
        self.loop.call_soon_threadsafe(asyncio.async, self.animate())

    def run(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    @asyncio.coroutine
    def animate(self):
        while True:
            yield from self.client.change_presence(game=discord.Game(name=self.gameList.get(self.currentGame)))
            logging.info("Spiel Status gechanged zu: %s" % self.gameList.get(self.currentGame))

            if self.currentGame == len(self.gameList):
                self.currentGame = 0
            else:
                self.currentGame += 1

            if self.gameList.get(self.currentGame) == "":
                self.currentGame = 0

            yield from asyncio.sleep(30)
