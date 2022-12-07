from django.core.management.base import BaseCommand, CommandError
from news.models import Category, Post


class Command(BaseCommand):
    help = 'Удаление всех новостей категории'  # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    missing_args_message = 'Недостаточно аргументов'
    requires_migrations_checks = True  # напоминать ли о миграциях. Если true — то будет напоминание о том, что не сделаны все миграции (если такие есть)

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('category', type=str)    # --argument=...

    def handle(self, *args, **options):
        answer = input(f'Do you really want to delete all posts in category {options["category"]}? yes/no ')  # считываем подтверждение
        category_del = options['category']
        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))
            return

        try:
            category = Category.objects.get(name=category_del)
            Post.objects.filter(category=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Succesfully deleted all news from category {category.name}'))
        except:
           self.stdout.write(self.style.ERROR(f'Could not find category {category_del}'))



