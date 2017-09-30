from os import environ
from time import sleep
from datetime import datetime
import aftership

aftership_token = environ['AFTERSHIP_TOKEN']
post = 'russian-post'

status_description = {
    'InfoReceived'      : "Скоро вышлю",
    'InTransit'         : "Посылка в пути",
    'OutForDelivery'    : "Посылка готова к вручению",
    'AttemptFail'       : "Не смог доставить посылку",
    'Delivered'         : "Посылка доставлена",
    'Exception'         : "С посылкой что-то пошло не так",
    'Expired'           : "Посылка протухла",
    'Pending'           : "Не знаю что с посылкой"
}

delivery_time_str = {
    'InTransit'         : " {0} дней",
    'OutForDelivery'    : " ({0} дней в пути)",
    'AttemptFail'       : " ({0} дней в пути)",
    'Delivered'         : " за {0} дней",
    'Exception'         : " ({0} дней в пути)",
    'Expired'           : " ({0} дней в пути)"
}

def command_pkg(bot, update):
    words = update.message.text.split()

    if len(words) != 2:
        update.message.reply_text("Надо указать трек-номер")
        return

    track_num = words[1]
    if len(track_num) != 13:
        update.message.reply_text("Трек-номер должен состоять из 13 символов")
        return

    try:
        trk = tracking.get(post, track_num)
    except:
        # Create if not found and try again
        update.message.reply_text("Пойду поищу в отделении...")
        tracking.post(tracking=dict(slug=post, tracking_number=track_num, title="Test"))
        sleep(10)
        trk = tracking.get(post, track_num)

    try:
        trk = trk['tracking']
        status = trk['tag']
        reply = status_description[status]
    except:
        reply = "Не могу найти посылку"

    if status == 'OutForDelivery':
        try:
            checkpoint = trk['checkpoints'][-1]
            reply += " в %s %s" % (
                     checkpoint['country_name'], checkpoint['location'])
        except:
            pass

    try:
        delivery_time = delivery_time_str[status]
        reply += delivery_time.format(trk['delivery_time'])
    except:
        pass

    if status == 'InTransit':
        try:
            checkpoint = trk['checkpoints'][-1]
            reply += ", последний раз её видели"
            delta = datetime.now() - checkpoint['checkpoint_time']
            if delta.days > 0:
                reply += " %d дней назад" % delta.days
            else:
                if checkpoint['checkpoint_time'].day == datetime.today().day:
                    reply += " сегодня"
                else:
                    reply += " вчера"
            reply += " в %s %s (%s)" % (
                     checkpoint['country_name'], checkpoint['location'], checkpoint['message'])
        except:
            pass

    update.message.reply_text(reply)

#
global tracking
tracking = aftership.APIv4(aftership_token).trackings
