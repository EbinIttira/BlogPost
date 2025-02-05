from django.shortcuts import render,redirect
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
