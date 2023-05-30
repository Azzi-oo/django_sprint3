from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Category, Post


def index(request):
    template = 'blog/index.html'
    posts = Post.objects.select_related(
        'category',
        'location',
        'author'
    ).filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    )[0:5]
    context = {'posts': posts}
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    posts = get_object_or_404(Post.objects.select_related(
        'location', 'category', 'author').filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True,
    ),
        pk=id
    )
    context = {'post': posts}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True)
    posts = Post.objects.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category=category
    )
    context = {'category': category, 'posts': posts}
    return render(request, template, context)
