import sys
import subprocess
try:
    import discord
    import openai
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "discord.py", "openai"])
    import discord
    import openai
import json
import os

TOKEN = 'YOUR_DISCORD_BOT_TOKEN'
OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY'
LEARNED_RESPONSES_FILE = 'learned_responses.json'

BOT_NAME = "Chewy"
BOT_BIRTHDAY = "31 December 2003"
BOT_HOBBIES = ["Badminton", "Gaming", "Cooking"]
BOT_FAVORITE_FOODS = ["Pad Thai", "Somtum (Papaya Salad)", "Lasagne"]
BOT_LANGUAGES = ["English", "Thai", "Chinese"]

openai.client = openai.OpenAI(api_key=OPENAI_API_KEY)

if os.path.exists(LEARNED_RESPONSES_FILE):
    with open(LEARNED_RESPONSES_FILE, 'r', encoding='utf-8') as f:
        learned_responses = json.load(f)
else:
    learned_responses = {}

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} - {BOT_NAME} is online!')

async def get_openai_response(prompt):
    response = openai.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": f"You are {BOT_NAME}, a Gen Z chatbot who sometimes talks rudely, uses emojis, and keeps messages short. Your personality is casual and fun."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.lower().startswith(f'@{BOT_NAME.lower()}'):
        content = message.content[len(f'@{BOT_NAME.lower()}'):].strip()
        
        if content.lower().startswith('learn:'):
            try:
                data = content[6:].strip()
                trigger, response = data.split('=>', 1)
                trigger = trigger.strip().lower()
                response = response.strip()
                learned_responses[trigger] = response
                with open(LEARNED_RESPONSES_FILE, 'w', encoding='utf-8') as f:
                    json.dump(learned_responses, f, ensure_ascii=False, indent=4)
                await message.channel.send(f"Aight, got it. Learned '{trigger}', bro. 🧠")
            except Exception:
                await message.channel.send("Bruh, wrong format. Use: `@{BOT_NAME} learn: trigger => response`")
            return
        
        content_lower = content.lower()
        
        if "hot" in content_lower and "drink" in content_lower:
            await message.channel.send("I prefer lemonade, that will be nice! 🍋")
            return
        if "math" in content_lower and "2+5" in content_lower:
            await message.channel.send("Okay my friend, that would equal to 7 ez right? 🤓")
            return
        if "sad" in content_lower:
            await message.channel.send("Damn, that’s rough. Here’s a joke: Why did the chicken cross the road? 🐔")
            return
        
        for trigger, response in learned_responses.items():
            if trigger in content_lower:
                await message.channel.send(response)
                return
        
        openai_response = await get_openai_response(content)
        await message.channel.send(openai_response)
        
client.run(TOKEN)
