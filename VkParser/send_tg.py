import os
import re
import json
import time
import requests
from auth_data import headers
from groups import suppliers
from decode_sequence import encode_decode_sequence

API_URL: str = 'https://api.telegram.org/bot'
BOT_TOKEN: str = '6242446471:AAHAESMZObnxdDcbmnVl8Ti-dXfTvEtuAow'
SECS = 30

def test_request(url, retry, data, link):
    try:
        response = requests.post(url, data=data, headers=headers)
        print(f"\n[+] {link} {response.status_code}")
        response.raise_for_status()  # Raise an exception if status is not 200
    except requests.exceptions.HTTPError as err:
        if response.status_code == 429:
            print('Упал в исключение!!!')
            if retry:
                print(f"[INFO] retry={retry} => {link}")
                time.sleep(SECS)
                return test_request(url=url, retry=(retry-1), data=data, link=link)
            else:
                print(f"[ERROR] Max retries exceeded => {link}")
        else:
            print(f"[ERROR] {err}")
    return response

def send_telegram(text, photos, chat_id, link, retry):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMediaGroup'
    media = []
    media.append({'type': 'photo', 'media': photos[0], 'caption': text})
    for photo in photos[1:]:
        media.append({'type': 'photo', 'media': photo})
    data = {
        'chat_id': chat_id,
        'media': json.dumps(media)
    }
    response = test_request(url, retry, data, link)
    return response.json()

def post_vkWall(club, text, attachments, token):
    url = f'https://api.vk.com/method/wall.post?owner_id=-{club}&message={text}&attachments={attachments}&access_token={token}&v=5.131'
    req = requests.get(url)
    return req


def send_post(text_file, keywords):
    if not any(keyword.lower() in text_file.lower() for keyword in keywords):
        try:
            intro = "💌" + "Hey, ОБЗОР 😍\n\n"
            name = "✔" + "Наименование: " + text_file.split('\n')[0] + '\n'
            pattern = r'(\d+)\s*(рублей|руб\.?|р\.?|₽)?'
            match_p = re.search(pattern, text_file)
            old_price = match_p.groups()[0]
            # match_p = re.search(r'\d+₽', text_file)
            # if match_p:
            #     match_p = match_p.group().strip()
            #     match_p = match_p.split('₽')[0]
            # else:
            #     match_p = re.search(r'\n\d+', text_file).group().strip()
            price = "🏷" + "Цена: " + str(
                int(int(old_price) * 1.3)) + "₽\n"
            rating = "⭐" + "Рейтинг: " + re.search(r'\d+/\d\b', text_file).group() + '\n'
            link = "🔍" + "Ссылка: " + re.search(r"https?://\S+", text_file).group() + '\n'
            match = re.search(r'https://\S+', text_file)
            if match:
                text = "\n".join(
                    [line for line in text_file[match.end():].split("\n") if line.strip()])
                description = "✏" + "Описание: " + text
            else:
                print("Описание не подтягивается. Проверь регулярное выражение")
            full_text = intro + name + price + rating + link + description
            return full_text
        except:
            pass

def find_price(text):
    match = re.search(r"(стоимость|шт[учнок]|sale|распродаж[аеыи]|цена за штук|цен[аеы]?).*(\d+)", text.lower())
    if match:
        new_match = match.group(0)
        out = re.search(r"\d.*", new_match.lower())
        # print(F"HERE: {file['url']}, {price}")
        if '₽' in out.group(0):
            out = re.search(r"\d+\s*₽", new_match.lower()) # добавил
            price = out.group(0).split('₽')[0]
            # print(out.group(0).split('₽')[0])
            return price
        elif re.search(r"\d{2,}", out.group(0)):
            l = re.search(r"\d{2,}", out.group(0))
            price = l.group(0)
            return price
def get_tg_text(text, post_id, symbol_assignments):
    # if find_price(text):
        # price = find_price(text)
        # print("TYPE PRICE:", type(price))
        # print("Ссылка:", file['url'])
        # print("Цена: ", price)
        # new_price = int(int(price) * 1.3)
        # pattern = r"(стоимость|шт[учнок]|sale|распродаж[аеыи]|цен[аеы]?).*(\d+)"
        # if (re.sub(pattern=pattern, repl='', string=text.lower())):
    key = post_id.split('_')[0]
    key = key.split('-')[1] if '-' in key else key
    brand_name = suppliers[key]
    supplier = "Поставщик: " + brand_name + '\n\n'
    # text = re.sub(pattern=pattern, repl='', string=text.lower())
    # art = f"\nАртикул: {encode_decode_sequence(post_id, symbol_assignments)}"
    # price = f"\nЦена с комиссией: {new_price}₽"
    # full_text = supplier + text + art + price
    link = "\nСсылка: " + 'https://vk.com/wall' + f"{post_id}"
    full_text = supplier + text + link
    return full_text

def get_vk_text(text, post_id, symbol_assignments):
    try:
        if find_price(text):
            price = find_price(text)
            # print("TYPE PRICE:", type(price))
            # print("Ссылка:", file['url'])
            # print("Цена: ", price)
            new_price = int(int(price) * 1.3)
        pattern = r".*(стоимость|шт[учнок]|sale|распродаж[аеыи]|цен[аеы]?).*(\d+).*"
        if (re.sub(pattern=pattern, repl='', string=text.lower())):
            new_text = re.sub(pattern=pattern, repl=f'📍{new_price}₽📍', string=text.lower())
        key = post_id.split('_')[0]
        key = key.split('-')[1] if '-' in key else key
        brand_name = suppliers[key]
        supplier = "Поставщик: " + brand_name + '\n\n'
        # text = re.sub(pattern=pattern, repl='', string=text.lower())
        art = f"\n\nАртикул: {encode_decode_sequence(post_id, symbol_assignments)}"
        price = f"\nЦена: {new_price}₽"
    # full_text = supplier + text + art + price
    # link = "\nСсылка: " + 'https://vk.com/wall' + f"{post_id}"
        full_text = new_text + art
        return full_text
    except:
        return ""