from pyaspeller import YandexSpeller
speller = YandexSpeller()

text = """
Поставщик: ⚜️ Стильная одежда Садовод ⚜️

🌹новый шорт мужские 
🌹ткано хлопок 
🌹тянутся хорошо 
🌹 длиной до колен
🌹размер : 32-33-34-35-36-38-40-42
                         50/52/54/56/58/60
🌹р
🌹 р
https://vk.com/jeans_fe  
whatsapp:89998296111
Артикул: !@==+**@+%?%=&:
Цена с комиссией: 1560₽
"""

fixed = speller.spelled("""
Поставщик: ⚜️ Дима Лыу ⚜️

✅новый получу жилет мужской 
✅качеств хороший
✅размер:48-50-52-54-56
✅ внутри холофайбер
✅ руб 
✅упаковки напиши  ватсап :📲89685271186
✅садовод линия:22-(33/35)
💥💥 https://vk.com/club198010005
💎💎 https://vk.com/club197807427
телеграмм канал: https://t.me/sadavod_22_33
👇👇все цвет реально фото 👇
Артикул: !@:+=*+%#+?@@%+&
Цена с комиссией: 1105₽
""")
print(fixed)

# from deeppavlov import build_model, configs
#
# model = build_model(configs.spelling_correction.levenshtein_corrector_ru, download=True)
#
# text = 'Аналищик данных занимается машинами обучением'
# corrected_text = model([text])[0]
# print(corrected_text)