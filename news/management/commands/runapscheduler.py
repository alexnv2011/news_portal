# Отмена, реализовано на Celery

# import logging
# from django.contrib.auth.models import User
# from django.conf import settings
# from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.triggers.cron import CronTrigger
# from django.core.management.base import BaseCommand
# from django_apscheduler.jobstores import DjangoJobStore
# from django_apscheduler.models import DjangoJobExecution
# from django.core.mail import send_mail
# from datetime import timedelta, datetime
# from ...models import Post, news
#
# logger = logging.getLogger(__name__)
#
#
#
# # наша задача по выводу текста на экран
# def my_job():
#     #  Your job processing logic here...
#     print('hello from job')
#
#
# # функция, которая будет удалять неактуальные задачи
# def delete_old_job_executions(max_age=604_800):
#     """This job deletes all apscheduler job executions older than `max_age` from the database."""
#     DjangoJobExecution.objects.delete_old_job_executions(max_age)
#
#
# # отправка новых статей подписчикам за неделю
# def send_news_to_subscribers():
#     subject = ' Новости за неделю'
#
#     end = datetime.now() + timedelta(days=-7)
#
#     # список пользователей (подписчиков)
#     scrbs = User.objects.all()
#
#     for scr in scrbs:   # цикл по людям
#         mes = ''
#         print('Subscriber', str(scr))
#         cats = scr.category_set.all()     # категории на которые подписан человек
#         if len(cats) > 0:
#             for cat in cats:    # цикл по категориям
#                 mes += 'Категория: ' + cat.name + '\n'
#                 print(cat)
#                 posts = cat.post_set.filter(time_create__gt=end)     # посты категории за неделю
#                 for post in posts:
#                     if post.post_type == news:
#                         mes += ' - ' + post.caption[0:10] + '  http://127.0.0.1:8000/news/' + str(post.id) + '\n'
#                     else:
#                         mes += ' - ' + post.caption[0:10] + '  http://127.0.0.1:8000/articles/' + str(post.id) + '\n'
#         if scr.email and mes:
#             send_mail(
#                 subject=subject,
#                 message=mes,  # сообщение
#                 from_email='info@vikingservice72.ru',  # здесь указываете почту, с которой будете отправлять
#                 recipient_list=[scr.email]    # список получателей.
#             )
#
#
#
# class Command(BaseCommand):
#     help = "Runs apscheduler."
#
#     def handle(self, *args, **options):
#         scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
#         scheduler.add_jobstore(DjangoJobStore(), "default")
#
#         # добавляем работу нашему задачнику
#         scheduler.add_job(
#             my_job,
#             trigger=CronTrigger(minute="*/1"),
#             # То же, что и интервал, но задача тригера таким образом более понятна django
#             id="my_job",  # уникальный айди
#             max_instances=1,
#             replace_existing=True,
#         )
#         logger.info("Added job 'my_job'.")
#
#
#         scheduler.add_job(
#             send_news_to_subscribers,
#             trigger=CronTrigger(
#                 day_of_week="mon", hour="23", minute="44"
#             ),
#             # Каждую неделю рассылка по подписчикам с новыми постами.
#             id="send_news_to_subscribers",
#             max_instances=1,
#             replace_existing=True,
#         )
#         logger.info(
#             "Added weekly job: 'send_news_to_subscribers'."
#         )
#
#
#         scheduler.add_job(
#             delete_old_job_executions,
#             trigger=CronTrigger(
#                 day_of_week="mon", hour="00", minute="00"
#             ),
#             # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
#             id="delete_old_job_executions",
#             max_instances=1,
#             replace_existing=True,
#         )
#         logger.info(
#             "Added weekly job: 'delete_old_job_executions'."
#         )
#
#         try:
#             logger.info("Starting scheduler...")
#             scheduler.start()
#         except KeyboardInterrupt:
#             logger.info("Stopping scheduler...")
#             scheduler.shutdown()
#             logger.info("Scheduler shut down successfully!")
#
#
