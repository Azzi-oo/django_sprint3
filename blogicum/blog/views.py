from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.utils import timezone
from .models import Category, Post
from django.db.models import Q

datenow = timezone.now()


def index(request):
    post_list = Post.objects.select_related(
        'category',
        'location',
        'author'
    ).filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    ).order_by(
        '-pub_date',
        'title',
    )[:5]
    context = {'post_list': post_list}
    return render(request, 'blog/index.html', context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post_list = get_object_or_404(Post.objects.select_related(
        'location', 'category', 'author').filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True,
    ),
        pk=id
    )
    context = {'post': post_list}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category.objects.values(
            'title',
            'description',
        ).filter(
            slug=category_slug,
            is_published=True
        )
    )
    post_list = get_list_or_404(
        Post.objects.select_related(
            'category',
        ).filter(
            Q(category__slug=category_slug)
            & Q(is_published=True)
            & Q(pub_date__lte=datenow)
        ),
        category__is_published=True
    )
    context = {'category': category, 'post_list': post_list}
    return render(request, template, context)
