import telebot
from telebot import types

import config
import questions
import answers

UnqueUsername = {}
Education = {}
VidQuestion = {}

bot = telebot.TeleBot(config.BOTTOKEN)

#MyUserName = ''

#Переменные во избежание нелепых ошибок(Костыль по своей сути)
messages = [
    '🤟 Я ещё школьник!', 'Далее...','🎓 Я уже студент!',
    "К вопросам...", "🤟 Погнали!", '/start',
    '/help', '/changename', '/changeeducation'
    ]

listOfNumbers = '12345678910'

#Приветствие
@bot.message_handler(commands=['start'])
def start(message):
    a = bot.send_message(message.chat.id, '👋 Привет! Меня зовут Макс, я помогу тебе с Ависмой! Для начала, давай познакомимся. Как тебя зовут?')
    bot.send_photo(message.chat.id,'https://i.postimg.cc/1XbZsy7D/AVISMABOT335.png')
    bot.register_next_step_handler(a, FirstInfo)
    VidQuestion[message.from_user.username] = False

#Вступление вплоть до вопросов
@bot.message_handler(content_types=['text'])
def FirstInfo(message):
    #global IsName
    
    if message.text not in messages and message.text not in listOfNumbers and VidQuestion[message.from_user.username] == False:
        VidQuestion[message.from_user.username] = False
        UnqueUsername[message.from_user.id] = message.text
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Далее...")
        markup.add(btn1)
        bot.send_message(message.chat.id, f'😊 Рад знакомству, {message.text}!', reply_markup=markup)
   
    elif (message.text == 'Далее...'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        
        btn1 = types.KeyboardButton("🤟 Я ещё школьник!")
        btn2 = types.KeyboardButton("🎓 Я уже студент!")
        
        markup.add(btn2)
        markup.add(btn1)
        
        bot.send_message(message.chat.id, f'🤔 {UnqueUsername[message.from_user.id]}, ты ещё учишься в школе, или уже успел стать студентом?',reply_markup=markup)
    
    elif message.text == '🤟 Я ещё школьник!':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("🤟 Погнали!")
        
        markup.add(btn1)
        
        bot.send_message(message.chat.id, '👍 Это круто! Специально для тебя я подобрал интересующие школьников вопросы!', reply_markup=markup)
        bot.send_message(message.chat.id, '👌 Просто напиши номер интересующего тебя вопроса и я предоставлю всю актуальную информацию!')
        
        Education[message.from_user.username] = 'School'


    elif message.text == '🎓 Я уже студент!':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("🤟 Погнали!")
        
        markup.add(btn1)
        
        bot.send_message(message.chat.id, '👍 Это круто! Специально для тебя я подобрал интересующие студентов вопросы!', reply_markup=markup)
        bot.send_message(message.chat.id, '👌 Просто напиши номер интересующего тебя вопроса и я предоставлю всю актуальную информацию!')

        Education[message.from_user.username] = 'Student'
    
    elif message.text == "🤟 Погнали!":
        SecondPart(message)


#Показываем список вопросов и перенаправляем на следующую функцию
def SecondPart(message):
    #UserId = message.from_user.id
    bot.send_message(message.chat.id, '🤓 Список вопросов:')
    QuestionsShow(message, message.from_user.username)
    a = bot.send_message(message.chat.id, 'Номер вопроса: ', reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(a, NextPart)
    
#Ответы на вопросы
@bot.message_handler(content_types=['text'])
def NextPart(message):
    if (message.text not in messages) and VidQuestion[message.from_user.username] != True:
        CheckResult = Check(message.text)
        if (message.text) and CheckResult: # and (isinstance(message.text, str))
            if int(message.text) <= len(answers.Student): 
                markup = types.InlineKeyboardMarkup()
                btn1 = types.InlineKeyboardButton('Показать список вопросов', callback_data='button1')
                btn2 = types.InlineKeyboardButton('Изменить образвание', callback_data='button2')
                btn3 = types.InlineKeyboardButton('Задать свой вопрос',callback_data='question')
                markup.add(btn1, btn2)
                markup.add(btn3)
                MessageNumberArray = int(message.text)-1
                bot.send_message(message.chat.id, '😉 Нашёл ответ на твой вопрос!')
                #Картинка
                if answers.ImageStudents[MessageNumberArray] != None: bot.send_photo(message.chat.id, answers.ImageStudents[MessageNumberArray])
                #Ссылка-кнопка
                if answers.LinksStudents[MessageNumberArray] != None:
                    button1 = types.InlineKeyboardButton(answers.LinksNames[MessageNumberArray], url= answers.LinksStudents[MessageNumberArray])
                    markup.add(button1)
                #Сам текст
                a= bot.send_message(message.chat.id, answers.Student[MessageNumberArray], reply_markup=markup)
                #Переход
                bot.register_next_step_handler(a, NextPart)
            else:
                markup = types.InlineKeyboardMarkup()
                btn1 = types.InlineKeyboardButton('Показать список вопросов', callback_data='button1')
                btn2 = types.InlineKeyboardButton('Изменить образвание', callback_data='button2')
                btn3 = types.InlineKeyboardButton('Задать свой вопрос',callback_data='question')
                markup.add(btn1, btn2)
                markup.add(btn3)
                a = bot.send_message(message.chat.id, '🙃 Нет такого вопроса! Пожалуйста, введи корректный номер вопроса, чтобы я смог дать на него ответ.',reply_markup=markup)
                bot.register_next_step_handler(a, NextPart)
        else:
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton('Показать список вопросов', callback_data='button1')
            btn2 = types.InlineKeyboardButton('Изменить образование', callback_data='button2')
            btn3 = types.InlineKeyboardButton('Задать свой вопрос',callback_data='question')
            markup.add(btn1, btn2)
            markup.add(btn3)
            a = bot.send_message(message.chat.id, '😞 Что-то пошло не так! Попробуй задать вопрос ещё раз!', reply_markup=markup)
            bot.register_next_step_handler(a, NextPart)    
    elif (message.text not in messages) and VidQuestion[message.from_user.username] == True:
        bot.forward_message(6412001806,message.chat.id, message.message_id)
        VidQuestion[message.from_user.id] = False
@bot.callback_query_handler(func=lambda call: call.data == 'button1')
def ShowQuest(call):
    user = call.from_user.username
    
    message = call.message
    bot.send_message(message.chat.id, 'Список вопросов:')
    QuestionsShow(message, user)

@bot.callback_query_handler(func=lambda call: call.data == 'button2')
def ChangeEdu(call):
    user = call.from_user.username
    print(user)
    message = call.message
    match Education[user]:
        case 'Student': 
            Education[user] = 'School'
            bot.send_message(message.chat.id, 'Образование изменено на школьное.\n\n Новый список вопросов:')
        case 'School': 
            Education[user] = 'Student'
            bot.send_message(message.chat.id, 'Образование изменено на студенчесское.\n\n Новый список вопросов:')
    QuestionsShow(message, user)

@bot.callback_query_handler(func=lambda call: call.data == 'question')
def anketa(call):
    user = call.from_user.username
    VidQuestion[user] = True
    message = call.message
    bot.send_message(message.chat.id, 'Введи интересующий тебя вопрос, я отправлю его сотруднику АВИСМЫ и он сможет ответить на него ')
    


#Проверка на буквы в числе
def Check(text):
    Result = True
    for i in text:
        if i not in listOfNumbers:
            Result = False
            break
        else: Result = True
    return Result

#Отобрадение списка вопросов
def QuestionsShow(message, username):
    UserId = username
    
    markup = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton('Изменить образование', callback_data='button2')
    btn3 = types.InlineKeyboardButton('Задать свой вопрос',callback_data='question')
    markup.add(btn2)
    markup.add(btn3)
    
    questions.FinalMessage = ''
    if Education[UserId] == 'School':
        for i,value in enumerate(questions.School,1):
            questions.FinalMessage += str(i) + " • "+ value + '\n'
    elif Education[UserId] == 'Student':
        for i,value in enumerate(questions.Student,1):
            questions.FinalMessage += str(i) + " • "+ value + '\n'
    bot.send_message(message.chat.id,  questions.FinalMessage, reply_markup=markup)

bot.polling(none_stop=True, interval=0) 