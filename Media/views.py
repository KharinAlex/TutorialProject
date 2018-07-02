from django.shortcuts import render, render_to_response
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import UploadImageForm, UploadImage

def media_upload(request):
    if request.method == "POST":
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('media-list'))
    else:
        form = UploadImageForm()
    return render_to_response('Media/media.html', {'form': form})

def index(request):
    return render(request, 'Media/media.html', {'imagesContent': UploadImage.objects.all})
