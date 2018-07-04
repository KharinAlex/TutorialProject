from django.shortcuts import render, redirect
from .models import UploadImage
from .forms import UploadImageForm


def image_upload(request):
    if request.method == "POST":
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('media_main')
    else:
        form = UploadImageForm()
    return render(request, 'Media/mediaupload.html', {'form': form})

def index(request):
    return render(request, 'Media/media.html', {'imagesContent': UploadImage.objects.order_by("id")[:6]})
