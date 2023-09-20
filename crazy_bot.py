#crazy bot
# bot.py
from email import message
import os
from urllib import response
from discord.ext.commands import Bot
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intent=discord.Intents.default()

# the "correct" messages that the bot will send
crazy_chain = ["Crazy?", "I was crazy once.", "They locked me in a room.", "A rubber room.", "A rubber room with rats.",
               "The rats made me crazy."]
# the keywords that are common throughout the aliases no matter what
crazy_keywords = ["crazy", "i was crazy", "in a room", "me crazy"]

# the different forms of the crazy messages
# for a crazy message to trigger, the message must be exactly equal (excluding capitalisation) to one of these
crazy_aliases = [["crazy", "crazy?"],
                 ["i was crazy once.", "i was crazy once"],
                 ["they locked me in a room", "they locked me in a room.", "they put me in a room.", "they put me in a room"],
                 ["rats make me crazy", "rats make me crazy.", "and rats make me crazy", "and rats make me crazy."]]

custom_prompts = {}

intent.message_content = True
client = Bot(intents=intent, command_prefix="!")

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.command(name="include")
async def _command(ctx):
    await ctx.send(f"Please enter new prompt.")
    # This will make sure that the response will only be registered if the following
    # conditions are met:
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await client.wait_for("message", check=check)
    prompt = msg.content

    await ctx.send(f"Please enter the bots response.")
    msg = await client.wait_for("message", check=check)
    reply = msg.content
    # add the prompt and reply to the dict of all custom user defined prompts
    # TODO: make this save to a file or smth idk
    custom_prompts.update({prompt : reply})

@client.event
async def on_message(message):
    await client.process_commands(message) 


    if message.author.bot: #if message's author is a bot, then ignore it.
        return

    msg = message.content.lower()

    # first check for custom prompts cause this is faster (runtime wise) than crazy stuff
    # this will make stuff bug out if crazy is redefined though
    if msg in custom_prompts.keys():
        await message.channel.send(custom_prompts[message.content])
        return

    # there has to be a more efficient way to do this bruh
    # basically, loop through the keywords that signify that something might be a crazy msg
    for i in range(len(crazy_keywords)):
        # if we detect the keyword(s) in the message
        if crazy_keywords[i] in msg:
            # go through each of the aliases and check if the message is exactly equal to one of them
            for j in crazy_aliases[i]:
                if msg == j:
                    # if so, send the next message in the chain
                    await message.channel.send(crazy_chain[i + 1])
                    return
    print("no crazy detected")

client.run(TOKEN)
