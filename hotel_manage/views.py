from django.shortcuts import render,redirect

# Create your views here.
from .models import User, Room, Guest, Order

def login(request):
    recv_data = request.POST
    if 'username' in recv_data and 'password' in recv_data:
        try:
            username = recv_data['username']
            password = recv_data['password']
        
            user = User.objects.get(user_username=username)
            if password == user.user_password:
                request.session['username'] = username
                request.session['is_admin'] = user.is_admin
                return redirect('/index')
            else:
                return render(request, 'login.html', {'msg': 'password error'})
        except User.DoesNotExist:
            return render(request, 'login.html', {'msg': 'username error'})
    else:
        return render(request, 'login.html', {'msg': ' error'})
    
def index(request):
    try:
        username = request.session.get('username')
        is_admin = request.session.get('is_admin')
        
        if is_admin:
            pass
        else:
            return render(request, 'index.html', {'msg': 'welcome'})
    
    except Exception as e:
        print(repr(e))
        return render(request, 'index.html', {'msg': 'please login first'})