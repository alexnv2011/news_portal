# from django.test import TestCase

# Create your tests here.

NOCENSORS = {
   'редиска',
   'хуев',
   'охуе',
   'охуи'
   'пизда',
   'пизда',
   'пизде',
   'нихуя',
   'пидор',
   'гандон'
   'блять',
   'нахуй',
   'уеба',
   'уебы',
   'ябать',
   'ебать',
   'блять',
   'нихуя',
   'хуй',
}

#@register.filter()
def censor(value):
    for nc in NOCENSORS:
        # в нижнем регистре
        if nc in value:
            s = ''
            for i in range(len(nc) - 1):
                s += '*'
            good_nc = nc[0] + s
            value = value.replace(nc, good_nc)

        # с Заглавной
        ncc = nc[0].upper() + nc[1:]
        if ncc in value:
            s = ''
            for i in range(len(ncc) - 1):
                s += '*'
            good_nc = ncc[0] + s
            value = value.replace(ncc, good_nc)
    return f'{value}'

str = '''Нахуй хуй asdadas sa asd as da редиска
Пидор Блять
редиска
пизда охуеть нахуй ебать блять
'''
print(censor(str))