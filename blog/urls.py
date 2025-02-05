from django.urls import path
from blog import views

app_name='blog'

urlpatterns=[
    path("",views.Home,name="index"),
    # URLs for user management
    path("register/",views.Register,name="register"),
    path("login/",views.UserLogin,name="login"),
    path("logout/",views.UserLogout,name="logout"),
  
    # Blog
    path("add-blog/",views.AddBlog,name="add_blog"),
    path("my-articles",views.MyArticles,name="my_articles"),


]