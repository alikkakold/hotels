from django.shortcuts import render


def main_page(request):
    title = 'Home'
    user = request.user

    return render(request, 'mainapp/index.html', {'user': user, 'title': title})

def error_404(request):
    return render(request, 'mainapp/404.html')

