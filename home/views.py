
# Create your views here.
from django.shortcuts import render, HttpResponse,redirect
from .models import Contact
from Blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model,authenticate,login,logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# Create your views here.
def home(request):
    homePost = Post.objects.all().order_by('-views')[:3]
    print(homePost)
    context = {'homePost':homePost}
    return render(request,"Home/home.html",context)

def contact(request):
    #return HttpResponse("This is contact")  
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        print(name,email,phone,content)
        if len(name)<2:
            messages.error(request,"Please fill the Name Correctly")
        elif len(email)<3:
            messages.error(request,"Please fill the Email Address Correctly")
        elif len(phone)<10 or len(phone)>10:
            messages.error(request,"Please fill the phone Number Correctly")
        elif len(content)<4:
            messages.error(request,"Please fill the content Correctly")
        else:
            contact =Contact(name=name, email=email,phone=phone,content=content)
            contact.save()
            messages.success(request,"Your response saved Successfully..!!")
    return render(request,"Home/contact.html")

def about(request):
    #return HttpResponse("This is about")
    return render(request,"Home/about.html")

def search (request):
    query = request.GET['search']
    if len(query) > 78:
        allPost = Post.objects.none()
    else:
        allPostBlog = Post.objects.filter(title__icontains=query)
        allPostAdd = Post.objects.filter(content__icontains=query)
        allPost = allPostBlog.union(allPostAdd)
    if allPost.count() == 0:
        messages.error(request,"No Search result found. Please refind your query")
    context = {'allPost':allPost, 'search':query}
    return render(request,"Home/search.html",context)

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
       
    
        html_content = render_to_string('email_template.html', {'fname':fname, 'lname':lname, 'username':username, 'pass':pass1})
        text_content = strip_tags(html_content)
        email1 = EmailMultiAlternatives(
            'Thank you for registering with us : Icoder',
            text_content,
            settings.EMAIL_HOST_USER,
             [email]
             )
        email1.attach_alternative(html_content,'text/html')
        email1.send()

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
            return redirect('home')
        else:
            messages.error(request,"Invalid Credentials, Please try again")
            return redirect('home')
    else:
       return HttpResponse('404 - Not Found')

def handleLogout(request):
        logout(request)
        messages.success(request,"You are Successfully Logged Out")
        return redirect('home')


