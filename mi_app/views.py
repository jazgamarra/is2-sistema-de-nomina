from django.shortcuts import render

def menu_inicio(request):
    return render(request, 'mi_app/menu.html')
