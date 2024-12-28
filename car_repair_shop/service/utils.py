def PluralRubleForm(number):

    last_digid = number % 10
    ruble_word_form = ''

    if last_digid == 1:
        ruble_word_form = 'рубль'
    elif last_digid < 5:
        ruble_word_form = 'рубля'
    else:
        ruble_word_form = 'рублей'

    return ruble_word_form
