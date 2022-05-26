import random
import time

from bs4 import BeautifulSoup
import asyncio
from aiogram import executor, Dispatcher, Bot
from urllib.request import urlopen


# список для сравнение с id старого поста
old_post = "0"

def teleForLoad():
    # делаем глобальным чтобы он был доступен внутри функции
    global old_post
    # ресурс на который мы заходим
    html = urlopen("https://www.avito.ru/groznyy/telefony?cd=1&s=104")
    # скармливаем bs4
    bs0bj = BeautifulSoup(html, "lxml")
    # вычисляем id первого поста
    id_product = bs0bj.find('div', class_="iva-item-root-_lk9K photo-slider-slider-S15A_ iva-item-list-rfgcH iva-item-redesign-rop6P iva-item-responsive-_lbhG items-item-My3ih items-listItem-Gd1jN js-catalog-item-enum")
    new_post = id_product["id"]
    # print(new_post)
    # смотрим есть ли новый товар
    if new_post != old_post:
        # если есть, определяем его как старый, для слудущей итерации
        old_post = new_post

        time_vrem = bs0bj.find("div", {"data-marker": "item-date"}).get_text()

        # цена
        price = bs0bj.find("span", {"class": "price-text-_YGDY text-text-LurtD text-size-s-BxGpL"}).get_text()
        # название продукта
        name_product = bs0bj.find('h3', class_='title-root-zZCwT iva-item-title-py3i_ title-listRedesign-_rejR title-root_maxHeight-X6PsH text-text-LurtD text-size-s-BxGpL text-bold-SinUO').text

        # общая информация
        infor = bs0bj.find("div", {"class": "iva-item-text-Ge6dR iva-item-description-FDgK4 text-text-LurtD text-size-s-BxGpL"}).get_text()
        # имя владельца товара
        name_user = bs0bj.find("div", {"class": "style-title-_wK5H text-text-LurtD text-size-s-BxGpL"}).get_text()
        # ссыка на товар
        more = bs0bj.find("div", class_="iva-item-titleStep-pdebR").find("a").get("href")
        more = "https://www.avito.ru" + more

        # исправляем ошибки в кодировки
        rep = ["\u20bd", "\xb3", "\xb2", "\xd8", "\u2011", "\xa0"]
        for item in rep:
            if item in price:
                price = price.replace(item, "")

        return time_vrem, name_product, price, infor.replace('\n', ''), name_user, more

    elif new_post == old_post:
        return "Нового товара ещё нет!"


TOKEN = "your token telegram bot"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# тест на таймер
async def scheduled(wait_for):
    while True:
        # отлавливаем обрыв соединения
        try:
            await asyncio.sleep(wait_for)
            print("Проверка на наличие товара")
            # если нет товара
            try:
                time_vrem, name_product, price, infor, name_user, more = teleForLoad()

                await bot.send_message(5295520075, f"ВРЕМЯ ДОБАВЛЕНИЕ ТОВАРА: {time_vrem}\n"
                                                   f"НАЗВАНИЕ ТОВАРА: {name_product}\n"
                                                   f"ЦЕНА {price}\n"
                                                   f"ОПИСАНИЕ: {infor}\n"
                                                   f"ВЛАДЕЛЕЦ: {name_user}\n"
                                                   f"ССЫЛКА: {more}", disable_notification=True)
            except:
                not_new_products = teleForLoad()
                print(not_new_products)
        except:
            print("Соединение востановлено")
            print("Проверка на наличие товара")
            # если нет товара
            try:
                time_vrem, name_product, price, infor, name_user, more = teleForLoad()

                await bot.send_message(5295520075, f"ВРЕМЯ ДОБАВЛЕНИЕ ТОВАРА: {time_vrem}\n"
                                                   f"НАЗВАНИЕ ТОВАРА: {name_product}\n"
                                                   f"ЦЕНА {price}\n"
                                                   f"ОПИСАНИЕ: {infor}\n"
                                                   f"ВЛАДЕЛЕЦ: {name_user}\n"
                                                   f"ССЫЛКА: {more}", disable_notification=True)
            except:
                not_new_products = teleForLoad()
                print(not_new_products)






if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(10))
    executor.start_polling(dp, skip_updates=True)