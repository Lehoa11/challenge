from django.shortcuts import render
from django.views import View
from .models import Post ,Comment
from .forms import PostForm ,CommentForm
from django.http import HttpResponseRedirect

class PostListView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_on')
        form  = PostForm()

        context = {
            'post_list': posts,
            "form" :form,
           
        }

        return render(request, 'social/post_list.html', context)
    

    def post(self,request,*args,**kwargs):
        posts = Post.objects.all().order_by("-created_on")
        form = PostForm(request.POST)

        if form.is_valid():
            new_pots = form.save(commit=False)
            new_pots.author = request.user
            new_pots.save()

            context = {
            'post_list': posts,
            "form" :form,
           
        }

        return render(request, 'social/post_list.html', context)
    
   
class PostDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm()
        comments = Comment.objects.filter(post=post).order_by('-created_on')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }

        return render(request, 'social/post_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
        
        comments = Comment.objects.filter(post=post).order_by('-created_on')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }

        return render(request, 'social/post_detail.html', context)
    
class AddLike( View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

      

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            post.likes.add(request.user)

        if is_like:
            post.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

