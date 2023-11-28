from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.shortcuts import render, redirect
from . import forms
from authentification.models import Friend
from listings.models import Publication

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required
def account_page(request):
    user = request.user
    return render(request, 'authentification/account.html', {'user': user})

@login_required
def delete_account(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        logout(request)
        return redirect('login')
    return render(request, 'authentification/delete_account.html')

@login_required
def display_informations(request):
    return render(request, 'authentification/informations.html')

def login_page(request):
    form = forms.LoginForm()
    error = False
    message = ''
    if request.method == 'POST' and 'login' in request.POST:
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username =form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('my-account')
            else :
                error = True
                message = 'Identifiants invalides'
    return render(request, 'authentification/login.html', {'form': form, 'message' : message, 'error': error})

def signup_page(request):
    User = get_user_model()

    if request.method == 'POST':
        pseudo = request.POST.get('pseudo')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if User.objects.filter(username=pseudo).exists() or password1 != password2:
            error = 'Ce pseudo est déjà utilisé.'
            if password1 != password2:
                error = 'Les mots de passe ne correspondent pas.'
            # Le pseudo est déjà pris
            return render(request, 'authentification/signup.html', {'error': error})
        else:
            user = User.objects.create()
            user.username = pseudo
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.set_password(password1)
            user.save()
        login(request, user)
        return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentification/signup.html')


@login_required
def update_informations(request):
    User = get_user_model()
    user = request.user
    if request.method == 'POST':
        pseudo = request.POST.get('pseudo')
        firstName = request.POST.get('first_name')
        lastName = request.POST.get('last_name')
        email = request.POST.get('email')
        if pseudo:
            if User.objects.filter(username=pseudo).exists():
                # Le pseudo est déjà pris
                return render(request, 'authentification/update_informations.html', {'error': 'Ce pseudo est déjà utilisé.'})
            else:
                user.username = pseudo
        if firstName :
            user.first_name = firstName
        if lastName :
            user.last_name = lastName
        if email : 
            user.email = email
        user.save()
        return redirect('informations')
    return render(request, 'authentification/update_informations.html')

@login_required
def change_password(request):
    error = False
    message = ''
    if request.method == 'POST':
        print("test")
        if request.method == 'POST':
            old_password = request.POST.get('old_password')
            new_password1 = request.POST.get('new_password1')
            new_password = request.POST.get('new_password2')
            # Vérification de l'ancien mot de passe
            if not request.user.check_password(old_password):
                error = True
                message = "L'ancien mot de passe est incorrect"
            elif new_password != new_password1:
                error = True
                message = "Les mots de passe ne correspondent pas"
            else:
                # Si l'ancien mot de passe est correct, changer le mot de passe
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                return redirect('my-account')
    return render(request, 'authentification/change_password.html', {'error': error, "message": message})

@login_required
def friends(request):
    friends = Friend.objects.all()
    user = request.user
    return render(request, 'authentification/my_friend.html', {'friends': friends, 'user': user})

@login_required
def search_friends(request):
    search = False
    user = request.user
    User = get_user_model()
    if request.method == 'POST':
        if 'search' in request.POST:
            pseudo = request.POST.get('pseudo')
            if pseudo:
                if not User.objects.filter(username=pseudo).exists():
                    # Le pseudo est déjà pris
                    return render(request, 'authentification/search_friend.html', {'user': user, 'search': search, 'error': "Cette utilisateur n'existe pas"})
                else:
                    search = True
                    newFriend = User.objects.get(username=pseudo)
                    return render(request, 'authentification/search_friend.html', {'user': user, 'search': search, 'newFriend': newFriend})
    return render(request, 'authentification/search_friend.html', {'search': search, 'user': user})

def account_user(request, id):
    User = get_user_model()
    friend = User.objects.get(id=id)
    publications = Publication.objects.filter(author=friend)
    user = request.user
    if request.method == 'POST':
        if 'add' in request.POST:
            newFriend = Friend.objects.create(user=user, friend=friend)
            newFriend.save()
            return redirect('friend')
    return render(request, 'authentification/account_user.html', {'friend': friend, 'user': user, 'publications': publications})