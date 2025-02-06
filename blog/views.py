from django.shortcuts import render,redirect,get_object_or_404
from blog.models import User
from django.contrib import messages
from django.contrib import auth
from blog.models import Blogs
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.

"""
This is the first page of the application .
Pagination is added to enhance performance 10 blogs per page. 
Users can views all blogs but requires authentication .
"""
def Home(request):
    blogs=Blogs.objects.all().order_by('-publish_date')
    p=Paginator(blogs,10)
    page=request.GET.get("page",1)
    if page!=1 and request.user.is_authenticated!=True:
        return redirect("blog:login")
    articles=p.get_page(page)
    return render(request,"index.html",{"posts":articles})

# Simple SignUp with django auth using Abstract model (blog.models.User) 
def Register(request):
    if request.method=="POST":
        f_name=request.POST['first_name']
        l_name=request.POST['last_name']
        mail=request.POST['email']
        password=request.POST['password']
        image=request.FILES.get("image") 
        if User.objects.filter(username=mail).exists():
            messages.info(request,"User aready exists")
        else:
            try:
                user=User.objects.create_user(username=mail,first_name=f_name,last_name=l_name,email=mail,password=password)
                if image:    # User image saved if uploaded by user else default image is provdied  
                    user.photo=image
                user.save()
                messages.success(request,"Welcome to BlogPost.")
                return redirect("blog:login") 
            except:  
                messages.error(request,"Sorry,unable to process your request")    
                return redirect("blog:register")
    return render(request,"register.html")

def UserLogin(request):
    if request.method=="POST":
        mail=request.POST['email']
        password=request.POST['password']
        user=auth.authenticate(username=mail,password=password)
        if user is not None:
            auth.login(request,user)  # Django builtin authentication with auth app
            return redirect("blog:index")
        else:
            messages.error(request,"Invalid credentials")
            return redirect("blog:login")
    return render(request,'login.html')
@login_required(login_url="blog:login")
def UserLogout(request):
     auth.logout(request)
     return redirect("blog:index")

# Adding new blog post
@login_required(login_url="blog:login")
def AddBlog(request):
    if request.method=="POST":
        t=request.POST['title']
        blog=request.POST['article']
        Blogs(title=t,article=blog,author=request.user).save()
        return redirect("blog:index")
    return render(request,"add-blog.html")

# View current user articles with their profile
@login_required(login_url="blog:login")
def MyArticles(request):
    user=User.objects.get(id=request.user.id)
    articles = Blogs.objects.select_related("author").filter(author=user)
    return render(request,"my-articles.html",{"author":user,"posts":articles})

# Individual view of every post with the respective author
@login_required(login_url="blog:login")
def ArticleDetail(request,id):
    article=get_object_or_404(Blogs,id=id)
    return render(request,"article-detail.html",{"post":article})

# Update Blog
@login_required(login_url="blog:login")
def UpdateBlog(request,pid):
    article=get_object_or_404(Blogs,id=pid) 
    if request.user!=article.author:  # Check if blogs belogs to the current user
        messages.error(request,"Permission denied")
        return redirect("blog:index")
    if request.method=="POST":
        t=request.POST['title']
        blog=request.POST['article']
        article.title=t
        article.article=blog
        article.save()
        return redirect("blog:article_detail",article.id)
    return render(request,"update-blog.html",{"post":article})

@login_required(login_url="blog:login")
def DeleteBlog(request,pid):
    article=get_object_or_404(Blogs,id=pid)
    if request.user!=article.author:
        messages.error(request,"Permission denied")
    article.delete()
    return redirect("blog:my_articles")

# Customized 404 page while deploying
# def Custom_404_Page(request,exception):
#     return render(request,'404.html',status=404)