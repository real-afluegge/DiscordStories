import discord
from discord.ext import commands
from discord.utils import get
import asyncio
from pymongo import MongoClient

# log-in to the database
database = MongoClient("mongodb+srv://username:password@cluster0.tmmhm.mongodb.net/notes?retryWrites=true&w=majority")
db = database.test

def get_prefix(client, message):

    prefixes = ['DS-']
    return commands.when_mentioned_or(*prefixes)(client, message)

bot = commands.Bot(                         # Create a new bot
    command_prefix=get_prefix,              # Set the prefix
    description='discord stories',  # Set a description for the bot
    owner_id=299199651876438016,            # Your unique User ID
    case_insensitive=True                   # Make the commands case insensitive
)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    # as soon as the bot starts, create msg deletion task
    bot.loop.create_task(msg_task())
    
# STATUS TASKS
async def msg_task():
    while True:
        # unlock the database
        st = db.discordStories
        for x in st.find():
            # iterate through every id in the database
            query = x
            channel_id = query["channel_id"]
            cur_id = bot.get_channel(int(channel_id))
            messages = await cur_id.history(limit=200).flatten()
            
            # get the message, remove ir
            msg_id = messages[-1].id
            msg = await cur_id.fetch_message(msg_id)
            await msg.delete()
        # waits 5 minutes before running again to delete the top message from the channel
        await asyncio.sleep(300)


@bot.command()
async def SetStory(ctx, id):
    """Using the channels ID, set the channel you'd like to be your story channel."""
    
    # the id given by the user is passed to the database
    st = db.discordStories
    new_id = {"channel_id": id}
    st.insert_one(new_id)
    
    # "you have enabled stories." message
    await ctx.send("this channel is now marked as a story channel. messages will be deleted every 5 minutes.")
    
bot.run('bot id', bot=True, reconnect=True)
