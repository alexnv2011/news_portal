from celery import shared_task
from .models import Post, news, Category
from django.core.mail import send_mail
import time


# Уведомление о новой статье
@shared_task
def send_notify_email(post_id):
    time.sleep(20)
    print('id = ' + str(post_id))
    post = Post.objects.get(id=post_id)
    categories = post.category.all()
    if post.post_type == news:
        capt = 'новость'
        urlp = 'news'
    else:
        capt = 'статья'
        urlp = 'articles'
    recipient_list = []

    for cat in categories:   # цикл по категориям поста
        scrbs = cat.subscribers.all()  # Подписчики категории
        for scrb in scrbs:   # цикл по подписчикам
            if scrb.email and not (scrb.email in recipient_list):
                recipient_list.append(scrb.email)   #- добавление почты

    print('recipient_list = ' + str(recipient_list))

    #  Отправляем простое письмо
    send_mail(
        subject=f'Новая {capt} на сайте!',
        message='Краткое содержание: ' + post.text[0:200] + '\n' + f'Читать: http://127.0.0.1:8000/{urlp}/{str(post_id)}',
        # сообщение с кратким описанием
        from_email='info@vikingservice72.ru',  # здесь указываете почту, с которой будете отправлять
        recipient_list=recipient_list  # здесь список получателей.
    )



