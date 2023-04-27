from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, BlogPostForm
from django.views.generic import UpdateView
from django.contrib import messages
from rest_framework import generics
from rest_framework import viewsets,status
from .serializers import BlogPostSerializer, CommentSerializer, UserProfileSerializer,LoginSerializer,RegistrationSerializer
from .models import BlogPost, Comment , UserProfile
from rest_framework.views import APIView
from rest_framework.response import Response
from  django.shortcuts import get_object_or_404
from .models import BlogPost
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpRequest, JsonResponse
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import LoginSerializer
from rest_framework import viewsets, permissions
from .models import BlogPost
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import generics, permissions
from .models import BlogPost
from .serializers import BlogPostSerializer
from rest_framework import viewsets, permissions
from .serializers import BlogPostSerializer
from .models import BlogPost
from rest_framework import viewsets, permissions
from .models import BlogPost
from .serializers import BlogPostSerializer
from Blog.config import ROLE_CHOICES
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets, permissions
from .models import BlogPost
from .serializers import BlogPostSerializer

def blogs(request):
    posts = BlogPost.objects.all()
    posts = BlogPost.objects.filter().order_by('-dateTime')
    return render(request, "blog.html", {'posts':posts})

def blogs_comments(request, slug):
    post = BlogPost.objects.filter(slug=slug).first()
    comments = Comment.objects.filter(blog=post)
    if request.method=="POST":
        user = request.user
        content = request.POST.get('content','')
        blog_id =request.POST.get('blog_id','')
        comment = Comment(user = user, content = content, blog=post)
        comment.save()
    return render(request, "blog_comments.html", {'post':post, 'comments':comments})

def Delete_Blog_Post(request, slug):
    posts = BlogPost.objects.get(slug=slug)
    if request.method == "POST":
        posts.delete()
        return redirect('/')
    return render(request, 'delete_blog_post.html', {'posts':posts})

def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        blogs = BlogPost.objects.filter(title__contains=searched)
        return render(request, "search.html", {'searched':searched, 'blogs':blogs})
    else:
        return render(request, "search.html", {})

@login_required(login_url = '/login')
def add_blogs(request):
    if request.method=="POST":
        form = BlogPostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            blogpost = form.save(commit=False)
            blogpost.author = request.user
            blogpost.save()
            obj = form.instance
            alert = True
            return render(request, "add_blogs.html",{'obj':obj, 'alert':alert})
    else:
        form=BlogPostForm()
    return render(request, "add_blogs.html", {'form':form})

class UpdatePostView(UpdateView):
    model = BlogPost
    template_name = 'edit_blog_post.html'
    fields = ['title', 'slug', 'content','image']


def user_profile(request, myid):
    post = BlogPost.objects.filter(id=myid)
    return render(request, "user_profile.html", {'post':post})

def Profile(request):
    return render(request, "profile.html")


def Register(request):
    if request.method=="POST":   
        username = request.POST['username']
        email = request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('/register')
        
        user = User.objects.create_user(username=username, email=email, password=password1, first_name=first_name,last_name=last_name)
        user.save()
        return render(request, 'login.html')   
    return render(request, "register.html")

def Login(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/")
        else:
            messages.error(request, "Invalid Credentials")
        return render(request, 'blog.html')   
    return render(request, "login.html")

def Logout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/login')

#API

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @login_required
    def blog_list(request):
        user = request.user
        if user.is_authenticated:
            if user.is_superuser or user.groups.filter(name='admin').exists():
                # show all blog posts to superusers and admins
                queryset = BlogPost.objects.all()
            elif user.groups.filter(name='author').exists():
                # show only the blog posts authored by the user to authors
                queryset = BlogPost.objects.filter(author=user)
            else:
                # show all published blog posts to regular users
                queryset = BlogPost.objects.filter(is_published=True)
        else:
            # show a message to unauthenticated users
            queryset = None
            message = "You need to be authenticated to view the blog posts."
            
        context = {
            'blog_posts': queryset,
            'message': message,
            'role_choices': ROLE_CHOICES,
        }
        
        return render(request, 'blog/blog_list.html', context)    
    
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class DeleteBlogPostView(View):
        def delete(self, request, slug, *args, **kwargs):
            try:
                post = get_object_or_404(BlogPost, slug=slug)
                post.delete()
                return JsonResponse({'status': 'success', 'message': 'Blog post deleted successfully'})
            except BlogPost.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Blog post not found'})

class RetrieveBlogPostView(View):
        def get(self, request, slug, *args, **kwargs):
            try:
                post = get_object_or_404(BlogPost, slug=slug)
                data = {
                    'title': post.title,
                    'slug': post.slug,
                    'content': post.content,
                    'image': post.image.url if post.image else None,
                }
                return JsonResponse({'status': 'success', 'data': data})
            except BlogPost.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Blog post not found'})    
            
class UserProfileViewSet(viewsets.ModelViewSet):
        queryset = UserProfile.objects.all()
        serializer_class = UserProfileSerializer     

class LoginView(ObtainAuthToken):
        def post(self, request, *args, **kwargs):
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        
class RegistrationView(generics.CreateAPIView):
    authentication_classes = []
    serializer_class = RegistrationSerializer
    permission_classes = []
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)    
