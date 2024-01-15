import telebot
from telebot import types
import requests
import time
from functools import partial

bot = telebot.TeleBot('6813673252:AAFKJX7Rwi2dQizdov_CEqQiNlRdQWyEYRg')

users = {} # создаем пустой словарь для хранения данных пользователей
role = ""

# Start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if user_id not in users:  # если пользователь не в словаре
        bot.send_message(message.chat.id, 'Привет! Для начала зарегистрируйтесь.', parse_mode='html')
        give_url(message, user_id)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        whereIsTheNextPair = types.KeyboardButton("Где следующая пара")
        scheduleForTheDayOfTheWeek = types.KeyboardButton("Расписание на день недели")
        scheduleForToday = types.KeyboardButton("Расписание на сегодня")
        scheduleForTomorrow = types.KeyboardButton("Расписание на завтра")
        whereIsTheTeacher = types.KeyboardButton("Где преподаватель")
        whenIsTheExam = types.KeyboardButton("Когда экзамен")
        comment = types.KeyboardButton("Оставить комментарий к [номер] паре [для группы]")
        whenIsTheGroup = types.KeyboardButton("Где группа / подгруппа")
        markup.row(whereIsTheNextPair)
        markup.row(scheduleForTheDayOfTheWeek, scheduleForToday, scheduleForTomorrow)
        markup.row(whereIsTheTeacher, whenIsTheExam)
        markup.row(comment, whenIsTheGroup)
        bot.send_message(message.chat.id, 'Привет! Я - твой личный эксперт и помощник по расписаниям '
                                                      'Крымского Федерального Университета '
                                                      'Я всегда в курсе актуальных расписаний университета '
                                                      'по группе ПИ-б-о-232')
        bot.send_message(message.chat.id,
                                     'На протяжении общения с ботом, общайтесь посредством кнопок. Удачи!',
                                     parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['toadmin'])
def toadmin(message):
    user_id = message.from_user.id
    # Проверяем, есть ли пользователь в словаре users
    if user_id not in users:  # если пользователь не в словаре
        bot.send_message(message.chat.id, 'Привет! Для начала зарегистрируйтесь.', parse_mode='html')
        give_url(message, user_id)
        role = requests.get(f'http://26.5.54.67:8080/role?tg_id={user_id}')
        if role == 'admin':
                # Отправляем пользователю сообщение, что он администратор
                bot.send_message(message.chat.id, 'Вы администратор. Вот ссылка на панель администратора \n')
                response = requests.get(f'http://26.5.54.67:8080/admin?tg_id={user_id}')
                bot.send_message(message.chat.id, response.text)
        else:
                # Отправляем пользователю сообщение, что он не администратор
                bot.send_message(message.chat.id, 'Вы не администратор.')
    else:
        role = requests.get(f'http://26.5.54.67:8080/role?tg_id={user_id}')
        # Сравниваем значение роли пользователя с 'admin'
        if role.text == 'admin':
            # Отправляем пользователю сообщение, что он администратор
            bot.send_message(message.chat.id, 'Вы администратор. Вот ссылка на панель администратора \n')
            response = requests.get(f'http://26.5.54.67:8080/admin?tg_id={user_id}')
            bot.send_message(message.chat.id, response.text)
        else:
            # Отправляем пользователю сообщение, что он не администратор
            bot.send_message(message.chat.id, 'Вы не администратор.')




