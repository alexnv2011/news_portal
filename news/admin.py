from django.contrib import admin
from .models import Category, Post, Author, Comment
from modeltranslation.admin import TranslationAdmin # импортируем модель амдинки (вспоминаем модуль про переопределение стандартных админ-инструментов)


class PostAdmin(admin.ModelAdmin):
    # list_display = [field.name for field in Post._meta.get_fields()]  # генерируем список имён всех полей
    list_display = ['caption', 'post_type', 'author', 'time_create', 'rating' ]
    list_filter = ('post_type', 'author', 'rating')  # добавляем фильтры в нашу админку
    search_fields = ('text', 'text')     # тут всё очень похоже на фильтры из запросов в базу


def update_ratings(modeladmin, request, queryset):  # request — объект хранящий информацию о запросе и queryset
    # — набор объектов, которых мы выделили галочками.
    print(queryset)
    for au in queryset:
        print(au)
        au.update_rating()
    update_ratings.short_description = 'Обновить рейтинг'


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'posts', 'comments', 'rating']
    actions = [update_ratings]  # добавляем действия в список


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'count_posts']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'rating']


# Регистрируем модели для перевода в админке
class CategoryAdmin1(TranslationAdmin):
    model = Category


class PostAdmin1(TranslationAdmin):
    model = Post

class CommentAdmin1(TranslationAdmin):
    model = Comment


# admin.site.register(Post)
# admin.site.register(Category)
# admin.site.register(Comment)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Comment, CommentAdmin)


