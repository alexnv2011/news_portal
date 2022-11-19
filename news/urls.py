from django.urls import path
# Импортируем созданное нами представление
from .views import NewsList, NewsDetail, NewsCreate, NewsEdit, NewsDelete,\
   ArticleList, ArticleDetail, ArticleCreate, ArticleEdit, ArticleDelete, NewsSearch


urlpatterns = [
   path('',                 NewsList.as_view(), name='news'),
   path('search/',               NewsSearch.as_view()),
   path('news/<int:pk>',         NewsDetail.as_view()),
   path('news/create/',          NewsCreate.as_view(),   name='post_create'),
   path('news/<int:pk>/edit/',   NewsEdit.as_view(),     name='post_edit'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(),   name='post_delete'),
   path('articles/',                ArticleList.as_view(), name='articles'),
   path('articles/<int:pk>',        ArticleDetail.as_view()),
   path('articles/create/',         ArticleCreate.as_view(),   name='post_create'),
   path('articles/<int:pk>/edit/',  ArticleEdit.as_view(),     name='post_edit'),
   path('articles/<int:pk>/delete/', ArticleDelete.as_view(),  name='post_delete'),
]