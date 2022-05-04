from django import template

register = template.Library()

STRONG_WORDS = ["php", "редиска"]


@register.filter()
def censor(value):
   if not isinstance(value, str):
       raise ValueError('Нельзя цензурировать не строку')

   for word in STRONG_WORDS:
       value = value.replace(word[1:], '*' * (len(word)-1))

   return value

# Мой ответ
# CENSOR_WORDS = {
#     'Редиска':'Р******',
#     'Редиска!':'Р******!',
#     'редиска':'р******',
# }
#
# @register.filter()
# def censor(value):
#     list_ = list(value.split())
#     for v in list_:
#         if v in CENSOR_WORDS.keys():
#             value = value.replace(v, CENSOR_WORDS[v])
#     return value
