from django.urls import include, path
from . import views
from .views import UpdatePostView
from rest_framework import routers
from .views import BlogPostViewSet, CommentViewSet, UserProfileViewSet, LoginView,DeleteBlogPostView,RetrieveBlogPostView
#from rest_framework.authtoken import views
from rest_framework.authtoken.views import obtain_auth_token
from .views import BlogPostViewSet



router = routers.DefaultRouter()
router.register(r'blogs', BlogPostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'userprofiles', UserProfileViewSet)

urlpatterns = [
    path('api-login/',LoginView.as_view(),name='login'),
    path("", views.blogs, name="blogs"),
    path("blog/<str:slug>/", views.blogs_comments, name="blogs_comments"),
    path("add_blogs/", views.add_blogs, name="add_blogs"),
    path("edit_blog_post/<str:slug>/", UpdatePostView.as_view(), name="edit_blog_post"),
    #path("delete_blog_post/<str:slug>/", views.Delete_Blog_Post, name="delete_blog_post"),
    path("search/", views.search, name="search"),
    path('delete-blog-post/<slug:slug>/', DeleteBlogPostView.as_view(), name='delete_blog_post'),
    path("profile/", views.Profile, name="profile"),
    path("register/", views.Register, name="register"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),
    path('', include(router.urls)),
    path('api-register/', views.RegistrationView.as_view(), name='register'),
    path('retrive-blog-post/<slug:slug>/', RetrieveBlogPostView.as_view(), name='delete_blog_post'),
]