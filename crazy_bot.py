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
prompts = []
replies = []
intent.message_content=True
client = Bot(intents=intent,command_prefix="!")

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
    prompts.append(msg.content)

    await ctx.send(f"Please enter the bots response.")
    msg = await client.wait_for("message", check=check)
    replies.append(msg.content)
    
@client.event
async def on_message(message):
    await client.process_commands(message) 
	# CHECKS IF THE MESSAGE THAT WAS SENT IS EQUAL TO "HELLO".
	# SENDS BACK A MESSAGE TO THE CHANNEL.
    if message.author.bot: #if message's author is a bot, then ignore it.
        return
    count=0
    for word in prompts:
        if message.content == word:
            await message.channel.send(replies[count])
            return
    count+=1

    if message.content.lower() in ["crazy", "crazy?"]:
        await message.channel.send("I was crazy once.")

    if message.content.lower() in ["i was crazy once", "i was crazy once."]:
        await message.channel.send("They locked me in a room.")

    if message.content.lower() in ["they locked me in a room", "they locked me in a room.","they put me in a room.","they put me in a room"]:
        await message.channel.send("A rubber room.")

    if message.content.lower() in ["a rubber room", "a rubber room."]:
        await message.channel.send("A rubber room with rats.")

    if message.content.lower() in ["a rubber room with rats","a rubber room with rats."]:
        await message.channel.send("Rats make me crazy.")

    if message.content.lower() in ["rats make me crazy","rats make me crazy.","and rats make me crazy","and rats make me crazy."]:
        await message.channel.send("Crazy?")

    elif not message.content and not message.attachments:
        print("message is empty")
client.run(TOKEN)
