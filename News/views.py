from django.shortcuts import get_object_or_404, reverse
from .models import Article, Comment
from django.utils import timezone
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin


# Функция для проверки наличия разрешения у пользователя на выполняемое действие
def has_rights(item, user):
    if not user.groups.filter(name="Moderator").exists() and \
            not user.is_superuser and user != item.Author:
        return False
    else:
        return True


class ArticleListView(ListView):
    queryset = Article.objects.order_by("-Date")[:20]
    template_name = "News/news.html"


class ArticleDetailView(TemplateView):
    template_name = 'News/post.html'

    def get_context_data(self, **kwargs):
        article  = get_object_or_404(Article, pk=kwargs['pk'])
        comments = Comment.objects.filter(article_id=article)
        context  = super().get_context_data(**kwargs)

        context['article']  = article
        context['comments'] = comments
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'News/post_new.html'

    def __init__(self, model, form_class):
        self.post_id    = None
        self.model      = model
        self.form_class = form_class

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.post_id})

    def form_valid(self, form):
        post        = form.save(commit=False)
        post.Author = self.request.user
        post.Date   = timezone.now()
        if self.model == Comment:
            self.post_id    = self.kwargs['pk']
            post.article_id = Article.objects.get(pk=self.post_id)
            post.save()
        else:
            post.save()
            self.post_id = post.id
        return super(PostCreateView, self).form_valid(form)


class PostEditView(LoginRequiredMixin, UpdateView):
    template_name = 'News/post_new.html'

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.kwargs['pk'])

    def get_success_url(self):
        if self.model == Comment:
            pk = Comment.objects.get(pk=self.kwargs['pk']).article_id.id
        else:
            pk = self.kwargs['pk']
        return reverse('post_detail', kwargs={'pk': pk})

    def get_template_names(self):
        if not has_rights(self.model.objects.get(pk=self.kwargs['pk']), self.request.user):
            return 'News/forbidden.html'
        else:
            return self.template_name

    def form_valid(self, form):
        post = form.save(commit=False)
        post.Author = self.request.user
        post.Date = timezone.now()
        post.save()
        return super(PostEditView, self).form_valid(form)


class PostDeleteView(LoginRequiredMixin, DeleteView):

    def __init__(self, model):
        self.pk    = None
        self.model = model

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        if self.model == Comment:
            return reverse('post_detail', kwargs={'pk': self.pk})
        else:
            return reverse('News_page')

    def get_template_names(self):
        if not has_rights(self.model.objects.get(pk=self.kwargs['pk']), self.request.user):
            return 'News/forbidden.html'
        else:
            return self.template_name

    def get_object(self, queryset=None):
        if self.model == Comment:
            self.pk = Comment.objects.get(pk=self.kwargs['pk']).article_id.id
        return self.model.objects.get(pk=self.kwargs['pk'])
