from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from taggit.models import Tag

from .forms import CommentForm, PostForm
from .models import Follow, Post, User


class PostListView(ListView):
    """
    Альтернативное представление для отображения постов.
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_list(request, tag_slug=None):
    """
    Альтернативное представление для отображения постов.
    """
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(
            Tag,
            slug=tag_slug
        )
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(
        request,
        'blog/post/list.html',
        {
            'posts': posts,
            'tag': tag,
            'section': 'post_list'
        }
    )


def post_detail(request, year, month, day, post):
    """
    Представления для отображения отдельного поста.
    """
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    comments = post.comments.filter(active=True)
    form = CommentForm()
    token = request.GET.get('token')
    if not post.is_hidden or str(post.secret_key) == token:
        return render(
            request,
            'blog/post/detail.html',
            {
                'post': post,
                'comments': comments,
                'form': form
            }
        )
    return HttpResponseForbidden('Этот пост доступен только по запросу')


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(
        request,
        'blog/post/comment.html',
        {
            'post': post,
            'form': form,
            'comment': comment
        }
    )


@login_required
def post_create(request):
    template = 'blog/post/create_post.html'
    form = PostForm(request.POST or None)
    context = {
        'form': form,
        'section': 'create'
    }
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect(f'/blog/profile/{post.author.username}/')
    return render(request, template, context)


@login_required
def post_edit(request, year, month, day, post):
    template = 'blog/post/create_post.html'
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    context = {
        'form': form,
        'post': post,
        'is_edit': True,
    }
    if request.user == post.author and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect(f'/blog/{post.publish.year}/{post.publish.month}/{post.publish.day}/{post.slug}')
    return render(request, template, context)


@login_required
def post_delete(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    if request.method == 'POST':
        post.delete()
        return redirect('blog:post_list')
    return render(
        request,
        'blog/post/post_delete_confirm.html',
        {'post': post}
    )


def profile(request, username):
    template = 'blog/post/profile.html'
    user = request.user
    author = get_object_or_404(User, username=username)
    following = (
        user.is_authenticated
        and Follow.objects.filter(user=user, author=author)
    )
    post_list = author.posts.all().order_by('author')
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    post_number = post_list.count()
    context = {
        'page_obj': page_obj,
        'post_number': post_number,
        'author': author,
        'following': following,
    }
    return render(request, template, context)


@login_required
def follow_index(request):
    """Выводит посты авторов, на которых
       подписан текущий пользователь."""
    template = 'blog/post/follow.html'
    user = request.user
    post_list = Post.objects.filter(
        author__following__user=user
    )
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'section': 'follow'
    }
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    """Делает подписку на автора."""
    user = request.user
    author = get_object_or_404(User, username=username)
    if author != user:
        user.follower.get_or_create(
            user=user,
            author=author
        )
    return redirect('blog:profile', username)


@login_required
def profile_unfollow(request, username):
    """Отписывает пользователя от автора."""
    user = request.user
    author = get_object_or_404(User, username=username)
    follow = Follow.objects.filter(
        user=user,
        author=author
    )
    if follow.exists():
        follow.delete()
    return redirect('blog:profile', username)
