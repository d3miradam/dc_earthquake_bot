import requests
import json
import discord
from discord.ext import tasks

previous_data = {}
latest_earthquake = {}

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)


async def send_earthquake_info(earthquake):
    global previous_data
    degerler = f"""
!!! DEPREM !!!
==============
Yer: {earthquake["yer"]}
Tarih: {earthquake["tarih"]}
Saat: {earthquake["saat"]}
Derinlik: {earthquake["derinlik_km"]} KM
Şiddet: {earthquake["ml"]}
==========================================
"""

    # Mesaj göndermek istediğiniz kanalın ID'sini belirtin.
    channel = client.get_channel(your_channel_id)

    # Kanala mesaj gönderme işlemi
    await channel.send(degerler)
    previous_data = latest_earthquake



#ISTANBUL ICIN

async def send_earthquake_info_ist(earthquake):
    global previous_data
    degerlerist = f"""
!!! DEPREM !!!
==============
Yer: {earthquake["yer"]}
Tarih: {earthquake["tarih"]}
Saat: {earthquake["saat"]}
Derinlik: {earthquake["derinlik_km"]} KM
Şiddet: {earthquake["ml"]}
==========================================
@everyone
"""

    # Mesaj göndermek istediğiniz kanalın ID'sini belirtin.
    channel = client.get_channel(your_channel_id)

    await channel.send(degerlerist)
    previous_data = latest_earthquake


deger = 0

@tasks.loop(seconds=60)
async def check_earthquakes():
    global latest_earthquake, previous_data, deger
    response = requests.get("http://hasanadiguzel.com.tr/api/sondepremler")
    data = json.loads(response.text)
    earthquakes = data["data"]
    latest_earthquake = earthquakes[0]

    if latest_earthquake != previous_data:
        if "ISTANBUL" in latest_earthquake["yer"]:
            send_earthquake_info_ist(latest_earthquake)
            deger = deger +1
        elif "MARMARA DENIZI" in latest_earthquake["yer"]:
            await send_earthquake_info_ist(latest_earthquake)
            deger = deger +1
        elif latest_earthquake["ml"] >= 4:
            await send_earthquake_info(latest_earthquake)
            deger = deger +1
        elif latest_earthquake["ml"] >= 5:
            await send_earthquake_info_ist(latest_earthquake)
            deger = deger + 1
        else:
            deger = deger +1
            pass
    elif deger == 60:
        quit()
    else:
        deger = deger +1
        pass


@client.event
async def on_ready():
    print('Bot is ready.')
    check_earthquakes.start()


TOKEN = 'Your_discord_bot_TOKEN'
client.run(TOKEN)