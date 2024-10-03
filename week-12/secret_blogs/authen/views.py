from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib import messages
from django.views import View
from django.contrib.auth.forms import AuthenticationForm

class LoginView(View):

    def get(self, request):
        # code here
        return render(request, 'login.html', {"form": None , "next": request.GET.get('next', '/')})
    
    def post(self, request):
        # code here
        form = AuthenticationForm(data=request.POST)
        
        next_url = request.POST.get("next", "/")
        print(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(next_url)
        else:
            return redirect("?next="+next_url, { "form": form })

class LogoutView(View):
    
    def get(self, request):
        # code here
        logout(request)
        return redirect('login')