from django.shortcuts import render,redirect
from .forms import SignUpForm

# Create your views here.
def IndexView(request):
    return render(request,'index.html',)

def registerView(request):
    if request.method=="POST":
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_url')
    else:
            form=SignUpForm()
    return render(request,'registration/register.html',{'form': form})
