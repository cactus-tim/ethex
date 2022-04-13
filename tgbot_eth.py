import telebot
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import re
import random



# bot creation
token = '5154039206:AAFI3OuN4KzD6RA1nPkhXYKNofE9MYMVgtE'
bot = telebot.TeleBot(token)


# web driver creation
options = Options()
options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'
)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


# links
links = [
    'https://p2p.binance.com/ru/trade/sell/USDT?fiat=RUB&payment=Tinkoff',
    'https://www.binance.com/ru/trade/BTC_USDT',
    'https://www.binance.com/ru/trade/ETH_USDT'
]


#hours
hours = [
    10, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22
         ]
sleep = [
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 23
          ]
reserv = []


# global variables
btc = float(0)
rub_btc = float(0)
eth = float(0)
rub_eth = float(0)



def get_data():
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        driver.get(url=links[0])
        time.sleep(random.randint(150, 400))
        item = driver.find_elements(By.CLASS_NAME, 'css-1m1f8hn')
        curancy_usdt = (float(item[0].text) + float(item[1].text) + float(item[2].text))/3 #Понаблюдай за тем како йкурс он выводит
        print(curancy_usdt)

        driver.get(url=links[1])
        time.sleep(random.randint(120, 300))
        item1 = driver.find_element(By.CLASS_NAME, 'showPrice').text
        curancy_btc = float(item1.replace(',', ''))
        print(curancy_btc)

        driver.get(url=links[2])
        time.sleep(random.randint(120, 300))
        item2 = driver.find_element(By.CLASS_NAME, 'showPrice').text
        curancy_eth = float(item2.replace(',', ''))
        print(curancy_eth)

        curances = []
        curances.append(curancy_usdt)
        curances.append(curancy_btc)
        curances.append(curancy_eth)
        return curances
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Привет, введи сначала количество активов (пока доступны только BTC и ETH)\n'
                          'Чтобы увидеть подробную информацию напиши /help '
                 )

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, 'FAQ\n'
                                  'Первое число - количество валют (1 - если BTC или ETH, 2 - если и то и другое,\n'
                          'второе - количество вложенных рублей, третье - криптовалюты с указанием наименования\n'
                                  'Если количество криптовалюты целое число - вводи с дробной частью\n'
                                  'Пример\n'
                                  '1ETH --- не правильно\n'
                                  '1.0ETH --- правильно\n'
                                  'Наименование криптовалюты можно писать в любом регистре,'
                                  'а дробную часть отделяй пожалуйста точкой\n'
                                  'Пример 1:\n'
                                  '1\n'
                                  '25000 0.1BTC\n'
                                  'Пример 2:\n'
                                  '2\n'
                                  '25000 0.1btc\n'
                                  '33000 1.0ETH\n'
                          'Так же ты можешь пополнить свой счет в BTC или ETH просто написав сумму, которую надо прибавить\n'
                          'ну и ещё можешь поддержать автора проекта)\n'
                          'Sber/Tink\n'
                          '89219988111\n'
                          'Или здесь в скором времени будет номер бинанс кошелька'
                 )

