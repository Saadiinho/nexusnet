<<<<<<< HEAD
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



def signup_page(request):
    User = get_user_model()
    user_connected = request.user
    if user_connected : 
        logout(request)
    if request.method == 'POST':
        pseudo = request.POST.get('pseudo')
        pseudo = str(pseudo)
        pseudo = pseudo.lower()
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
            admin = User.objects.get(username='admin')
            friend = Friend.objects.create(user=user, friend=admin)
            friend.save()
        login(request, user)
        return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentification/signup.html')


@login_required
def update_informations(request):
    User = get_user_model()
    user = request.user
    if request.method == 'POST':
        pseudo = request.POST.get('pseudo')
        pseudo = str(pseudo)
        pseudo = pseudo.lower()
        firstName = request.POST.get('first_name')
        lastName = request.POST.get('last_name')
        email = request.POST.get('email')
        photo = request.FILES.get('profile_photo')
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
        if photo:
            user.profile_photo = photo
        user.save()
        return redirect('informations')
    return render(request, 'authentification/update_informations.html')

@login_required
def change_password(request):
    error = False
    message = ''
    if request.method == 'POST':
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


def login_page(request):
    user = request.user
    if user : 
        logout(request)
    error = False
    message = ''
    if request.method == 'POST' and 'login' in request.POST:
        username = request.POST.get('pseudo')
        username = str(username)
        username = username.lower()
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('my-account')
        else :
            error = True
            message = 'Identifiants invalides'
    return render(request, 'authentification/login.html', {'message' : message, 'error': error})


@login_required
def friends(request):
    friends = Friend.objects.all()
    user = request.user
    count = count_friend(request)
    return render(request, 'authentification/my_friend.html', {'friends': friends, 'user': user, 'count': count})

@login_required
def search_friends(request):
    search = False
    user = request.user
    User = get_user_model()
    count = count_friend(request)
    if request.method == 'POST':
        if 'search' in request.POST:
            pseudo = request.POST.get('pseudo')
            if pseudo:
                if not User.objects.filter(username=pseudo).exists() or user.username == pseudo:
                    return render(request, 'authentification/search_friend.html', {'user': user, 'search': search, 'error': "Cette utilisateur n'existe pas", 'count': count})
                else:
                    search = True
                    newFriend = User.objects.get(username=pseudo)
                    return render(request, 'authentification/search_friend.html', {'user': user, 'search': search, 'newFriend': newFriend, 'count': count})
    return render(request, 'authentification/search_friend.html', {'search': search, 'user': user, 'count': count})


def count_friend(request):
    friends = Friend.objects.all()
    user = request.user
    count = 0
    for friend in friends:
        if friend.user == user or friend.friend == user:
            count +=1
    return count

def presence(request, id):
    list_friends = Friend.objects.all()
    User = get_user_model()
    user = request.user
    friend = User.objects.get(id=id)
    for list_friend in list_friends:
        if list_friend.user == user:
            if list_friend.friend == friend:
                presence = True
        elif list_friend.friend == user:
            if list_friend.user == friend:
                presence = True
    return presence


def account_user(request, id):
    list_friends = Friend.objects.all()
    User = get_user_model()
    friend = User.objects.get(id=id)
    publications = Publication.objects.filter(author=friend)
    user = request.user
    presence = False
    count = count_friend(request)
    for list_friend in list_friends:
        # Vérification des deux sens de l'amitié
        if (list_friend.user == user and list_friend.friend == friend) or (list_friend.user == friend and list_friend.friend == user):
            presence = True
            break 
    if request.method == 'POST':
        if 'add' in request.POST:
            if not presence:
                newFriend = Friend.objects.create(user=user, friend=friend)
                newFriend.save()
                return redirect('friend')
            else :
                return render(request, 'authentification/account_user.html', {'friend': friend, 'user': user, 'publications': publications, 'presence': presence, 'count': count})
        elif 'delete' in request.POST:
            for list_friend in list_friends:
                if (list_friend.friend == friend and list_friend.user == user) or (list_friend.friend == user and list_friend.user == friend):
                    list_friend.delete()
                    return redirect('friend')
    return render(request, 'authentification/account_user.html', {'friend': friend, 'user': user, 'publications': publications, 'presence': presence, 'count': count})
 
def suggestion(request):
    count = count_friend(request)
    return render(request, 'authentification/suggestion.html', {'count': count})
