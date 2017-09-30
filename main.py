#!/usr/bin/env python

import logging
from os import environ
from telegram.ext import Updater, CommandHandler
from post_office import command_pkg

telegram_token = environ['TELEGRAM_TOKEN']

def command_help(bot, update):
    reply = """Это я, почтальон Печкин, принёс журнал «Мурзилка» для вашего мальчика!

Команды:
/pkg CA123456789RU — Информация о посылке"""

    update.message.reply_text(reply)

def error(bot, update, error):
    logging.getLogger().warn('Update "%s" caused error "%s"' % (update, error))

def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    updater = Updater(telegram_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', command_help))
    dispatcher.add_handler(CommandHandler('help',  command_help))
    dispatcher.add_handler(CommandHandler('pkg',   command_pkg))
    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