# btc actual curance
@bot.message_handler(content_types=['text'])
def get_balance(message):
    global btc
    global rub_btc
    global eth
    global rub_eth
    k = 0

    text = str(message.text)
    print(text)
    driver.close()
    driver.quit()

    count = re.search(r'\d{1}', text)
    if count[0] == '1':
        match_rub = re.findall(r'\s\d{2,}[^.A-Za-z\s]', text)
        match_crypt = re.findall(r'\d+[.,]\d+', text)
        valut = re.search(r'\D{3}', text)
        if valut[0].lower() == 'eth':
            eth += float(match_crypt[0])
            rub_eth += float(match_rub[0])
        elif valut[0].lower() == 'btc':
            btc += float(match_crypt[0])
            rub_btc += float(match_rub[0])

    elif count[0] == '2':
        match_rub = re.findall(r'\s\d{2,}[^.A-Za-z\s]', text)
        match_crypt = re.findall(r'\d+[,.]\d+', text)
        valut = re.search(r'\D{3}', text)
        if valut[0].lower() == 'eth':
            eth += float(match_crypt[0])
            rub_eth += float(match_rub[0])
            btc += float(match_crypt[1])
            rub_btc += float(match_rub[1])
        elif valut[0].lower() == 'btc':
            btc = float(match_crypt[0])
            rub_btc = float(match_rub[0])
            eth += float(match_crypt[1])
            rub_eth += float(match_rub[1])
    else:
        bot.send_message(message.chat.id, 'Проверьте то, что вы написали')

    print(eth, rub_eth, btc, rub_btc)

    while True:

        time_now = time.localtime().tm_hour

        if time_now in hours:

            hours.remove(time_now)
            reserv.append(time_now)
            curances = get_data()
            print(1)
            curancy_usdt = curances[0]
            curancy_btc = curances[1]
            curancy_eth = curances[2]

            if (btc > 0) and (eth == 0):

                percents_btc = ((btc * curancy_btc * curancy_usdt - rub_btc) / rub_btc) * 100
                rub_balance_now = btc * curancy_btc * curancy_usdt

                if (percents_btc >= 10) and (percents_btc < 15):
                    bot.send_message(message.chat.id, f'Срочно!\n'
                                                      f'Ваши вложения выросли на {percents_btc:.2f} процентов!\n'
                                                      f'Курс BTC - {curancy_btc:.2f} долларов\n'
                                                      f'Курс USDT - {curancy_usdt:.2f} рублей\n'
                                                      f'Ваши активы - {rub_balance_now:.2f} RUB')

                elif (percents_btc >= 15) and (percents_btc < 20):
                    bot.send_message(message.chat.id, f'Срочно!!\n'
                                                      f'Ваши вложения выросли на {percents_btc:.2f} процентов!\n'
                                                      f'Курс BTC - {curancy_btc:.2f} долларов\n'
                                                      f'Курс USDT - {curancy_usdt:.2f} рублей\n'
                                                      f'Ваши активы - {rub_balance_now:.2f} RUB')

                elif percents_btc >= 20:
                    bot.send_message(message.chat.id, f'Срочно!!!\n'
                                                      f'Ваши вложения выросли на {percents_btc:.2f} процентов!\n'
                                                      f'Курс BTC - {curancy_btc:.2f} долларов\n'
                                                      f'Курс USDT - {curancy_usdt:.2f} рублей\n'
                                                      f'Ваши активы - {rub_balance_now:.2f} RUB')

            if (btc == 0) and (eth > 0):

                percents_eth = ((eth * curancy_eth * curancy_usdt - rub_eth) / rub_eth) * 100
                rub_balance_now = eth * curancy_eth * curancy_usdt

                if (percents_eth >= 10) and (percents_eth < 15):
                    bot.send_message(message.chat.id, f'Срочно!\n'
                                                      f'Ваши вложения выросли на {percents_eth:.2f} процентов!\n'
                                                      f'Курс ETH - {curancy_eth:.2f} долларов\n'
                                                      f'Курс USDT - {curancy_usdt:.2f} рублей\n'
                                                      f'Ваши активы - {rub_balance_now:.2f} RUB')

                elif (percents_eth >= 15) and (percents_eth < 20):
                    bot.send_message(message.chat.id, f'Срочно!!\n'
                                                      f'Ваши вложения выросли на {percents_eth:.2f} процентов!\n'
                                                      f'Курс ETH - {curancy_eth:.2f} долларов\n'
                                                      f'Курс USDT - {curancy_usdt:.2f} рублей\n'
                                                      f'Ваши активы - {rub_balance_now:.2f} RUB')

                elif percents_eth >= 20:
                    bot.send_message(message.chat.id, f'Срочно!!!\n'
                                                      f'Ваши вложения выросли на {percents_eth:.2f} процентов!\n'
                                                      f'Курс ETH - {curancy_eth:.2f} долларов\n'
                                                      f'Курс USDT - {curancy_usdt:.2f} рублей\n'
                                                      f'Ваши активы - {rub_balance_now:.2f} RUB')

            if (btc > 0) and (eth > 0):

                percents_btc = ((btc * curancy_btc * curancy_usdt - rub_btc) / rub_btc) * 100
                rub_balance_now_btc = btc * curancy_btc * curancy_usdt
                percents_eth = ((eth * curancy_eth * curancy_usdt - rub_eth) / rub_eth) * 100
                rub_balance_now_eth = eth * curancy_eth * curancy_usdt

                if (percents_btc >= 10) and (percents_btc < 15):
                    bot.send_message(message.chat.id, f'Срочно!\n'
                                                      f'Ваши вложения выросли на {percents_btc:.2f} процентов!\n'
                                                      f'Курс BTC - {curancy_btc:.2f} долларов\n'
                                                      f'Курс USDT - {curancy_usdt:.2f} рублей\n'
                                                      f'Ваши активы - {rub_balance_now_btc:.2f} RUB')

                elif (percents_btc >= 15) and (percents_btc < 20):
                    bot.send_message(message.chat.id, f'Срочно!!\n'
                                                      f'Ваши вложения выросли на {percents_btc:.2f} процентов!\n'
                                                      f'Курс BTC - {curancy_btc:.2f} долларов\n'
                                                      f'Курс USDT - {curancy_usdt:.2f} рублей\n'
                                                      f'Ваши активы - {rub_balance_now_btc:.2f} RUB')

                elif percents_btc >= 20:
                    bot.send_message(message.chat.id, f'Срочно!!!\n'
                                                      f'Ваши вложения выросли на {percents_btc:.2f} процентов!\n'
                                                      f'Курс BTC - {curancy_btc:.2f} долларов\n'
                                                      f'Курс USDT - {curancy_usdt:.2f} рублей\n'
                                                      f'Ваши активы - {rub_balance_now_btc:.2f} RUB')

                if (percents_eth >= 10) and (percents_eth < 15):
                    bot.send_message(message.chat.id, f'Срочно!\n'
                                                      f'Ваши вложения выросли на {percents_eth:.2f} процентов!\n'
                                                      f'Курс ETH - {curancy_eth:.2f} долларов\n'
                                                      f'Курс USDT - {curancy_usdt:.2f} рублей\n'
                                                      f'Ваши активы - {rub_balance_now_eth:.2f} RUB')

                elif (percents_eth >= 15) and (percents_eth < 20):
                    bot.send_message(message.chat.id, f'Срочно!!\n'
                                                      f'Ваши вложения выросли на {percents_eth:.2f} процентов!\n'
                                                      f'Курс ETH - {curancy_eth:.2f} долларов\n'
                                                      f'Курс USDT - {curancy_usdt:.2f} рублей\n'
                                                      f'Ваши активы - {rub_balance_now_eth:.2f} RUB')

                elif percents_eth >= 20:
                    bot.send_message(message.chat.id, f'Срочно!!!\n'
                                                      f'Ваши вложения выросли на {percents_eth:.2f} процентов!\n'
                                                      f'Курс ETH - {curancy_eth:.2f} долларов\n'
                                                      f'Курс USDT - {curancy_usdt:.2f} рублей\n'
                                                      f'Ваши активы - {rub_balance_now_eth:.2f} RUB')

            time.sleep(random.randint(2500, 4250))

        elif time_now in sleep:
            time.sleep(3600)
            k += 1
            if k == len(sleep):
                hours.extend(reserv)
                reserv.clear()
                k = 0

        else:
            time.sleep(900)


bot.polling()