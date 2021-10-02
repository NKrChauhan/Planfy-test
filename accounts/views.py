from django.shortcuts import render,redirect
from .forms import UserLoginForm,UserRegisterForm
from django.contrib.auth import login ,authenticate ,logout,get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import  ValidationError
from django.utils.http import is_safe_url
  
# Create your views here.

User = get_user_model()

def LoginView(request):
    form=UserLoginForm(request.POST or None)
    next_=request.GET.get('next')
    next_post=request.POST.get('next')
    redirect_urls=next_ or next_post or None
    if form.is_valid():
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            try:
                del request.session['guest_user_id'] #if user try to login after checkout
            except:
                pass
            if is_safe_url(redirect_urls,request.get_host()):
                return redirect(redirect_urls)
            else:
                return redirect('/')
        else:
            raise ValidationError('Invalid uname or password', code='invalid')
    return render(request,"auth/login.html",{'form':form})

def RegisterView(request):
    form=UserRegisterForm(request.POST or None)
    if form.is_valid():
        uname=form.cleaned_data.get("Username")
        email=form.cleaned_data.get("Email")
        passwd=form.cleaned_data.get("Password")
        new_user=User.objects.create_user(uname,email,passwd)
        return redirect('/login')
    return render(request,"auth/register.html",{"form":form})

@login_required
def LogoutView(request):
    logout(request)
    return redirect('/login')
