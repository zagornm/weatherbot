import asyncio
import requests
from bs4 import BeautifulSoup
from aiogram import Bot
from datetime import datetime

# Конфигурация
BOT_TOKEN = "8497876910:AAGLopwWA3mnpYIsGk3NH4IJS754ulH84v0"
CHANNEL_ID = "-1002955948611"

last_data = None
bot = Bot(token=BOT_TOKEN)

# Словарь для перевода месяцев на русский
RUSSIAN_MONTHS = {
    1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля',
    5: 'мая', 6: 'июня', 7: 'июля', 8: 'августа',
    9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'
}


def parse_weather():
    """Парсит данные о погоде"""
    url = "http://www.meteo.nw.ru/"
    response = requests.get(url, timeout=25)
    response.encoding = 'windows-1251'

    soup = BeautifulSoup(response.text, 'html.parser')

    data = {
        'temp': soup.find('div', id='wtemp').text.strip(),
        'weather': soup.find('div', id='wpic').img['title'],
        'wind_dir': soup.find('div', class_='wwindd2').text.strip(),
        'wind_speed': soup.find_all('div', class_='wttdr')[1].text.strip(),
        'pressure': soup.find_all('div', class_='wttdr')[2].text.strip(),
        'humidity': soup.find_all('div', class_='wttdr')[3].text.strip()
    }

    return data


async def check_and_send():
    """Проверяет и отправляет погоду"""
    global last_data

    current_data = parse_weather()

    # Проверяем изменения
    if str(current_data) != str(last_data):
        # Получаем текущую дату и время
        now = datetime.now()
        day = now.day
        month = RUSSIAN_MONTHS[now.month]
        year = now.year
        time = now.strftime("%H:%M")

        # Форматируем дату на русском
        current_date = f"{day} {month} {year}"

        # Создаем сообщение с временем
        message = (
            f"🌤️ *Погода в Петербурге {current_date}*\n"
            f"🕐 *Время обновления:* {time}\n\n"
            f"🌡️ *Температура:* {current_data['temp']}\n"
            f"☁️ *Состояние:* {current_data['weather']}\n"
            f"💨 *Ветер:* {current_data['wind_dir']}, {current_data['wind_speed']}\n"
            f"📊 *Давление:* {current_data['pressure']}\n"
            f"💧 *Влажность:* {current_data['humidity']}\n\n"
            f"#погода #СПб"
        )

        # Отправляем в канал
        await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='Markdown')
        print(f"Отправлено обновление")

        last_data = current_data
    else:
        print("Данные не изменились")


async def main():
    """Основной цикл"""
    print("Бот запущен...")
    while True:
        await check_and_send()
        await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