# @bot.message_handler()
# def button(message):
#     if message.text == "Где следующая пара":
#         user_id = message.from_user.id
#         if user_id not in users:  # если пользователь не в словаре
#             bot.send_message(message.chat.id, 'Вы не зарегистрированы.')
#             bot.send_message(message.chat.id, 'Привет! Для начала напиши как я могу к тебе обращаться.'
#                                               '\n Пожалуйста укажите свое настоящее имя и фамилию.\n'
#                                               '<b>Например</b>: Щербаков Алексей', parse_mode='html')
#             bot.register_next_step_handler(message, give_url(message, user_id))
#         else:
#             bot.send_message(message.chat.id, 'Перед тем, как отправить вам необходимые данные, вы должны ответить на несколько'
#                                               'вопросов по средством встроенных кнопок')
#             keyboard = types.InlineKeyboardMarkup()
#             group1 = types.InlineKeyboardButton(text='231', callback_data='231')
#             group2 = types.InlineKeyboardButton(text='232', callback_data='232')
#             group3 = types.InlineKeyboardButton(text='233', callback_data='233')
#             keyboard.add(group1, group2, group3)
#             bot.send_message(message.chat.id, 'Выберите необходимую вам группу ПИ из предложенных', reply_markup=keyboard)
#
#     if message.text == "Расписание на день недели":
#         user_id = message.from_user.id
#         if user_id not in users:  # если пользователь не в словаре
#             bot.send_message(message.chat.id, 'Вы не зарегистрированы.')
#             bot.send_message(message.chat.id, 'Привет! Для начала напиши как я могу к тебе обращаться.'
#                                               '\n Пожалуйста укажите свое настоящее имя и фамилию.\n'
#                                               '<b>Например</b>: Щербаков Алексей', parse_mode='html')
#             bot.register_next_step_handler(message, give_url(message, user_id))
#         else:
#             bot.send_message(message.chat.id,
#                              'Перед тем, как отправить вам необходимые данные, вы должны ответить на несколько'
#                              'вопросов по средством встроенных кнопок')
#             keyboard = types.InlineKeyboardMarkup()
#             group1 = types.InlineKeyboardButton(text='231', callback_data='231')
#             group2 = types.InlineKeyboardButton(text='232', callback_data='232')
#             group3 = types.InlineKeyboardButton(text='233', callback_data='233')
#             keyboard.add(group1, group2, group3)
#             bot.send_message(message.chat.id, 'Выберите необходимую вам группу ПИ из предложенных',
#                              reply_markup=keyboard)
#
#     if message.text == "Расписание на сегодня":
#         user_id = message.from_user.id
#         if user_id not in users:  # если пользователь не в словаре
#             bot.send_message(message.chat.id, 'Вы не зарегистрированы.')
#             bot.send_message(message.chat.id, 'Привет! Для начала напиши как я могу к тебе обращаться.'
#                                               '\n Пожалуйста укажите свое настоящее имя и фамилию.\n'
#                                               '<b>Например</b>: Щербаков Алексей', parse_mode='html')
#             bot.register_next_step_handler(message, give_url(message, user_id))
#         else:
#             bot.send_message(message.chat.id,
#                              'Перед тем, как отправить вам необходимые данные, вы должны ответить на несколько'
#                              'вопросов по средством встроенных кнопок')
#             keyboard = types.InlineKeyboardMarkup()
#             group1 = types.InlineKeyboardButton(text='231', callback_data='231')
#             group2 = types.InlineKeyboardButton(text='232', callback_data='232')
#             group3 = types.InlineKeyboardButton(text='233', callback_data='233')
#             keyboard.add(group1, group2, group3)
#             bot.send_message(message.chat.id, 'Выберите необходимую вам группу ПИ из предложенных',
#                              reply_markup=keyboard)
#
#     if message.text == "Расписание на завтра":
#         user_id = message.from_user.id
#         if user_id not in users:  # если пользователь не в словаре
#             bot.send_message(message.chat.id, 'Вы не зарегистрированы.')
#             bot.send_message(message.chat.id, 'Привет! Для начала напиши как я могу к тебе обращаться.'
#                                               '\n Пожалуйста укажите свое настоящее имя и фамилию.\n'
#                                               '<b>Например</b>: Щербаков Алексей', parse_mode='html')
#             bot.register_next_step_handler(message, give_url(message, user_id))
#         else:
#             bot.send_message(message.chat.id,
#                              'Перед тем, как отправить вам необходимые данные, вы должны ответить на несколько'
#                              'вопросов по средством встроенных кнопок')
#             keyboard = types.InlineKeyboardMarkup()
#             group1 = types.InlineKeyboardButton(text='231', callback_data='231')
#             group2 = types.InlineKeyboardButton(text='232', callback_data='232')
#             group3 = types.InlineKeyboardButton(text='233', callback_data='233')
#             keyboard.add(group1, group2, group3)
#             bot.send_message(message.chat.id, 'Выберите необходимую вам группу ПИ из предложенных',
#                              reply_markup=keyboard)
#
#     if message.text == "Где преподаватель":
#         user_id = message.from_user.id
#         if user_id not in users:  # если пользователь не в словаре
#             bot.send_message(message.chat.id, 'Вы не зарегистрированы.')
#             bot.send_message(message.chat.id, 'Привет! Для начала напиши как я могу к тебе обращаться.'
#                                               '\n Пожалуйста укажите свое настоящее имя и фамилию.\n'
#                                               '<b>Например</b>: Щербаков Алексей', parse_mode='html')
#             bot.register_next_step_handler(message, give_url(message, user_id))
#         else:
#             role = requests.get(f'http://10.99.6.69:8080/role?tg_id={user_id}')
#             if role.text == "student" or role.text == "admin":
#                 bot.send_message(message.chat.id, 'Не выполнено \U0001F64F')
#             else:
#                 bot.send_message(message.chat.id, 'У вас недостаточно прав.')
#
#     if message.text == "Когда экзамен":
#         user_id = message.from_user.id
#         if user_id not in users:  # если пользователь не в словаре
#             bot.send_message(message.chat.id, 'Вы не зарегистрированы.')
#             bot.send_message(message.chat.id, 'Привет! Для начала напиши как я могу к тебе обращаться.'
#                                               '\n Пожалуйста укажите свое настоящее имя и фамилию.\n'
#                                               '<b>Например</b>: Щербаков Алексей', parse_mode='html')
#             bot.register_next_step_handler(message, give_url(message, user_id))
#         else:
#             role = requests.get(f'http://10.99.6.69:8080/role?tg_id={user_id}')
#             if role.text == "student" or role.text == "admin":
#                 bot.send_message(message.chat.id, 'С 15 по 27 января включительно\n'
#                                                   'С 17 июня по 6 июля включительно')
#             else:
#                 bot.send_message(message.chat.id, 'У вас недостаточно прав.')
#
#     if message.text == "Оставить комментарий к [номер] паре [для группы]":
#         user_id = message.from_user.id
#         if user_id not in users:  # если пользователь не в словаре
#             bot.send_message(message.chat.id, 'Вы не зарегистрированы.')
#             bot.send_message(message.chat.id, 'Привет! Для начала напиши как я могу к тебе обращаться.'
#                                               '\n Пожалуйста укажите свое настоящее имя и фамилию.\n'
#                                               '<b>Например</b>: Щербаков Алексей', parse_mode='html')
#             bot.register_next_step_handler(message, give_url(message, user_id))
#         else:
#             role = requests.get(f'http://10.99.6.69:8080/role?tg_id={user_id}')
#             if role.text == "teacher" or role.text == "admin":
#                 bot.send_message(message.chat.id,
#                                  'Перед тем, как отправить вам необходимые данные, вы должны ответить на несколько'
#                                  'вопросов по средством встроенных кнопок')
#                 keyboard = types.InlineKeyboardMarkup()
#                 group1 = types.InlineKeyboardButton(text='231', callback_data='231')
#                 group2 = types.InlineKeyboardButton(text='232', callback_data='232')
#                 group3 = types.InlineKeyboardButton(text='233', callback_data='233')
#                 keyboard.add(group1, group2, group3)
#                 bot.send_message(message.chat.id, 'Выберите необходимую вам группу ПИ из предложенных',
#                                  reply_markup=keyboard)
#             else:
#                 bot.send_message(message.chat.id, 'У вас недостаточно прав.')
#
#     if message.text == "Где группа / подгруппа":
#         user_id = message.from_user.id
#         if user_id not in users:  # если пользователь не в словаре
#             bot.send_message(message.chat.id, 'Вы не зарегистрированы.')
#             bot.send_message(message.chat.id, 'Привет! Для начала напиши как я могу к тебе обращаться.'
#                                               '\n Пожалуйста укажите свое настоящее имя и фамилию.\n'
#                                               '<b>Например</b>: Щербаков Алексей', parse_mode='html')
#             bot.register_next_step_handler(message, give_url(message, user_id))
#         else:
#             role = requests.get(f'http://10.99.6.69:8080/role?tg_id={user_id}')
#             if role.text == "teacher" or role.text == "admin":
#                 bot.send_message(message.chat.id, 'Не выполнено \U0001F64F')
#             else:
#                 bot.send_message(message.chat.id, 'У вас недостаточно прав.')
#
#
def give_url(message, user_id):
    start = time.time()
    bot.send_message(message.chat.id, "<b>Вы не зарегестрированы, зарегестрируйтесь по ссылке ниже</b>",
                         parse_mode='html')
    response = requests.get(f'http://26.5.54.67:8080/reg?tg_id={user_id}')
    bot.send_message(message.chat.id, f"{response.text}", parse_mode='html')
    elapsed_time = 0
    while (elapsed_time <= 900):
        response = requests.get(f'http://26.5.54.67:8080/sendgit?tg_id={user_id}')
        if response.text != "":
            break
        current_time = time.time()  # получаем текущее время
        elapsed_time = current_time - start  # вычисляем прошедшее время
    if response.text != "":
        users[user_id] = {'github_id': f'{response.text}'}  # создаем новую запись в словаре с пустыми данными


