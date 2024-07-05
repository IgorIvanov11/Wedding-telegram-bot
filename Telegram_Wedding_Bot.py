import telebot
from telebot import types
import emoji
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot('your token')

users = ['user1'] # list of users invited to the wedding. In this step only invited users have access.
answers = {}

@bot.message_handler(commands=['start'])
def send_wedding_message(message):
    if message.from_user.username in users:
        bot.send_message(message.chat.id, 'Здравствуйте, дорогие гости!')
        bot.send_photo(message.chat.id,
                       "your URL link to the welcome image")
        ask_attendance(message)
    else:
        bot.send_message(message.chat.id, 'Вы не являетесь приглашенным гостем на нашу свадьбу.')

def ask_attendance(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    item_yes = types.KeyboardButton('Да')
    item_no = types.KeyboardButton('Нет')
    markup.add(item_yes, item_no)
    msg = bot.send_message(message.chat.id, "Вы придете на нашу свадьбу?", reply_markup=markup)
    bot.register_next_step_handler(msg, attendance_callback)

def attendance_callback(message):
    chat_id = # Here write your personal chat id so that messages about users' replies will be sent to you.
    if message.text == 'Да':
        bot.send_message(chat_id, f'Гость "{message.from_user.first_name} {message.from_user.last_name} "({message.from_user.username})" " будет на свадьбе!'+ emoji.emojize(":check_mark:"))
        answers[message.from_user.username] = message.text
        bot.send_message(message.chat.id, 'Отлично! '+ emoji.emojize(":grinning_face:") +' Хотите узнать подробнее?')
        markup = types.ReplyKeyboardMarkup(row_width=1)
        item1 = types.KeyboardButton('План вечера')
        item2 = types.KeyboardButton('Место проведения')
        item3 = types.KeyboardButton('Наши пожелания')
        item4 = types.KeyboardButton('Контакты организатора')
        markup.add(item1, item2, item3, item4)
        msg = bot.send_message(message.chat.id, 'Выберите что вас интересует', reply_markup=markup)
        bot.register_next_step_handler(msg, info_callback)
    elif message.text == 'Нет':
        bot.send_message(chat_id, f'Гость {message.from_user.first_name} {message.from_user.last_name} "({message.from_user.username})" не сможет присутствовать на свадьбе.'+ emoji.emojize(":cross_mark:"))
        bot.send_message(message.chat.id, 'Очень жаль '+ emoji.emojize(":crying_face:"), reply_markup=types.ReplyKeyboardRemove())
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, выберите Да или Нет')
        ask_attendance(message)



transport_needed = None


@bot.message_handler(content_types=['text'])
def info_callback(message):
    if message.text == 'План вечера':
        bot.send_message(message.chat.id,
                         '<b>Мы расскажем историю нашей семьи и будем счастливы разделить с вами радость нашего дня</b> ' + emoji.emojize(
                             ":man_in_tuxedo:") + emoji.emojize(":person_with_veil:") +
                         '\n\n🥂 Встречаемся 08.06.2023 в 15:30 на фуршете;' +
                         '\n\n💍 Начало церемонии в 16:30;' +
                         '\n\n💃🕺 Будем благодарны, если при выборе одежды на наше торжество вы не будете придерживаться палитры и наденете свой самый красивый наряд. \nФорма одежды - торжественная;' +
                         '\n\n👠 Девушки, просим вас воздержаться от туфлей на высоких каблуках или спланировать её как сменную обувь, так как дорога до места проведения мероприятия грунтовая.' +
                         '\n\n🌥️ Заранее подумайте о погоде, так как вечером может стать прохладнее и потребуется теплая одежда.',
                         parse_mode='HTML')


    elif message.text == 'Место проведения':
        global transport_needed
        transport_needed = None
        keyboard = InlineKeyboardMarkup()
        location_button = InlineKeyboardButton(text="Как добраться?", callback_data="location")
        keyboard.add(location_button)
        bot.send_photo(message.chat.id,
                       "https://weddywood.ru/wp-content/uploads/2021/02/nikita-i-vlada__2_0_weddywood.jpg")
        bot.send_message(message.chat.id, '📍Место проведения:'
                                          '\nPine river, Калужская область, Жуковский район, сельское поселение Деревня Верховье, территория База отдыха Сосновый городок, 1', reply_markup=keyboard)
        bot.send_location(message.chat.id, 54.955160851065784, 36.77342983094527)
    elif message.text == 'Наши пожелания':
        bot.send_message(message.chat.id, '🎁 Мы будем признательны за выбор подарка в конверте;\n\n🥀 🍷 Пожалуйста, не дарите нам цветы, так как мы не успеем насладиться их красотой. Приятным комплиментом для нас вместо цветов будет бутылка вашего любимого вина, которое, мы обещаем, не завянет.')
    elif message.text == 'Контакты организатора':
        bot.send_message(message.chat.id, '☎ На все вопросы, связанные с торжеством, ответит наш свадебный организатор Имя: +7(000)000-00-00')
    else:
        bot.send_message(message.chat.id, 'Неправильный выбор')
        ask_attendance(message)

    markup = types.ReplyKeyboardMarkup(row_width=1)
    item1 = types.KeyboardButton('План вечера')
    item2 = types.KeyboardButton('Место проведения')
    item3 = types.KeyboardButton('Наши пожелания')
    item4 = types.KeyboardButton('Контакты организатора')
    markup.add(item1, item2, item3, item4)
    msg = bot.send_message(message.chat.id, 'Выберите что вас интересует', reply_markup=markup)
    bot.register_next_step_handler(msg, info_callback)


@bot.callback_query_handler(func=lambda call: call.data == "location")
def handle_location_callback(call):
    if call.message:
        bot.answer_callback_query(callback_query_id=call.id)
        keyboard = InlineKeyboardMarkup()
        yes_button = InlineKeyboardButton(text="Да", callback_data="yes")
        no_button = InlineKeyboardButton(text="Нет", callback_data="no")
        keyboard.add(yes_button, no_button)
        bot.send_message(call.message.chat.id, 'Дорогие гости, мы организовываем трансфер до места проведения.\nСкажите нам, пожалуйста, потребуется ли Вам трансфер?', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data in ['yes', 'no'])
def handle_transport_callback(call):
    if call.message:
        bot.send_message(call.message.chat.id,'Спасибо за ответ! Если ваш выбор был положительным, с Вами свяжутся и дадут полную информацию по трансферу.')
        bot.answer_callback_query(callback_query_id=call.id)
        last_name = call.message.chat.last_name if call.message.chat.last_name else ""
        user_name = call.message.chat.first_name + " " + last_name
        transport = "поедет на транспорте " + emoji.emojize(":bus:") if call.data == "yes" else "доберется самостоятельно" + emoji.emojize(":person_walking:")
        bot.send_message(408158395, f'Гость "{user_name} ({call.message.chat.username})" {transport}')

        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)





bot.polling()
