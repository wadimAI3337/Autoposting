import os
import json
import requests
import numpy as np
import time
from auth_data import token, headers, symbol_assignments
from send_tg import send_telegram, send_post, find_price, get_tg_text, post_vkWall, get_vk_text
from tqdm import tqdm
from groups import suppliers, chats_id, review_group
from datetime import datetime


SECS = 60
RETRY = 5


def divide_groups(groups: list[str]):
    groups_name = np.array([])
    for group in groups:
        name = (group.split('club')[-1])
        groups_name = np.append(groups_name, name)

    return groups_name


def get_wall_posts(groups_name, vk, count):
    posts = []
    if vk:
        name = "vk_groups"
    else:
        name = "tg_groups"

    if os.path.exists(f"{name}"):
        print(f"{name} уже создана директория.")
    else:
        os.mkdir(name)

    # groups_name = divide_groups(groups)

    for group_name in groups_name:
        if group_name.isdigit():
            url = f'https://api.vk.com/method/wall.get?owner_id=-{group_name}&count={count}&access_token={token}&v=5.131'
        else:
            url = f'https://api.vk.com/method/wall.get?domain={group_name}&count={count}&access_token={token}&v=5.131'
        req = requests.get(url)
        src = req.json()
        try:
            post = src['response']['items']
            posts.append(post)
            with open(f"{name}/{group_name}.json", "w", encoding="utf-8") as file:
                json.dump(src, file, indent=4, ensure_ascii=False)
            time.sleep(1)
        except:
            pass

def download_photo(url: str, post_id: int, number: int, group_name='Data'):
    if not os.path.exists(f"{group_name}/photos"):
        os.mkdir(f"{group_name}/photos")

    res = requests.get(url, headers=headers, stream=True)

    with open(f"{group_name}/photos/{post_id}_{number}.jpg", "wb") as img_file:
        img_file.write(res.content)


