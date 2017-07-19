from django.conf import settings
from django.conf.urls import url
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.utils.baseconv import base56

from random import randint
from urllib.parse import urlparse


# Задание 3. URL shortener
#
# Реализуйте сервис для сокращения ссылок. Примеры таких сервисов:
# http://bit.ly, http://t.co, http://goo.gl
# Пример ссылки: http://bit.ly/1qJYR0y
#
# Вам понадобится шаблон с формой для отправки ссылки (файл index.html),
# и две функции, одна для обработки запросов GET и POST для сабмита URL
# и отображения результата, и вторая для редиректа с короткого URL на исходный.
# Для хранения соответствий наших коротких ключей и полных URL мы будем
# использовать кеш Django, django.core.cache
# Экземпляр cache уже импортирован, и используется следующим образом.
# Сохранить значение:
#
#  cache.add(key, value)
#
# Извлечь значение:
#
#  cache.get(key, default_value)
#
# Второй аргумент метода get - значение по умолчанию, если ключ не найден в кеше.
#
# Для проверки корректности реализации ваших функций,
# запустите этот файл на выполнение:
#
# python homework4.py test homework4
#
# (последний аргумент - это указание, где искать тесты - в текущем модуле)
# Также вы можете запустить сервер для разработки, и посмотреть
# ответы ваших функций в браузере:
#
# python homework4.py runserver


# Конфигурация, не редактировать
if not settings.configured:
    settings.configure(
        DEBUG=True,
        ROOT_URLCONF=__name__,
        TEMPLATES=[{'BACKEND': 'django.template.backends.django.DjangoTemplates',
                    'DIRS': ['']
                    }],
        ALLOWED_HOSTS=['127.0.0.1']
    )
# 1. Index
#
# При запросе методом GET, отдаем HTML страницу (шаблон index.html) с формой
# с одним полем url типа text (отредактируйте шаблон, дополните форму).
# При отправке формы методом POST извлекаем url из request.POST и делаем следующее:
#
# 1. Проверяем URL. Допускаются следующие схемы: http, https, ftp

ALLOWED_SCHEMES = {'http', 'https', 'ftp'}


def validate_url(url):
    url_parse = urlparse(url)
    if url_parse.scheme in ALLOWED_SCHEMES:
        return url
    else:
        errors = 'Такие схемы не поддерживаються! поддерживаються только' + str(ALLOWED_SCHEMES)
        return {'errors': errors}
# Для реализации проверки проще всего разобрать URL функцией urllib.parse.urlparse
# Если URL не прошел проверку - отобразите на нашей странице с формой сообщение о том,
# какие схемы поддерживаются.
#
# Если URL прошел проверку:
#
# 2. Создаем случайный короткий ключ, состоящий из цифр и букв.
# Воспользуйтесь реализацией ниже или напишите свою.


def random_key():
    return base56.encode(randint(0, 0x7fffff))

# 3. Сохраняем URL в кеш со сгенерированным ключом:
#
#    cache.add(key, url)
#
# 4. Отдаем ту же страницу с формой и дополнительно отображаем на ней
# кликабельную короткую ссылку (HTML тег 'a') вида http://localhost:8000/наш_короткий_ключ


def index(request):
    short = random_key()
    if 'url' in request.POST:
        valid = validate_url(request.POST.get('url'))
        if 'errors' not in valid:
            cache.add(short, valid)
    return render(request, 'index.html', locals())


# 2. Редирект
# 
# Функция обрабатывает сокращенный URL вида http://localhost:8000/наш_короткий_ключ
# (напишите регулярное выражение в urlpatterns).
# Ищем ключ в кеше (cache.get). Если ключ не найден, редиректим на главную страницу (/)
# Если найден, редиректим на полный URL, сохраненный под данным ключом.
# Для редиректа можете воспользоваться функцией django.shortcuts.redirect(redirect_to)

def redirect_view(request, key):
    url_path = cache.get(key)
    if not url_path:
        return redirect('/')
    return redirect(url_path)


urlpatterns = [
    url(r'^$', index),
    
    # http://localhost:8000/наш_короткий_ключ
    url(r'^(?P<key>[\w]+)$', redirect_view),
]

##### Конец задания. Дальше идет проверочный код, который вы не правите.
from django.test import SimpleTestCase


class UrlShortenerTest(SimpleTestCase):
    def test_index_get(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_index_post(self):
        response = self.client.post('/', {'url': 'http://example.com/'})
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/', {'url': 'mailto:admin@google.com'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'http')
        self.assertContains(response, 'https')
        self.assertContains(response, 'ftp')

    def test_redirect(self):
        response = self.client.get('/randomnonsense')
        self.assertRedirects(response, '/')


if __name__ == '__main__':
    import sys
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
