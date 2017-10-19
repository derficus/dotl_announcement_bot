import discord
from discord import Forbidden
from discord.errors import NotFound
import asyncio
from command_parser import Parser
from command_scheduler import Scheduler

client = discord.Client()

class Bot(Parser, Scheduler):
    def __init__(self, client):
        super().__init__(client)
    

bot = Bot(client)
bot.schedule_periodic(
    bot.check_rss_factory(
        "http://www.daughterofthelilies.com/rss.php",
        "281960431738683396",
        "Hey @everyone! A new page just went up: %%%. Enjoy :3"
    ),
    30 * 60,
    0
)

@client.event
async def on_ready():
    print('------')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await bot.start_task(0)
    print("Started all tasks")

@client.event
async def on_message(message):
    # response should be an Embed
    response = await bot.parse(message)
    output = bot.format_embed(message.author, response)
    if output is not None:
        if bot.is_yes(bot.db[message.author.id, "delete_command"]):
            try:
                await client.delete_message(message)
            except (Forbidden, NotFound):
                pass
            
        rspmsg = await client.send_message(message.channel, embed=output)
        # If this is turned on and you still don't want it
        # deleted, just make main_parser send it from
        # within a method instead of returning something
        if bot.is_yes(bot.db[message.author.id, "delete_response"]):
            asyncio.ensure_future(bot.wait_then_delete(rspmsg, message.author))

with open('oauth2.tok') as file:
    print("Starting...")
    client.run(file.read())
