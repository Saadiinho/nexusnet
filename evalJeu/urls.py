"""evalJeu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

import listings.views
import authentification.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', authentification.views.login_page, name='login'),
    path('logout/', authentification.views.logout_user, name='logout'),
    path('signup/', authentification.views.signup_page, name='signup'),
    path('account/', authentification.views.account_page, name='my-account'),
    path('change-password/', authentification.views.change_password, name='change_password'),
    path('delete-account/', authentification.views.delete_account, name='delete'),
    path('account-informations/', authentification.views.display_informations, name='informations'),
    path('update-infrmations/', authentification.views.update_informations, name='update'),

    path('friends/', authentification.views.friends, name='friend'),
    path('search-friends/', authentification.views.search_friends, name='searchFriend'),
    path('account-user/<int:id>', authentification.views.account_user, name="accountUser"),
    path('suggestion/', authentification.views.suggestion, name='suggestion'),
    #path('friends/', authentification.views.friends, name='friend'),


    path('home/', listings.views.home, name='home'),
    path('publications/<int:id>/', listings.views.publicationDetail, name='publicationDetail'),
    path('write-publication/', listings.views.writePublication, name='writePublication'),
    path('publication-update/<int:id>/', listings.views.publicationUpdate, name='publicationUpdate'),
    path('publication-delete/<int:id>/', listings.views.publicationDelete, name='publicationDelete'),
    path('my-publications/', listings.views.myPublication, name='myPublications'),
] 

if settings.DEBUG:
    urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
