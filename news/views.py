from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives  # импортируем класс для создание объекта письма с html
from django.template.loader import render_to_string  # импортируем функцию, которая срендерит наш html в текст
# Create your views here.
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, news, article, Author, Category
from .forms import PostForm
from .filters import PostFilter
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from datetime import timedelta, datetime
from .tasks import send_notify_email
from django.core.cache import cache     # импортируем наш кэш


from django.contrib.auth.decorators import login_required

@login_required
def subscribe_me(request):  # add subscriber if not exists for category
    user = request.user
    cat_id = request.GET.get('cat_id', False)
    if cat_id:
        current_category = Category.objects.get(id=cat_id)
        if not current_category.subscribers.filter(id=user.id).exists():
            current_category.subscribers.add(user)
    return redirect('/')



class NewsList(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'posts.html'
    context_object_name = 'news'
    paginate_by = 10
    #printer.apply_async([5], countdown=5)
    queryset = Post.objects.filter(post_type=news)   # фильтр - новости
    extra_context = {'post_type': 'news'}


class NewsSearch(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'posts_search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class NewsDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'new'
    extra_context = {'post_type': 'news'}

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'news-{self.kwargs["pk"]}', None)  # кэш очень похож на словарь, и метод get действует так же.
        # Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'news-{self.kwargs["pk"]}', obj)
        return obj


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    extra_context = {'post_type': 'news'}
    success_url = reverse_lazy('news')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = news
        author = post.author
        end = datetime.now() + timedelta(days=-1)
        posts = author.post_set.filter(time_create__gt=end)

        if len(posts) >= 3:
            raise Exception('Запрещено более 3 постов в день!')
        else:
            super().form_valid(form)
            #post.save()
            send_notify_email.delay(post.id)    # Уведомление подписчикам о новом посте
            return redirect('/')


    # НЕ НУЖНО т.к. есть Сигналы
    # def post(self, request, *args, **kwargs):
    #     current_user = request.user
    #     current_author = Author.objects.get(user__id=current_user.id)
    #
    #     if not current_author:
    #         raise ValueError("User not in Authors")
    #
    #     post = Post(
    #         text=request.POST['text'],
    #         caption=request.POST['caption'],
    #         author=current_author,
    #     )
    #
    #     categories = request.POST.getlist('category')
    #
    #     post.save()
    #
    #     for cat in categories:
    #         curr_cat = Category.objects.get(id=cat)
    #         post.category.add(curr_cat)


        #   Отправляем простое письмо
        # send_mail(
        #     subject=f'Новая новость!',
        #     message='Краткое содержание ' + post.text,  # сообщение с кратким описанием проблемы
        #     from_email='info@vikingservice72.ru',  # здесь указываете почту, с которой будете отправлять
        #     recipient_list=['alexnv2011@gmail.com']  # здесь список получателей.
        # )

        # Отправка в HTML формате - не нужно т.к. есть Сигналы
        # получаем наш html
        # html_content = render_to_string('mail_news.html', {'post': post})
        # # в конструкторе уже знакомые нам параметры, да? Называются правда немного по-другому, но суть та же.
        # msg = EmailMultiAlternatives(
        #     subject=f'Привет, {post.author.user.username}! Новость на сайте!',
        #     body=post.text,  # это то же, что и message
        #     from_email='info@vikingservice72.ru',
        #     to=['alexnv2011@gmail.com'],  # это то же, что и recipients_list
        # )
        # msg.attach_alternative(html_content, "text/html")  # добавляем html
        # msg.send()  # отсылаем

        # return redirect('/')


class NewsEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    extra_context = {'post_type': 'news'}
    success_url = reverse_lazy('news')


# Представление, удаляющее пост.
class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'post_delete.html'
    extra_context = {'post_type': 'news'}
    success_url = reverse_lazy('news')



class ArticleList(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'posts.html'
    context_object_name = 'news'
    paginate_by = 10
    queryset = Post.objects.filter(post_type=article)   # фильтр - статьи


class ArticleDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'new'

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'articles-{self.kwargs["pk"]}', None)  # кэш очень похож на словарь, и метод get действует так же.
        # Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'articles-{self.kwargs["pk"]}', obj)
        return obj


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    success_url = reverse_lazy('articles')
    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = article
        author = post.author
        end = datetime.now() + timedelta(days=-1)
        posts = author.post_set.filter(time_create__gt=end)

        if len(posts) >= 3:
            raise Exception('Запрещено более 3 постов в день!')
        else:
            super().form_valid(form)
            send_notify_email.delay(post.id)    # Уведомление подписчикам о новом посте
            return redirect('/')

    # def post(self, request, *args, **kwargs):
    #     current_user = request.user
    #     current_author = Author.objects.filter(user__id=current_user.id)[0]
    #
    #     if not current_author:
    #         raise ValueError("User not in Authors")
    #     post = Post(
    #         text=request.POST['text'],
    #         caption=request.POST['caption'],
    #         author=current_author,
    #         post_type=article,
    #     )
    #     post.save()
    #
    #     # отправляем письмо - получаем наш html
    #     html_content = render_to_string(
    #         'mail_news.html',  {'post': post, })
    #     msg = EmailMultiAlternatives(
    #         subject=f'Привет, {post.author.user.username}! Статья на сайте!',
    #         body=post.text,  # это то же, что и message
    #         from_email='info@vikingservice72.ru',
    #         to=['alexnv2011@gmail.com'],  # это то же, что и recipients_list
    #     )
    #     msg.attach_alternative(html_content, "text/html")  # добавляем html
    #     msg.send()  # отсылаем
    #     return redirect('/articles')




class ArticleEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('articles')


# Представление, удаляющее пост.
class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('articles')