=======
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



def signup_page(request):
    User = get_user_model()
    user_connected = request.user
    if user_connected : 
        logout(request)
    if request.method == 'POST':
        pseudo = request.POST.get('pseudo')
        pseudo = str(pseudo)
        pseudo = pseudo.lower()
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
            admin = User.objects.get(username='admin')
            friend = Friend.objects.create(user=user, friend=admin)
            friend.save()
        login(request, user)
        return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentification/signup.html')


@login_required
def update_informations(request):
    User = get_user_model()
    user = request.user
    if request.method == 'POST':
        pseudo = request.POST.get('pseudo')
        pseudo = str(pseudo)
        pseudo = pseudo.lower()
        firstName = request.POST.get('first_name')
        lastName = request.POST.get('last_name')
        email = request.POST.get('email')
        photo = request.FILES.get('profile_photo')
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
        if photo:
            user.profile_photo = photo
        user.save()
        return redirect('informations')
    return render(request, 'authentification/update_informations.html')

@login_required
def change_password(request):
    error = False
    message = ''
    if request.method == 'POST':
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


def login_page(request):
    user = request.user
    if user : 
        logout(request)
    error = False
    message = ''
    if request.method == 'POST' and 'login' in request.POST:
        username = request.POST.get('pseudo')
        username = str(username)
        username = username.lower()
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('my-account')
        else :
            error = True
            message = 'Identifiants invalides'
    return render(request, 'authentification/login.html', {'message' : message, 'error': error})


@login_required
def friends(request):
    friends = Friend.objects.all()
    user = request.user
    count = count_friend(request)
    return render(request, 'authentification/my_friend.html', {'friends': friends, 'user': user, 'count': count})

@login_required
def search_friends(request):
    search = False
    user = request.user
    User = get_user_model()
    count = count_friend(request)
    if request.method == 'POST':
        if 'search' in request.POST:
            pseudo = request.POST.get('pseudo')
            if pseudo:
                if not User.objects.filter(username=pseudo).exists():
                    return render(request, 'authentification/search_friend.html', {'user': user, 'search': search, 'error': "Cette utilisateur n'existe pas", 'count': count})
                else:
                    search = True
                    newFriend = User.objects.get(username=pseudo)
                    return render(request, 'authentification/search_friend.html', {'user': user, 'search': search, 'newFriend': newFriend, 'count': count})
    return render(request, 'authentification/search_friend.html', {'search': search, 'user': user, 'count': count})


def count_friend(request):
    friends = Friend.objects.all()
    user = request.user
    count = 0
    for friend in friends:
        if friend.user == user or friend.friend == user:
            count +=1
    return count

def presence(request, id):
    list_friends = Friend.objects.all()
    User = get_user_model()
    user = request.user
    friend = User.objects.get(id=id)
    for list_friend in list_friends:
        if list_friend.user == user:
            if list_friend.friend == friend:
                presence = True
        elif list_friend.friend == user:
            if list_friend.user == friend:
                presence = True
    return presence


def account_user(request, id):
    list_friends = Friend.objects.all()
    User = get_user_model()
    friend = User.objects.get(id=id)
    publications = Publication.objects.filter(author=friend)
    user = request.user
    presence = False
    count = count_friend(request)
    for list_friend in list_friends:
        # Vérification des deux sens de l'amitié
        if (list_friend.user == user and list_friend.friend == friend) or (list_friend.user == friend and list_friend.friend == user):
            presence = True
            break 
    if request.method == 'POST':
        if 'add' in request.POST:
            if not presence:
                newFriend = Friend.objects.create(user=user, friend=friend)
                newFriend.save()
                return redirect('friend')
            else :
                return render(request, 'authentification/account_user.html', {'friend': friend, 'user': user, 'publications': publications, 'presence': presence, 'count': count})
        elif 'delete' in request.POST:
            for list_friend in list_friends:
                if (list_friend.friend == friend and list_friend.user == user) or (list_friend.friend == user and list_friend.user == friend):
                    list_friend.delete()
                    return redirect('friend')
    return render(request, 'authentification/account_user.html', {'friend': friend, 'user': user, 'publications': publications, 'presence': presence, 'count': count})
 
def suggestion(request):
    count = count_friend(request)
    return render(request, 'authentification/suggestion.html', {'count': count})
>>>>>>> 710d29c1cf81e76015b4297a69c10f218c08b0b3
