from django.shortcuts import render

# Create your views here.
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, news, article
from .forms import PostForm
from .filters import PostFilter


class NewsList(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'posts.html'
    context_object_name = 'news'
    paginate_by = 10
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

class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    extra_context = {'post_type': 'news'}
    success_url = reverse_lazy('news')
    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = news
        return super().form_valid(form)

class NewsEdit(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    extra_context = {'post_type': 'news'}
    success_url = reverse_lazy('news')


# Представление, удаляющее пост.
class NewsDelete(DeleteView):
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


class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    success_url = reverse_lazy('articles')
    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = article
        return super().form_valid(form)


class ArticleEdit(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('articles')


# Представление, удаляющее пост.
class ArticleDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('articles')

