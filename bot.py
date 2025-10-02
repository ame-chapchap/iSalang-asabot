import discord
from discord.ext import tasks
import os
from datetime import datetime, timezone, timedelta
from flask import Flask
from threading import Thread

# Flask設定（Renderで動かし続けるため）
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 日本時間の設定
JST = timezone(timedelta(hours=9))

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

client = discord.Client(intents=intents)

# ボイスチャンネルIDを設定（後で変更してください）
VOICE_CHANNEL_ID = 1372559165108785244  # ←あなたのボイスチャンネルIDに変更

@tasks.loop(minutes=1)
async def check_time():
    now = datetime.now(JST)
    hour = now.hour
    
    voice_client = discord.utils.get(client.voice_clients)
    
    # 6時台で未接続なら接続
    if hour == 6 and voice_client is None:
        channel = client.get_channel(VOICE_CHANNEL_ID)
        if channel:
            try:
                await channel.connect()
                print(f"✅ ボイスチャンネルに接続しました: {now}")
            except Exception as e:
                print(f"❌ 接続エラー: {e}")
    
    # 7時以降で接続中なら切断
    elif hour >= 7 and voice_client is not None:
        try:
            await voice_client.disconnect()
            print(f"✅ ボイスチャンネルから切断しました: {now}")
        except Exception as e:
            print(f"❌ 切断エラー: {e}")

@client.event
async def on_ready():
    print(f'🤖 {client.user} としてログインしました')
    print(f'⏰ 時刻チェックを開始します')
    check_time.start()

if __name__ == "__main__":
    keep_alive()
    client.run(os.getenv('DISCORD_TOKEN'))
