from django.shortcuts import render


def index(request):
    """Отображает главную страницу меню."""
    return render(request, 'menu/index.html')
