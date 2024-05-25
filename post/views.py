from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.db.models import Count
from . import models
from .forms import PostCommentForm


class HomeView(ListView):
    queryset = models.Post.objects.filter(status='publish').order_by('-create_date')
    template_name = 'post/home.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_posts'] = models.Post.objects.annotate(vw=Count('views')).order_by('-vw')[:3]
        context['popular_tags'] = models. Tag.objects.annotate(tg=Count('posts')).order_by('-tg')[:10]
        return context


class PostView(View):
    def get(self, request, slug):
        post = get_object_or_404(models.Post, slug=slug)
        related_posts = models.Post.objects.filter(tags__in=post.tags.all()).exclude(id=post.id)[:4]
        comments = models.Comment.objects.filter(post=post)
        comment_form = PostCommentForm()

        ip_address = request.user.ip_address
        if ip_address not in post.views.all():
            post.views.add(ip_address)
        context = {
            'post': post,
            'comments': comments,
            'form': comment_form,
            'related_posts': related_posts,
        }
        return render(request, 'post/post.html', context)

    def post(self, request, slug):
        form = PostCommentForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.post = get_object_or_404(models.Post, slug=slug)  # must optimize (two same query in get and post)
            if request.user.is_authenticated:
                obj.user = request.user
            parent_id = request.POST.get('reply')
            if parent_id:
                obj.parent = models.Comment.objects.get(id=parent_id)
            obj.save()
        return HttpResponseRedirect(self.request.path_info)


class CategoryPageView(View):
    def get(self, request, slug, page=1):
        category = get_object_or_404(models.Category, slug=slug)
        posts_list = models.Post.objects.filter(category=category, status='publish').order_by('-create_date')
        paginator = Paginator(posts_list, 4)
        posts = paginator.get_page(page)
        context = {
            'posts': posts,
            'paginator': paginator,
            'category': category,
        }
        return render(request, 'post/category.html', context)


class TagPageView(View):
    def get(self, request, slug, page=1):
        tag = get_object_or_404(models.Tag, slug=slug)
        posts_list = models.Post.objects.filter(tags=tag, status='publish').order_by('-create_date')
        paginator = Paginator(posts_list, 4)
        posts = paginator.get_page(page)
        context = {
            'posts': posts,
            'paginator': paginator,
            'tag': tag,
        }
        return render(request, 'post/tag.html', context)
