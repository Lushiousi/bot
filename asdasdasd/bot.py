import telebot
from telebot import types

bot = telebot.TeleBot('6143986083:AAFCzZL36ovCBFH-Vl7Pn0ZoGhCn73DXRSk')
registered_users = {}


# Словарь для хранения зарегистрированных пользователей
registered_users = {}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    # Проверяем, зарегистрирован ли уже пользователь
    if message.chat.id in registered_users:
        bot.send_message(message.chat.id, 'Вы уже зарегистрированы!')
    else:
        # Запрашиваем у пользователя имя для регистрации
        bot.send_message(message.chat.id, 'Введите ваше имя:')
        bot.register_next_step_handler(message, register)

# Функция для обработки следующего шага регистрации
def register(message):
    # Получаем имя пользователя из сообщения
    name = message.text

    # Регистрируем нового пользователя
    registered_users[message.chat.id] = name
    bot.send_message(message.chat.id, 'Вы успешно зарегистрированы!')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    if message.text == '👋 Поздороваться':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
            btn1 = types.KeyboardButton('клиент')
            btn2 = types.KeyboardButton('страховщик')
            markup.add(btn1, btn2)
            bot.send_message(message.from_user.id, 'клиент/страховщик', reply_markup=markup)#ответ бота

            if message.text == 'клиент':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
                btn1 = types.KeyboardButton('подать заявку на страхование') 
                btn2 = types.KeyboardButton('посмотреть свои заявки') 
                btn3 = types.KeyboardButton('просмотреть историю заявок')
                markup.add(btn1, btn2, btn3) 
                bot.send_message(message.from_user.id, '')


bot.polling(none_stop=True, interval=0) 