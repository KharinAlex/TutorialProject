from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostNewArticle, PostComment
from .models import Article, Comment
from django.utils import timezone


def post_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'GET':
        comments = Comment.objects.filter(article_id=pk)
        return render(request, 'News/post.html', {'article': article, 'comments': comments})
    
    
def post_new(request):
    if request.method == 'POST':
        form = PostNewArticle(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.Author = request.user
            post.Date = timezone.now()
            post.save()
            return redirect('<slug:pk>', post.id)
    else:
        form = PostNewArticle()
    return render(request, 'News/post_new.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = PostNewArticle(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.Author = request.user
            post.Date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.id)
    else:
        form = PostNewArticle(instance=post)
    return render(request, 'News/post_new.html', {'form': form})


def post_delete(request, pk):
    post = get_object_or_404(Article, pk=pk)
    post.delete()
    return redirect('News_page')


def post_comment(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = PostComment(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article_id = article
            comment.Author = request.user
            comment.Date = timezone.now()
            comment.save()
            return redirect('post_detail', pk=pk)
    else:
        form = PostComment()
    return render(request, 'News/post_new.html', {'form': form})


def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        form = PostComment(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.Author = request.user
            comment.Date = timezone.now()
            comment.save()
            return redirect('post_detail', pk=comment.article_id.id)
    else:
        form = PostComment(instance=comment)
    return render(request, 'News/post_new.html', {'form': form})


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    article_id = comment.article_id.id
    comment.delete()
    return redirect('post_detail', pk=article_id)
