from django.utils import timezone


def PluralRubleForm(number):

    last_digid = number % 10
    ruble_word_form = ''

    if last_digid == 1:
        ruble_word_form = 'рубль'
    elif 0 < last_digid < 5:
        ruble_word_form = 'рубля'
    else:
        ruble_word_form = 'рублей'

    return ruble_word_form


def filter_orders(objects):
    return objects.filter(
        service__is_shown=True,
        service__master__is_shown=True,
        start_time__lte=timezone.now()
    )
