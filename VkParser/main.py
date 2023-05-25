import re
from time import time
from parse_posts import collect_postData, get_wall_posts, divide_groups
from auth_data import symbol_assignments
from decode_sequence import encode_decode_sequence
from groups import groups_name, chats_id, smotrinashmotki, tg_groups, man_vip_group, vk_groups
from send_tg import find_price, test_request
import requests
import time
from auth_data import token
from datetime import date, timedelta

COUNT = 5
REVIEW = False
Vk = True
API_URL: str = 'https://api.telegram.org/bot'
BOT_TOKEN: str = '6242446471:AAHAESMZObnxdDcbmnVl8Ti-dXfTvEtuAow'
DATE = date.today() - timedelta(days=15)
# chat_id: str = "@publi7773"
#

if REVIEW:
    groups = smotrinashmotki
elif Vk:
    groups = vk_groups
else:
    groups = tg_groups
get_wall_posts(groups_name=groups, vk=Vk, count=COUNT)
collect_postData(groups_name=groups_name, needed_date=DATE, vk=Vk, review=REVIEW)

# url = "https://vk.com/wall" + encode_decode_sequence('!>.=$**.:^?<==*<', symbol_assignments, encode=False)
# print(url)