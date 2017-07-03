from django.conf import settings
from django.conf.urls import url
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseBadRequest

# Задание 3. Django: urlpatterns и views
#
# Напишите реализации объявленных ниже функций.
# Для проверки корректности реализации ваших функций,
# запустите этот файл на выполнение:
#
# python homework3.py test homework3
#
# (последний аргумент - это указание, где искать тесты - в текущем модуле)
# Также вы можете запустить сервер для разработки, и посмотреть
# ответы ваших функций в браузере:
#
# python homework3.py runserver


# Конфигурация, не редактировать
if not settings.configured:
    settings.configure(
        DEBUG=True,
        ROOT_URLCONF=__name__
    )


# 1. GET
# Реализуйте регулярное выражение и функцию-обработчик для таких URL:
#
# /get
# /get?a=1&b=2
#
# При выполнении запроса на этот URL, функция должна проверять HTTP метод.
# Если это 'GET', функция возвращает JSON с соответствующим Content-type,
# содержащий GET-параметры (часть URL после ?, например /get?a=1&b=2)
# Если метод запроса не 'GET', должен вернуться HTTP ответ 400 - Bad Request.
# Для реализации ответов воспользуйтесь подходящими подклассами HttpResponse.

def get(request):
    if request.method == 'GET':            
        response = JsonResponse(request.GET)
        return response
    else:
        return HttpResponseBadRequest()


# 2. HTTP заголовки (headers).
# Реализуйте регулярное выражение и функцию-обработчик для такого URL:
#
# /headers/
# /headers/<начало имени заголовка>
#
# При выполнении запроса на первую форму URL, функция возвращает JSON
# с соответствующим Content-type ('application/json'), содержащий
# HTTP заголовки - содержимое request.META, с ключами, начинающимися с 'HTTP_'.
#
# При выполнении запроса на вторую форму URL, функция возвращает JSON
# содержащий HTTP заголовки из request.META, начинающиеся c 'HTTP_' плюс указанный
# в URL фрагмент (часть URL после /headers/).
#
# Пример URL: /headers/HOST
# Ответ: { "HTTP_HOST": "localhost:8000" }

def headers(request, **kwargs):
    res = {}
    res1 = {}
    for key, val in request.META.items():
        if 'HTTP_' in key:
            res[key] = request.META[key]
    if not kwargs:        
        response = JsonResponse(res)
    else:
        for key, val in request.META.items():
            if kwargs['name'] in key:
                res1[key] = request.META[key]
        response = JsonResponse(res1)
    return response


# 3. Редиректы
# Реализуйте регулярное выражение в urlpatterns и функцию-обработчик для такого URL:
#
# /redirect/<к-во редиректов>/<счетчик>
#
# При вызове
#
# /redirect/10/0
#
# или
#
# /redirect/10/
#
# (сделайте так, чтобы при нулевом значении счетчика его можно было бы не указывать)
# должен происходить редирект c кодом 302 на URL
#
# /redirect/9/1
#
# то есть значение количества редиректов должно уменьшаться на 1,
# а счетчик соответственно увеличиваться. При достижении 0
# для количества редиректов, то есть при редиректе на URL
#
# /redirect/0/10
#
# функция должна вернуть стандартный HTTP ответ c кодом 200,
# типом (Сontent-type) 'text/plain'. В теле ответа должно быть
# значение счетчика, т.е. в нашем примере - '10'
#
# Поэкспериментируйте в браузере. При каком количестве редиректов он выдает ошибку?

def redirect(request, **kwargs):
    n = int(kwargs['n'])    

    if 'count' not in kwargs:
        count = 0
    else:
        count = int(kwargs['count'])

    while n != 0:
        n -= 1
        count += 1 
        return HttpResponseRedirect('/redirect/' + str(n) + '/' + str(count)) 

    return HttpResponse(count)  

urlpatterns = [
    # get
    # get?a=1&b=2
    url(r'^get', get),

    # headers/
    # headers/HOST
    url(r'^headers/$', headers),
    url(r'^headers/(?P<name>[\w]+)$', headers),

    # redirect/10
    # redirect/5/5
    url(r'redirect/(?P<n>[\d]+)$', redirect),
    url(r'redirect/(?P<n>[\d]+)/(?P<count>[\d]+)$', redirect),
]

##### Конец задания. Дальше идет проверочный код, который вы не правите.


from django.test import SimpleTestCase

class Homework3Test(SimpleTestCase):
    def test_get(self):
        params = {'a': '1', 'b': '2'}
        response = self.client.get('/get', params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertJSONEqual(str(response.content, encoding='utf8'), params)
        response = self.client.post('/get', params)
        self.assertEqual(response.status_code, 400)

    def test_headers(self):
        response = self.client.get('/headers/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        headers = {'HTTP_USER_AGENT': 'r2d2'}
        response = self.client.get('/headers/USER_AGENT', **headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertJSONEqual(str(response.content, encoding='utf8'), headers)

    def test_redirect(self):
        response = self.client.get('/redirect/10')
        self.assertRedirects(response, '/redirect/9/1', target_status_code=302)
        response = self.client.get('/redirect/0/10')
        self.assertContains(response, '10')


if __name__ == '__main__':
    import sys
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
