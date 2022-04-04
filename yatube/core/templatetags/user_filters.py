# yatube/core/temlatetags/user_filters.py
from django import template

# В template.Library зарегистрированы все встроенные теги и фильтры шаблонов
# пока я учусь - подобные комментарии мне нужны
register = template.Library()


@register.filter
# функция как пример - переделать
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


# проверка залогиненного юзера на авторство
def required_edit(user, author) -> bool:
    return user == author
