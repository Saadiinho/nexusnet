from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from listings.models import Publication
from listings.forms import *

@login_required
def home(request):
    user = request.user
    publications = Publication.objects.all()
    if publications.exists():
        present = True
    else :
        present = False
    return render(request, 'listings/home.html', {'publications': publications, 'present': present, "user": user})

def publicationDetail(request, id):
    publication = Publication.objects.get(id=id)
    return render(request, 'listings/publicationDetails.html', {'publication': publication})

@login_required
def writePublication(request):
    if request.method == 'POST':
        message = request.POST.get('publication')
        image = request.POST.get('imageUpload')
        private = request.POST.get('private')
        isPrivate = False
        if private == 'on':
            isPrivate = True
        date = timezone.now()
        author = request.user
        publication = Publication.objects.create(message=message, date=date, picture=image, author=author, isPrivate=isPrivate)
        publication.save()
        return redirect('home')
    else:
        form = writePublicationForm()
    return render(request, 'listings/writePublication.html', {'form': form})
@login_required
def publicationCreated(request):
    return render(request, 'listings/publicationCreated.html')
@login_required
def publicationUpdate(request, id):
    publication = Publication.objects.get(id=id)
    if request.method == 'POST':
        publication.message = request.POST.get('publication')
        publication.picture = request.POST.get('imageUpload')
        private = request.POST.get('private')
        isPrivate = False
        if private == 'on':
            isPrivate = True
            publication.isPrivate = isPrivate
        publication.date = timezone.now()
        publication.save()
        return redirect("publicationDetail", publication.id)
    else: 
        form = writePublicationForm()
    return render(request, 'listings/publicationUpdate.html', {'form': form})
@login_required
def publicationDelete(request, id):
    publication = Publication.objects.get(id=id)
    if request.method == 'POST':
        publication.delete()
        return redirect('home')
    return render(request, 'listings/publicationDelete.html')
@login_required
def myPublication(request):
    user = request.user
    publications = Publication.objects.filter(author=user)
    return render(request, 'listings/myPublication.html', {'publications': publications})