# @bot.callback_query_handler(func=lambda call: True)
# def callback_worker(call):
#     # Редактируем сообщение с вопросом и inlinekeyboard
#     if call.data == '231':
#         # Создаем новый объект inlinekeyboard с другими кнопками
#         global id
#         id = "1"
#         keyboard = types.InlineKeyboardMarkup()
#         even = types.InlineKeyboardButton(text='Четная', callback_data='even')
#         odd = types.InlineKeyboardButton(text='Нечетная', callback_data='odd')
#         keyboard.add(even, odd)
#         # Редактируем текст вопроса и inlinekeyboard
#         bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Какая неделя вас интересует?', reply_markup=keyboard)
#     elif call.data == '232':
#         # Создаем новый объект inlinekeyboard с другими кнопками
#         # global id
#         id = "2"
#         keyboard = types.InlineKeyboardMarkup()
#         even = types.InlineKeyboardButton(text='Четная', callback_data='even')
#         odd = types.InlineKeyboardButton(text='Нечетная', callback_data='odd')
#         keyboard.add(even, odd)
#         # Редактируем текст вопроса и inlinekeyboard
#         bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                               text='Какая неделя вас интересует?', reply_markup=keyboard)
#     elif call.data == '233':
#         # Создаем новый объект inlinekeyboard с другими кнопками
#         # global id
#         id = "3"
#         keyboard = types.InlineKeyboardMarkup()
#         even = types.InlineKeyboardButton(text='Четная', callback_data='even')
#         odd = types.InlineKeyboardButton(text='Нечетная', callback_data='odd')
#         keyboard.add(even, odd)
#         # Редактируем текст вопроса и inlinekeyboard
#         bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                               text='Какая неделя вас интересует?', reply_markup=keyboard)
#     elif call.data == 'even':
#         # Создаем новый объект inlinekeyboard с другими кнопками
#         # global id
#         id += "0"
#         keyboard = types.InlineKeyboardMarkup()
#         Monday = types.InlineKeyboardButton(text='Понедельник', callback_data='Monday')
#         Tuesday = types.InlineKeyboardButton(text='Вторник', callback_data='Tuesday')
#         Wednesday = types.InlineKeyboardButton(text='Среда', callback_data=' Wednesday')
#         Thursday = types.InlineKeyboardButton(text='Четверг', callback_data='Thursday')
#         Friday = types.InlineKeyboardButton(text='Пятница', callback_data='Friday')
#         keyboard.add(Monday, Tuesday, Wednesday, Thursday, Friday)
#         # Редактируем текст вопроса и inlinekeyboard
#         bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                               text='Какой день вас интересует?', reply_markup=keyboard)
#     elif call.data == 'odd':
#         # Создаем новый объект inlinekeyboard с другими кнопками
#         # global id
#         id += "1"
#         keyboard = types.InlineKeyboardMarkup()
#         Monday = types.InlineKeyboardButton(text='Понедельник', callback_data='Monday')
#         Tuesday = types.InlineKeyboardButton(text='Вторник', callback_data='Tuesday')
#         Wednesday = types.InlineKeyboardButton(text='Среда', callback_data=' Wednesday')
#         Thursday = types.InlineKeyboardButton(text='Четверг', callback_data='Thursday')
#         Friday = types.InlineKeyboardButton(text='Пятница', callback_data='Friday')
#         keyboard.add(Monday, Tuesday, Wednesday, Thursday, Friday)
#         # Редактируем текст вопроса и inlinekeyboard
#         bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                               text='Какой день вас интересует?', reply_markup=keyboard)
#     elif call.data == 'Monday':
#         # Создаем новый объект inlinekeyboard с другими кнопками
#         global id
#         id += "1"
#     elif call.data == 'Tuesday':
#         # Создаем новый объект inlinekeyboard с другими кнопками
#         global id
#         id += "2"
#     elif call.data == 'Wednesday':
#         # Создаем новый объект inlinekeyboard с другими кнопками
#         global id
#         id += "3"
#     elif call.data == 'Thursday':
#         # Создаем новый объект inlinekeyboard с другими кнопками
#         global id
#         id += "4"
#     elif call.data == 'Friday':
#         # Создаем новый объект inlinekeyboard с другими кнопками
#         global id
#         id += "5"
#
#
#
#
#
bot.polling(none_stop=True)
