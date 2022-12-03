from django.db import models
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.models import User
from django.core.cache import cache


news = 'NE'
article = 'AR'

TYPES = [
    (news, 'Новость'),
    (article, 'Статья')
]


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through='CategorySubscriber')
    def __str__(self):
        return self.name


class CategorySubscriber(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Author(models.Model):
    rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def count_today(self):
        return 2

    def __str__(self):
        return self.user.username

    def update_rating(self):
        self.rating = 0
           # суммарный рейтинг комментариев автора (пользователя)
        for i in self.user.comment_set.all():
            self.rating += i.rating

            # суммарный рейтинг постов автора
        for i in self.post_set.all():
            self.rating += 3 * i.rating

         # суммарный рейтинг комментариев к постам автора
        for i in Comment.objects.filter(post__author__id=self.id):
            self.rating += i.rating


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.TextField(max_length=2, choices=TYPES, default=news)
    time_create = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    caption = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0, db_column='rating')

    def get_absolute_url(self):
        return reverse('articles', args=[str(self.id)])

    @property
    def preview(self):
        return self.text[:125] + "..."

    def __str__(self):
        return self.caption[:125] + '.... | ' + self.preview

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)   # сначала вызываем метод родителя, чтобы объект сохранился
        if self.post_type == news:
            cache.delete(f'news-{self.pk}')     # затем удаляем его из кэша, чтобы сбросить его
        else:
            cache.delete(f'articles-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его

class Comment(models.Model):
    text = models.TextField()
    rating = models.IntegerField(default=0, db_column='rating')
    time_create = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return self.text[:125] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)





