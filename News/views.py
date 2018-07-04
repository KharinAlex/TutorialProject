from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostNewArticle, PostComment
from .models import Article, Comment
from django.utils import timezone


# Обработчик для отображения страницы со статьей
def post_detail(request, pk):
    # Получаем объект статьи по id
    article = get_object_or_404(Article, pk=pk)
    # Выполняем выборку комментариев, которые относятся к отображаемой статье
    comments = Comment.objects.filter(article_id=pk)
    # Отображаем страницу, передавая ей объект статьи и QuerySet из комментариев
    return render(request, 'News/post.html', {'article': article, 'comments': comments})


# Обработчик для добавления в БД новой статьи
def post_new(request):
    # Проверка на тип полученного запроса
    if request.method == 'POST':
        # Создаем новую форму и заполняем ее параметрами из HTTP запроса
        form = PostNewArticle(request.POST)
        # Проверка на валидность
        if form.is_valid():
            # Сохраняем данные из формы, но не вносим БД, поскольку не все поля сущности заполнялись из формы
            post = form.save(commit=False)
            # Заполняем остальные поля сущности
            post.Author = request.user
            post.Date = timezone.now()
            # Сохраняем статью в БД
            post.save()
            # Переход на персональную ссылку для только-что созданной статьи
            return redirect('post_detail', post.id)
    else:
        # Если пришел GET запрос - создаем пустую форму
        form = PostNewArticle()
    # Отрисовка формы на странице
    return render(request, 'News/post_new.html', {'form': form})


# Обработчик для редактирования статьи
def post_edit(request, pk):
    # Получаем объект статьи по id
    post = get_object_or_404(Article, pk=pk)
    # Если пришел POST запрос - сохраняем внесенные изменения
    if request.method == 'POST':
        # Создаем форму на базе существующего объекта и изменяем его содержимое значениями из запроса
        form = PostNewArticle(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.Author = request.user
            post.Date = timezone.now()
            post.save()
            # Переход на отредактированную статью
            return redirect('post_detail', pk=post.id)
    else:
        # Если пришел GET запрос - создаем форму с текущим содержанием статьи
        form = PostNewArticle(instance=post)
    # Отрисовка формы на странице
    return render(request, 'News/post_new.html', {'form': form})


# Обработчик для удаления статьи
def post_delete(request, pk):
    post = get_object_or_404(Article, pk=pk)
    post.delete()
    # Переход на стартовую новостную страницу
    return redirect('News_page')


# Обработчик для добавления комментария
def post_comment(request, pk):
    # Получаем объект статьи по id, к которой будет относиться комментарий
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = PostComment(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            # Заполняем поле ключа, в качестве которого выступает статья
            comment.article_id = article
            comment.Author = request.user
            comment.Date = timezone.now()
            comment.save()
            # Переход на страницу со статьей и комментариями
            return redirect('post_detail', pk=pk)
    else:
        form = PostComment()
    return render(request, 'News/post_new.html', {'form': form})


# Обработчик для редактирования комментария
def edit_comment(request, pk):
    # Получаем объект комментария по id
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        form = PostComment(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.Author = request.user
            comment.Date = timezone.now()
            comment.save()
            # Переход на страницу со статьей и комментариями
            return redirect('post_detail', pk=comment.article_id.id)
    else:
        form = PostComment(instance=comment)
    return render(request, 'News/post_new.html', {'form': form})


# Обработчик для удаления комментария
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    article_id = comment.article_id.id
    comment.delete()
    # Переход на страницу со статьей и комментариями
    return redirect('post_detail', pk=article_id)