def collect_postData(groups_name, needed_date, vk, review, download=False):
    data = []
    if vk:
        name_gr = "vk_data"
        club = 216316323
        review = False
        gpath = "C:/Users/wadim.DESKTOP-ONBR3LG/PycharmProjects/Autoposting/VkParser/vk_groups/"
        dpath = "C:/Users/wadim.DESKTOP-ONBR3LG/PycharmProjects/Autoposting/VkParser/vk_data/"
    else:
        name_gr = "tg_data"
        gpath = "C:/Users/wadim.DESKTOP-ONBR3LG/PycharmProjects/Autoposting/VkParser/tg_groups/"
        dpath = "C:/Users/wadim.DESKTOP-ONBR3LG/PycharmProjects/Autoposting/VkParser/tg_data/"
    list_dir = os.listdir(gpath)
    if review:
        groups = ['smotrinashmotki']
        list_dir = [list_dir[list_dir.index('smotrinashmotki.json')]]
        groups_name = review_group
    else:
        if 'smotrinashmotki.json' in list_dir:
            list_dir.remove('smotrinashmotki.json')
        else:
            list_dir = list_dir
    keywords = ['Посредник', 'Брала в группе по сборам Китая', 'проверенные сборы', 'Приглашаем', 'Собирали в группе по сбору', 'сборам']
    print(name_gr)
    for item in list_dir:
        name, ext = os.path.splitext(item)
        exist_file_path = dpath + name + "_data" + ext
        item = gpath + item
        for group_name, groups in groups_name.items():
            if review:
                chat_id = '-1001938933203'
            elif name in groups:
                chat_id = chats_id[group_name]
            else:
                continue
            if os.path.isfile(f"{name_gr}/{name}_data.json"):
                print(f"Файл {name}_data.json уже существует")
                with open(exist_file_path, encoding="utf-8") as f:
                    exist_file = json.load(f)
                    old_length = len(exist_file)
                with open(item, encoding="utf-8") as f:
                    file = json.load(f)
                    posts = file['response']['items']
                    for i in tqdm(range(len(posts) - 1, -1, -1)):
                        images = []
                        date_stamp = int(posts[i]['date'])
                        date = datetime.utcfromtimestamp(date_stamp).date()
                        if date >= needed_date:
                            post_id = str(posts[i]['from_id']) + '_' + str(posts[i]['id'])
                            if post_id > exist_file[-1]['id']:
                                post_url = "https://vk.com/wall" + post_id
                                if review:
                                    full_text = send_post(posts[i]['text'], keywords)
                                elif vk:
                                    full_text = get_vk_text(posts[i]['text'], post_id, symbol_assignments)
                                else:
                                    # key = post_id.split('_')[0].split('-')[1]
                                    # brand_name = suppliers[key]
                                    full_text = get_tg_text(posts[i]['text'], post_id, symbol_assignments)
                                    # full_text = "Поставщик: " + brand_name + '\n\n' + posts[i]['text']
                                    # full_text = full_text + f"\nАртикул: {encode_decode_sequence(post_id, symbol_assignments)}"
                                if 'is_pinned' not in posts[i]:
                                    for i, post in enumerate(posts[i]['attachments']):
                                        if post['type'] == 'photo':
                                            if vk:
                                                image = 'photo' + str(post['photo']['owner_id']) + '_' + str(post['photo']['id'])
                                            else:
                                                image = (post['photo']['sizes'][-1]['url'])
                                            images.append(image)
                                            if download:
                                                download_photo(url=image, post_id=post_id, number=i)
                                if images:
                                    dict_to_added = \
                                        {
                                            'url': post_url,
                                            'id': post_id,
                                            'text': full_text,
                                            'images': images,
                                            'type': 'photo'
                                        }
                                    time.sleep(SECS)
                                    if vk:
                                        attachments = ','.join(images)
                                        post_vkWall(club, full_text, attachments, token)
                                    else:
                                        link = "https://vk.com/wall" + post_id
                                        send_telegram(full_text, images, chat_id, link, RETRY)
                                        # exist_file.insert(-1, dict_to_added)
                                    exist_file.append(dict_to_added)
                                if old_length < len(exist_file):
                                    with open(exist_file_path, "w", encoding="utf-8") as file:
                                        json.dump(exist_file, file, indent=4, ensure_ascii=False)
                                        print(f"Новый пост только что был добавлен в файл {name}!")
                                        print(f"---------------\n")
                                else:
                                    print(f"Посты актуальные в файле {name}. Добавлять нечего!")
            else:
                print(f"Файл {name_gr}/{name}_data.json НЕ существует")
                with open(item, encoding="utf-8") as f:
                    file = json.load(f)
                    posts = file['response']['items']
                    for i in tqdm(range(len(posts) - 1, -1, -1)):
                        images = []
                        date_stamp = int(posts[i]['date'])
                        date = datetime.utcfromtimestamp(date_stamp).date()
                        if date >= needed_date:
                            post_id = str(posts[i]['from_id']) + '_' + str(posts[i]['id'])
                            post_url = "https://vk.com/wall" + post_id
                            if 'is_pinned' not in posts[i]:
                                if review:
                                    full_text = send_post(posts[i]['text'], keywords)
                                elif vk:
                                    full_text = get_vk_text(posts[i]['text'], post_id, symbol_assignments)
                                else:
                                    # key = post_id.split('_')[0]
                                    # key = key.split('-')[1] if '-' in key else key
                                    # brand_name = suppliers[key]
                                    # full_text = "Поставщик: " + brand_name + '\n\n' + posts[i]['text']
                                    # full_text = full_text + f"\nАртикул: {encode_decode_sequence(post_id, symbol_assignments)}"
                                    full_text = get_tg_text(posts[i]['text'], post_id, symbol_assignments)
                                for i, post in enumerate(posts[i]['attachments']):
                                    if post['type'] == 'photo':
                                        if vk:
                                            image = 'photo' + str(post['photo']['owner_id']) + '_' + str(post['photo']['id'])
                                        else:
                                            image = (post['photo']['sizes'][-1]['url'])
                                        images.append(image)
                                        if download:
                                            download_photo(url=image, post_id=post_id, number=i)
                            if images:
                                dict_to_added = \
                                    {
                                        'url': post_url,
                                        'id': post_id,
                                        'text': full_text,
                                        'images': images,
                                        'type': 'photo'
                                    }
                                if vk:
                                    attachments = ','.join(images)
                                    response = post_vkWall(club, full_text, attachments, token)
                                    print(f"\n[+] {response.status_code}")
                                else:
                                    link = "https://vk.com/wall" + post_id
                                    send_telegram(full_text, images, chat_id, link, RETRY)
                                data.append(dict_to_added)
                                with open(f"{name_gr}/{name}_data.json", "w", encoding="utf-8") as file:
                                    json.dump(data, file, indent=4, ensure_ascii=False)
                                    print(f"---------------")
                                print("Заснул на", SECS)
                                time.sleep(SECS)
                print(f"Все посты были добавлены в файл {name}!")
            data = []
            print("Засыпаю...")
            time.sleep(1)
