from django_filters import FilterSet
from .models import Post

# Создаем свой набор фильтров для модели Post.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
   # release_year__gt = django_filters.NumberFilter(field_name='release_date', lookup_expr='year__gt')
   class Meta:
       model = Post
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
       fields = {
           # поиск по названию
           'caption': ['icontains'],
           'text': ['icontains'],
           'time_create': ['gt'],
           # # количество товаров должно быть больше или равно
           # 'quantity': ['gt'],
           # 'price': [
           #     'lt',  # цена должна быть меньше или равна указанной
           #     'gt',  # цена должна быть больше или равна указанной
           # ],
       }