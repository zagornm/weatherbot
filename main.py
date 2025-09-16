import asyncio
import requests
from bs4 import BeautifulSoup
from aiogram import Bot
from datetime import datetime

BOT_TOKEN = "8497876910:AAGLopwWA3mnpYIsGk3NH4IJS754ulH84v0"
CHANNEL_ID = "-1002955948611"

last_data = None
bot = Bot(token=BOT_TOKEN)

RUSSIAN_MONTHS = {1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля', 5: 'мая', 6: 'июня', 
                  7: 'июля', 8: 'августа', 9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'}

async def main():
    """Максимально простой и надежный цикл"""
    global last_data
    print("Бот запущен...")
    
    while True:
        try:
            # Парсим погоду
            response = requests.get("http://www.meteo.nw.ru/", timeout=30)
            response.encoding = 'windows-1251'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            current_data = {
                'temp': soup.find('div', id='wtemp').text.strip(),
                'weather': soup.find('div', id='wpic').img['title'],
                'wind_dir': soup.find('div', class_='wwindd2').text.strip(),
                'wind_speed': soup.find_all('div', class_='wttdr')[1].text.strip(),
                'pressure': soup.find_all('div', class_='wttdr')[2].text.strip(),
                'humidity': soup.find_all('div', class_='wttdr')[3].text.strip()
            }
            
            # Отправляем если данные изменились
            if str(current_data) != str(last_data):
                now = datetime.now()
                message = (
                    f"🌤️ *Погода в Петербурге {now.day} {RUSSIAN_MONTHS[now.month]} {now.year}*\n"
                    f"🕐 *Время:* {now.strftime('%H:%M')}\n\n"
                    f"🌡️ *Температура:* {current_data['temp']}\n"
                    f"☁️ *Состояние:* {current_data['weather']}\n"
                    f"💨 *Ветер:* {current_data['wind_dir']}, {current_data['wind_speed']}\n"
                    f"📊 *Давление:* {current_data['pressure']}\n"
                    f"💧 *Влажность:* {current_data['humidity']}\n\n#погода #СПб"
                )
                await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='Markdown')
                last_data = current_data
                print("Отправлено обновление")
            else:
                print("Данные не изменились")
                
        except Exception as e:
            # ЛЮБАЯ ошибка будет поймана здесь и контейнер НЕ перезагрузится
            print(f"Произошла ошибка: {e}")
        
        # Ждем 60 секунд в любом случае
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
