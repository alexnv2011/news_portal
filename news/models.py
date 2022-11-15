from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

news = 'NE'
article = 'AR'

TYPES = [
    (news, 'Новость'),
    (article, 'Статья')
]


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

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





