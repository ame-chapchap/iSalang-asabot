from keep_alive import keep_alive

import discord
from discord.ext import tasks
import os
from datetime import datetime, timezone, timedelta

# 日本時間の設定
JST = timezone(timedelta(hours=9))

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

client = discord.Client(intents=intents)

# ボイスチャンネルIDを設定（後で変更）
VOICE_CHANNEL_ID = 1234567890  # ←あなたのボイスチャンネルIDに変更

@tasks.loop(minutes=1)
async def check_time():
    now = datetime.now(JST)
    hour = now.hour
    
    voice_client = discord.utils.get(client.voice_clients)
    
    # 6時台で未接続なら接続
    if hour == 6 and voice_client is None:
        channel = client.get_channel(VOICE_CHANNEL_ID)
        if channel:
            await channel.connect()
            print(f"ボイスチャンネルに接続しました: {now}")
    
    # 7時以降で接続中なら切断
    elif hour >= 7 and voice_client is not None:
        await voice_client.disconnect()
        print(f"ボイスチャンネルから切断しました: {now}")

@client.event
async def on_ready():
    print(f'{client.user} としてログインしました')
    check_time.start()

# TOKENは環境変数から取得
client.run(os.getenv('DISCORD_TOKEN'))

if __name__ == "__main__":
    keep_alive()
    client.run(os.getenv('DISCORD_TOKEN'))
