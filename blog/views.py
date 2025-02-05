from django.shortcuts import render,redirect,get_object_or_404
from blog.models import User
from django.contrib import messages
from django.contrib import auth
from blog.models import Blogs

# Create your views here.
def Home(request):
    return render(request,"index.html")

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
                if image:
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
            auth.login(request,user)
            return redirect("blog:index")
        else:
            messages.error(request,"Invalid credentials")
            return redirect("blog:login")
    return render(request,'login.html')

def UserLogout(request):
     auth.logout(request)
     return redirect("blog:index")

def AddBlog(request):
    if request.method=="POST":
        t=request.POST['title']
        blog=request.POST['article']
        Blogs(title=t,article=blog,author=request.user).save()
        return redirect("blog:index")
    return render(request,"add-blog.html")

def MyArticles(request):
    user=User.objects.get(id=request.user.id)
    articles = Blogs.objects.select_related("author").filter(author=user)
    return render(request,"my-articles.html",{"author":user,"posts":articles})

def ArticleDetail(request,id):
    article=get_object_or_404(Blogs,id=id)
    return render(request,"article-detail.html",{"post":article})

def UpdateBlog(request,pid):
    article=get_object_or_404(Blogs,id=pid)
    if request.user!=article.author:
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

def DeleteBlog(request,pid):
    article=get_object_or_404(Blogs,id=pid)
    if request.user!=article.author:
        messages.error(request,"Permission denied")
    article.delete()
    return redirect("blog:my_articles")

def Custom_404_Page(request,exception):
    return render(request,'404.html',status=404)