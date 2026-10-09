import discord
from discord import app_commands
from discord.ext import commands
import asyncio
from flask import Flask
from threading import Thread

# سيرفر ويب داخلي لمنصة Render ليبقى البوت حياً
app = Flask('')

@app.route('/')
def home():
    return "Bot is online!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# إعدادات البوت الأساسية
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ⚠️ اكتب الكلمات التي تريد حذفها هنا داخل القوسين وعلامات التنصيص
BANNED_WORDS = ["كلمة1", "كلمة2", "رابط_ممنوع"]

@bot.event
async def on_ready():
    print(f"تم تشغيل البوت باسم: {bot.user.name}")
    try:
        await bot.tree.sync()
        print("تمت مزامنة الأوامر بنجاح.")
    except Exception as e:
        print(f"خطأ في المزامنة: {e}")

@bot.tree.command(name="clean_all", description="حذف الرسائل القديمة المحظورة من السيرفر بالكامل")
@app_commands.checks.has_permissions(manage_messages=True)
async def clean_all(interaction: discord.Interaction):
    await interaction.response.send_message("⏳ جاري فحص وتنظيف السيرفر من الرسائل القديمة...", ephemeral=True)
    guild = interaction.guild
    deleted_count = 0

    for channel in guild.text_channels:
        permissions = channel.permissions_for(guild.me)
        if not (permissions.read_messages and permissions.manage_messages and permissions.read_message_history):
            continue
        try:
            async for message in channel.history(limit=None):
                if message.author == bot.user:
                    continue
                if any(word in message.content.lower() for word in BANNED_WORDS):
                    try:
                        await message.delete()
                        deleted_count += 1
                        await asyncio.sleep(0.2)
                    except:
                        continue
        except:
            continue

    await interaction.followup.send(f"✅ اكتمل التنظيف! تم حذف **{deleted_count}** رسالة قديمة.")

keep_alive()
# ⚠️ ضع توكن بوتك هنا بين علامات التنصيص
bot.run("MTU1ODE4OTI0NTI2MzI1MzUzNA.GxkHbv.P0voQUfMNBCcB7BwoVJf_mF3ozF6RQjsB30TLs")
