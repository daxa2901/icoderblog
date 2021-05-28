from django.shortcuts import render, HttpResponse, redirect
from Blog.models import Post,BlogComment
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model,authenticate,login,logout
from Blog.templatetags import get_Dict
from django.core.paginator import Paginator
# Create your views here.
def blogHome(request):
    if request.method == 'POST':
        messages.error(request,"Please First Login to Our Icoder blog to read full content")
    allPost = Post.objects.all().order_by('-views')
    paginator = Paginator(allPost,2, orphans=1)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    user = request.user
    context = {'allPost':page_obj, 'user':user}
    return render(request,"Blog/blogHome.html", context)
    

def blogPost(request, slug):
    
        post = Post.objects.filter(slug=slug).first()
        post.views = post.views + 1
        post.save()
        comments = BlogComment.objects.filter(post=post, parent=None)
        replies = BlogComment.objects.filter(post=post).exclude(parent=None)
        repDict = {}
        for reply in replies:
            if reply.parent.sno not in repDict.keys():
                repDict[reply.parent.sno] = [reply]
            else:
                repDict[reply.parent.sno].append(reply) 
        
        context = {'post':post, 'comments':comments,'user':request.user,'repDict':repDict}
        return render(request,"Blog/blogPost.html", context)
        


def postComment(request):
    if request.method == 'POST':
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get('postSno')
        print(postSno)
        post = Post.objects.get(id=postSno)
        parentSno =  request.POST.get('parentSno')

        if parentSno == "":
                
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request,"Comment successfully")
            
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post,parent=parent)
            comment.save()
            messages.success(request,"Your Reply Send successfully")
        return redirect(f'/blog/{post.slug}')

    else:
       return HttpResponse('404 - Not Found')

def handleSignup(request):
    if request.method == 'POST':
        #Get The post parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 =  request.POST['password']
        cpass = request.POST['cpassword']

        User = get_user_model()
        users = User.objects.filter(username=username)
        print(users)
        #Checks for erroneous input

        if not users.count() == 0:
             messages.error(request,"Username must be unique")
             return redirect('home')
        
        if len(username) > 10:
            messages.error(request,"Username must be under 10 character")
            return redirect('home')
  
        if not username.isalnum():
            messages.error(request,"Usernamemust must contain alphanumeric character")
            return redirect('home')

        if not fname.isalpha():
            messages.error(request,"First name must contains only  alphabetic character")
            return redirect('home')
        
        if not lname.isalpha():
            messages.error(request,"Last name must contains only  alphabetic character")
            return redirect('home')
           
        elif pass1 != cpass:
            messages.error(request,"Passwords do not match")
            return redirect('home')




        #create the user
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request,"Your account has been successfully created")
        return redirect('home')
    else:
       return HttpResponse('404 - Not Found')

def handleLogin(request):
    if request.method == 'POST':
        #Get The post parameters
        loginusername = request.POST['loginusername']
        loginpassword =  request.POST['loginpassword']
        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request,user)
            messages.success(request,"You are Successfully Logged In")
            return redirect('blogHome')
        else:
            messages.error(request,"Invalid Credentials, Please try again")
            return redirect('blogHome')
    else:
       return HttpResponse('404 - Not Found')

def handleLogout(request):
        logout(request)
        messages.success(request,"You are Successfully Logged Out")
        return redirect('blogHome')


