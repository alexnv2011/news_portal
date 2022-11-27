from django.db.models.signals import m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from .models import Post, Category
from django.core.mail import send_mail


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(m2m_changed, sender=Post.category.through)
def notify_create_news(sender, instance, **kwargs):

    subject = f' Новая новость/ статья {instance.time_create.strftime("%d %m %Y")}'

    # Получение подписчиков категории
    recipients = []
    for cat in instance.category.all():
        for subs in cat.subscribers.all():
            if not (subs.email in recipients) and subs.email:
                recipients.append(subs.email)

    send_mail(
         subject=subject,
         message='Краткое содержание ' + instance.text,  # сообщение с кратким описанием проблемы
         from_email='info@vikingservice72.ru',  # здесь указываете почту, с которой будете отправлять
         recipient_list=recipients  # здесь список получателей.
    )


# m2m_changed.connect(notify_create_news, sender=Post.category.through)




