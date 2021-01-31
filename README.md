# DiscordStories ![made with python](https://img.shields.io/badge/made%20with-python-brightgreen)
The program utilizes python, mongoDB/pymongo, and discord.py.

This project is the code for a discord bot with two features. The one command it has allows users to designate a channel as a "story" channel in their discord server, which will be saved within a database of channels all marked as this.

When the bot runs, it starts a looping task with it. This task will, every five minutes, loop through the database for channels marked as "story" channels. From these channels, it will delete the earliest message it finds.
