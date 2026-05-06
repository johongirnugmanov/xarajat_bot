import os
import pandas as pd
import re
from aiogram import Bot, Dispatcher, types, executor

# API_TOKEN ni Render sozlamalaridan oladi (xavfsizlik uchun)
API_TOKEN = os.getenv('API_TOKEN') 
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

FILE_NAME = "xarajatlar.csv"

def get_amount(text):
    clean_text = text.replace(" ", "").lower()
    res = re.findall(r'\d+', clean_text)
    if res:
        val = int(res[0])
        # "ming" yoki "m" so'zi bo'lsa 1000 ga ko'paytirish
        if val < 1000 and ('ming' in text.lower() or 'm' in text.lower()):
            val *= 1000
        return val
    return 0

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Xarajatni yozing. Masalan: 'Tushlik 35000' yoki 'Taxi 12 ming'")

@dp.message_handler(commands=['hisobot'])
async def report(message: types.Message):
    if os.path.exists(FILE_NAME):
        df = pd.read_csv(FILE_NAME)
        await message.answer(f"📊 Jami xarajat: {df['Summa'].sum():,} so'm".replace(",", " "))
    else:
        await message.answer("Hali ma'lumot yo'q.")

@dp.message_handler()
async def collect(message: types.Message):
    summa = get_amount(message.text)
    if summa > 0:
        if not os.path.exists(FILE_NAME):
            pd.DataFrame(columns=["Sana", "Xabar", "Summa"]).to_csv(FILE_NAME, index=False)
        
        df = pd.read_csv(FILE_NAME)
        # Yangi xarajatni qo'shish
        new_row = {"Sana": "2026-05-06", "Xabar": message.text, "Summa": summa}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(FILE_NAME, index=False)
        await message.reply(f"✅ Saqlandi: {summa:,} so'm".replace(",", " "))
    else:
        await message.reply("⚠️ Summani tushunmadim. Iltimos, raqam bilan yozing.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
  
