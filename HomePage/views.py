from django.shortcuts import render

def index(request):
    return render(request, 'HomePage/home.html')

def info(request):
    about_info = {"Author": 'Oleksandr Kharin', "Country": 'Ukraine',
                                                   "Date": "25.06.2018"}
    return render(request, 'HomePage/about.html', {'content': about_info})
