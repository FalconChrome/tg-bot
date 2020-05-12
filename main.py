import json
from os import path
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, Filters
from telegram.ext import MessageHandler, CommandHandler, ConversationHandler
from random import randrange, shuffle


class Bot:
    DATA = 'data'
    IMAGES = path.join('data', 'images')
    TOKEN = open(path.join(DATA, 'QB token')).read().strip()
    QUESTIONS = json.load(open(path.join(DATA,
                                         ('questions.json'))))['questions']
    # Структура файла вопросов:
    # {'questions': [[вопрос, правильный_ответ, *неправильные_ответы], ...]}

    def __init__(self):
        updater = Updater(self.TOKEN, use_context=True)

        # Получаем из него диспетчер сообщений.
        dp = updater.dispatcher

        dp.add_handler(CommandHandler('help', self.help))
        conv_handler = ConversationHandler(
            # Точка входа в диалог.
            # В данном случае — команда /start. Она задаёт первый вопрос.
            entry_points=[CommandHandler('start', self.start, pass_user_data=True)],

            states={
                1: [MessageHandler(~Filters.command & Filters.text, self.answer,
                                   pass_user_data=True)]
            },

            # Точка прерывания диалога. В данном случае — команда /stop.
            fallbacks=[CommandHandler('stop', self.stop, pass_user_data=True)]
        )
        dp.add_handler(conv_handler)

        # Запускаем цикл приема и обработки сообщений.
        updater.start_polling()

        # Ждём завершения приложения.
        updater.idle()

    def ask(self, update, context):
        n_left = len(context.user_data['not asked'])
        if n_left <= 0:
            return True
        q = context.user_data['not asked'].pop(randrange(n_left))
        context.user_data['current'] = q
        markup = self.markup(q)
        update.message.reply_text(self.QUESTIONS[q][0], reply_markup=self.markup(q))

    def markup(self, q):
        items = self.QUESTIONS[q][1:]
        shuffle(items)
        items = [items[:2], items[2:]]
        return ReplyKeyboardMarkup(items, one_time_keyboard=True)

    def answer(self, update, context):
        ans = update.message.text
        if ans == self.QUESTIONS[context.user_data['current']][1]:
            context.user_data['right n'] += 1
        if self.ask(update, context):
            self.show_res(update, context)
            return ConversationHandler.END
        return 1

    def start(self, update, context):
        context.user_data['not asked'] = list(range(len(self.QUESTIONS)))
        context.user_data['current'] = 0
        context.user_data['right n'] = 0
        update.message.reply_text("Здравствуйте! Сейчас мы проведём викторину!")
        self.ask(update, context)
        return 1

    def help(self, update, context):
        update.message.reply_text(
            """/start - запуск викторины
/help - помощь
/stop - завершить викторину

deployed by heroku v1.0""")

    def stop(self, update, context):
        context.user_data['not asked'].append(context.user_data['current'])
        self.show_res(update, context)
        return ConversationHandler.END

    def show_res(self, update, context):
        update.message.reply_text('Завершение викторины',
                                  reply_markup=ReplyKeyboardRemove())
        n_asked = len(self.QUESTIONS) - len(context.user_data['not asked'])
        res = context.user_data['right n']
        update.message.reply_text(f"Ваш результат: {res} из {n_asked}.")
        if n_asked == 0:
            return None
        if res / n_asked < 0.9:
            context.bot.send_photo(
                update.message.chat_id,  # Идентификатор чата.
                open(path.join(self.IMAGES, 'low.jpg'), 'rb'),
                caption="Не расстраивайтесь!"
            )
        else:
            context.bot.send_photo(
                update.message.chat_id,
                open(path.join(self.IMAGES, 'high.jpg'), 'rb'),
                caption="Вы хорошо эрудированы!"
            )


if __name__ == '__main__':
    bot = Bot()
