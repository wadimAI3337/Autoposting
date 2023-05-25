import re

texts = [
    '''Two NK UNISEX
    Material : Three-piece without fleece | Turkish
    Sizes: 48-54 OverSize
    Price : 1600
    Wholesale: 5pcs-1500₽
    The best for you!''',

    '''⚜  ⚜ ❤ 🌺 𝙉𝙀𝙒 𝘾𝙊𝙇𝙇𝙀𝘾𝙏𝙄𝙊𝙉 🌺 ❤ ⚜  ⚜

    ~~~~~~ 2A-75 Housing A ~~~~~~
    ▫ Jackets Classic Spring-Summer
    __________________________________
    ▫ Product Length: 72cm
    ▫ Production: FACTORY CHINA
    __________________________________
    ▫ Fabric: 75%Cotton 25%Spandex
    __________________________________
    ▫ Sizes: 42-48 Single
    __________________________________
    ▫ Price: 450₽ ‼ ‼ ‼
    __________________________________
    ▫ Product For The Marketplace ‼ ‼ ‼
    __________________________________
    📞 Number for ordering and receiving information: +7 (926 818 70 47)
    https://vk.com/kolyaxas'''
]

# remove lines containing "Wholesale", links, and phone numbers starting with +7 or 8
for i, text in enumerate(texts):
    texts[i] = re.sub(r".*Wholesale.*\n", "", text)
    texts[i] = re.sub(r"http\S+", "", texts[i])
    texts[i] = re.sub(r"\+?[78]\s?\(?\d{3}\)?\s?\d{3}\s?\-?\d{2}\s?\-?\d{2}", "", texts[i])

    # multiply price by 1.3
    price_match = re.search(r"Price : (\d+)", texts[i])
    if price_match:
        price = int(price_match.group(1))
        new_price = price * 1.3
        texts[i] = re.sub(r"Price : \d+", f"Price : {new_price:.2f}", texts[i])

print(texts[1])


# def find_material(dpath):
#     file_length = 0
#     cnt = 0
#     list_dir = os.listdir(dpath)
#     for item in list_dir:
#         name, ext = os.path.splitext(item)
#         exist_file_path = dpath + name + "_data" + ext
#         item = dpath + item
#         with open(item, encoding="utf-8") as f:
#             files = json.load(f)
#             file_length = file_length + len(files)
#             for file in files:
#                 text = file['text']
#                 pattern_material = r'материал(.+)'
#                 pattern_tkan = r'ткань(.+)'
#                 pattern_quality = r'качество(.+)'
#                 match_mat = re.search(pattern_material, text.lower(), re.IGNORECASE)
#                 match_tk = re.search(pattern_tkan, text.lower(), re.IGNORECASE)
#                 match_qual = re.search(pattern_quality, text.lower(), re.IGNORECASE)
#                 if match_mat:
#                     cnt = cnt + 1
#                     # print("Материал:", match_mat.group(1).strip(":").strip())
#                     material = match_mat.group(1).strip(":").strip()
#                     print("Метериал:", material, '-->', file['url'])
#                 elif match_tk:
#                     cnt = cnt + 1
#                     # print("Материал:", match_tk.group(1).strip(":").strip())
#                     material = match_tk.group(1).strip(":").strip()
#                     print("Метериал:", material, '-->', file['url'])
#                 elif match_qual:
#                     material = match_qual.group(1).strip(":").strip()
#                     print("Качество:", material, '-->', file['url'])
#                     cnt = cnt + 1
#                 else:
#                     material = "Отличное качество!"
#                     print(material, '-->', file['url'])
#     print("CNT", cnt)
#     print("file_length", file_length)



def find_price(text):
    match = re.search(r"(стоимость|шт[учнок]|sale|распродаж[аеыи]|цен[аеы]?).*(\d+)", text.lower())
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
    # else:
    #     print("Я НЕ СМОГ НАЙТИ В ТЕКСТЕ СЛОВО 'ЦЕНА'!!! -->", file['url'])