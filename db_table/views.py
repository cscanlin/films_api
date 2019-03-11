from django.shortcuts import render

def db_table(request):
    return render(request, 'index.html')
