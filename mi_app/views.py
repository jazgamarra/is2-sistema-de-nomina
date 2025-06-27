from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def menu_inicio(request):
    return render(request, 'mi_app/menu.html')
