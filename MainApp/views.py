from django.http import Http404
from django.shortcuts import render, redirect
from MainApp.models import Snippet


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    context = {'pagename': 'Добавление нового сниппета'}
    return render(request, 'pages/add_snippet.html', context)


def snippets_page(request):
    snippets = Snippet.objects.all()
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': snippets
    }
    return render(request, 'pages/view_snippets.html', context)


def snippet_detail(request):
    pass


def snippet_create(request):
    if request.method == "POST":
        name = request.POST["name"]
        lang = request.POST["lang"]
        code = request.POST["code"]
        snippet = Snippet(name=name, lang=lang, code=code)
        snippet.save()
        return redirect('snippets-list')