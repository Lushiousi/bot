import telebot
import mysql.connector
from telebot import types

# Подключение к базе данных MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
)

# Создание курсора для работы с базой данных
cursor = db.cursor()

# Создание базы данных users
cursor.execute("CREATE DATABASE IF NOT EXISTS users")

#
cursor.execute("USE users")


# Создание таблицы users
cursor.execute(
    "CREATE TABLE IF NOT EXISTS users (user_id INT PRIMARY KEY, login VARCHAR(255), password VARCHAR(255), role VARCHAR(255))")

cursor.execute("""
CREATE TABLE IF NOT EXISTS requests (
  id INT AUTO_INCREMENT PRIMARY KEY,
  client_name VARCHAR(255),
  request_text TEXT,
  date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  user_id_fk int,
  foreign key (user_id_fk) references users (user_id)
)
""")

# Создание экземпляра бота с токеном вашего бота
bot = telebot.TeleBot('6583203649:AAH1c0OiZaUjumi5Mqa5CjotNC-2VvSdHYI')

# Обработчик команды /start


@bot.message_handler(commands=['start'])
def start(message_start):
    # Проверяем, зарегистрирован ли уже пользователь
    user_id = message_start.chat.id
    if is_registered(user_id):
        bot.send_message(user_id, 'Вы уже зарегистрированы!')
    else:
        bot.send_message(user_id, 'Введите ваш логин:')
        bot.register_next_step_handler(message_start, ask_password)

# Функция для проверки, зарегистрирован ли пользователь


def is_registered(user_id):
    query = "SELECT * FROM users WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    return result is not None

# Функция для обработки следующего шага регистрации - запрос пароля


def ask_password(message_ask_password):
    user_id = message_ask_password.chat.id
    login = message_ask_password.text

    if is_registered(user_id):
        bot.send_message(
            user_id, 'Пользователь с таким логином уже зарегистрирован!')
    else:
        bot.send_message(user_id, 'Введите ваш пароль:')
        bot.register_next_step_handler(message_ask_password, ask_role, login)

# Функция для обработки следующего шага регистрации - запрос роли


def ask_role(message_ask_role, login):
    user_id = message_ask_role.chat.id
    password = message_ask_role.text

    markup = types.ReplyKeyboardMarkup(row_width=2)
    markup.add(types.KeyboardButton('Страховщик'), types.KeyboardButton(
        'Клиент'), types.KeyboardButton('Админ'))
    bot.send_message(user_id, 'Выберите вашу роль:', reply_markup=markup)
    bot.register_next_step_handler(message_ask_role, register, login, password)

# Функция для обработки следующего шага регистрации - сохранение данных пользователя


def register(message_register, login, password):
    user_id = message_register.chat.id
    role = message_register.text

    query = "INSERT INTO users (user_id, login, password, role) VALUES (%s, %s, %s, %s)"
    values = (user_id, login, password, role)
    cursor.execute(query, values)
    db.commit()

    bot.send_message(user_id, 'Вы успешно зарегистрированы!')

# Обработчик команды /login


@bot.message_handler(commands=['login'])
def login(message_login):
    user_id = message_login.chat.id
    bot.send_message(user_id, 'Введите ваш логин:')
    bot.register_next_step_handler(message_login, check_login)

# Функция для проверки введенного логина и пароля


def check_login(message_check_login):
    user_id = message_check_login.chat.id
    login = message_check_login.text

    query = "SELECT * FROM users WHERE login = %s"
    cursor.execute(query, (login,))
    result = cursor.fetchone()

    if result is None:
        bot.send_message(user_id, 'Неверный логин!')
    else:
        bot.send_message(user_id, 'Введите ваш пароль:')
        bot.register_next_step_handler(
            message_check_login, check_password, result)

# Функция для проверки введенного пароля и роли


def check_password(message_check_password, user_data):
    user_id = message_check_password.chat.id
    password = message_check_password.text

    if password == user_data[2]:
        bot.send_message(user_id, 'Вы успешно вошли!')
        role = user_data[3]
        if role == 'Страховщик':
            # Действия для страховщика
            pass
        elif role == 'Клиент':
            # Действия для клиента
            markup = types.ReplyKeyboardMarkup(row_width=2)
            markup.add(types.KeyboardButton('Фото транспортного средства'),
                       types.KeyboardButton('Текст с фотографиями загородного дома'))
            bot.send_message(
                user_id, 'Выберите тип сообщения:', reply_markup=markup)
            bot.register_next_step_handler(
                message_check_password, handle_client_choice)
        elif role == 'Админ':
            # Действия для админа
            pass
    else:
        bot.send_message(user_id, 'Неверный пароль!')

# Функция для обработки выбора клиента


def handle_client_choice(message_choise):
    user_id = message_choise.chat.id
    choice = message_choise.text
    if choice == 'Фото транспортного средства':
        bot.send_message(
            user_id, 'Пожалуйста, отправьте фотографии транспортного средства по данному шаблону')
        bot.send_message(user_id, 'Транспортное средство должно быть в чистом виде \n Не принимаются фото транспортного средства в разобранном виде или в процессе ремонта (установки противоугонных устройств и т.п.) \nВ процессе проведения осмотра необходимо сделать следующие фотографии: \n фото VIN-номера на металле – минимум 1 фотофото транспортного средства снаружи – минимум 8 фото: с 4-х сторон + с 4-х углов (допускается больше при необходимости) \nфото лобового стекла – минимум 1 фото \nфото маркировки лобового стекла – 1 фото \nфото колеса в сборе – минимум 1 фото (должны читаться размер и производитель шины); \nфото показаний одометра (пробег) – 1 фото \nфото салона – минимум 2 фото: \nпередняя часть салона с приборной панелью + задняя часть салона \nфото всех повреждений (при наличии) – неограниченное количество фото \nфото штатных ключей + ключей/брелоков/меток от дополнительных противоугонных устройств.')
        bot.register_next_step_handler(message_choise, handle_photo)
    elif choice == 'Текст с фотографиями':
        bot.send_message(
            user_id, 'Пожалуйста, отправьте текст с фотографиями!')
    else:
        bot.send_message(user_id, 'Неверный выбор!')


def handle_photo(message_handle_photo):
    photos = []
    user_id = message_handle_photo.chat.id
    if message_handle_photo.content_type == "photo":
        photos.insert(0, message_handle_photo)
        if len(photos) >= 1:

            # Выполнить действия, если отправлена хотя бы одна фотография
            bot.send_message(user_id, f"Вы отправили {len(photos)} фотографии")
            bot.register_next_step_handler(
                message_handle_photo, new_request)  # Возвращает выбор к if

        else:
            # Выполнить действия, если не отправлена ни одна фотография
            bot.send_message(
                user_id, "Пожалуйста, отправьте хотя бы одну фотографию транспортного средства!")
            bot.register_next_step_handler(
                message_handle_photo, handle_photo)  # Возвращает выбор к if
    else:
        bot.send_message(
            user_id, "Пожалуйста, отправьте фотографию транспортного средства!")
        bot.register_next_step_handler(
            message_handle_photo, handle_photo)  # Возвращает выбор к if


def new_request(message_new_request):
    user_id = message_new_request.chat.id
    client_name = message_new_request.from_user.first_name
    requests_text = message_new_request.text
    request = "INSERT INTO requests (client_name, request_text, user_id_fk) VALUES (%s, %s, %s)"
    values = (client_name, requests_text, user_id)
    cursor.execute(request, values)
    db.commit()
    bot.send_message(
        user_id, "Введите информацию про ваш страховой случай")


# Запуск бота
bot.polling()
