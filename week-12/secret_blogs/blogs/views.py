from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from blogs.forms import BlogForm
from django.core.exceptions import PermissionDenied
from django import views
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from blogs.models import Blog


def is_my_blog(user, author):
    if user == author:
        return True
    return False


class BlogListView(PermissionRequiredMixin, LoginRequiredMixin, views.View):
    login_url = '/authen/'
    permission_required = ["blogs.view_blog"]
    permission_denied_message = "Nuh uh"
    def get(self, request: HttpRequest):
        blog_qs = Blog.objects.all()
        context = {
            "blogs": blog_qs
        }
        return render(request, 'blog_list.html', context)


class BlogDetailView(PermissionRequiredMixin, LoginRequiredMixin, views.View):
    login_url = '/authen/'
    permission_required = ["blogs.view_blog"]
    permission_denied_message = "Nuh uh"
    def get(self, request: HttpRequest, pk):
        blog = get_object_or_404(Blog, pk=pk)
        form = BlogForm(instance=blog)
        context = {
            "blog": blog,
            "form": form
        }
        return render(request, "blog_detail.html", context)
    

class BlogCreateView(PermissionRequiredMixin, LoginRequiredMixin, views.View):
    login_url = '/authen/'
    permission_required = ["blogs.add_blog"]
    permission_denied_message = "Nuh uh"
    def get(self, request: HttpRequest):
        form = BlogForm()
        context = {
            "form": form
        }
        return render(request, 'blog_create.html', context)
    
    def post(self, request: HttpRequest):
        form = BlogForm(request.POST)
        
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            form.save_m2m()
            return redirect('blog-list')
        else:
            return render(request, "blog_create.html", {"form": form})
            

class BlogEditView(PermissionRequiredMixin, LoginRequiredMixin, views.View):
    login_url = '/authen/'
    permission_required = ["blogs.change_blog"]
    permission_denied_message = "Nuh uh"
    def post(self, request: HttpRequest, pk):
        blog = get_object_or_404(Blog, pk=pk)
        
        if not is_my_blog(request.user, blog.author):
            raise PermissionDenied("Only for the blog owner.")
        
        form = BlogForm(request.POST, instance=blog)
        
        if form.is_valid():
            form.save()
            return redirect('blog-detail', pk=blog.id)
        else:
            context = {
                "blog": blog,
                "form": form  
            }
            return render(request, "blog_detail.html", context)
        
       
class BlogDeleteView(PermissionRequiredMixin, LoginRequiredMixin, views.View):
    login_url = '/authen/'
    permission_required = ["blogs.delete_blog"]
    permission_denied_message = "Nuh uh"
    def get(self, request: HttpRequest, pk):
        blog = get_object_or_404(Blog, pk=pk)
        
        if not is_my_blog(request.user, blog.author):
            if not request.user.is_staff:
                raise PermissionDenied("Only for the blog owner.")

        blog.delete()
        return redirect('blog-list')
        