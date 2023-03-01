from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from MainApp.models import Snippet
from MainApp.forms import SnippetForm, UserRegistrationForm, CommentForm
from django.db.models import Count
from django.contrib.auth.models import User


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


@login_required()
def add_snippet_page(request):
    if request.method == "GET":  # хотим получить форму
        form = SnippetForm()
        context = {
            'pagename': 'Добавление нового сниппета',
            'form': form
        }
        return render(request, 'pages/add_snippet.html', context)
    if request.method == "POST":  # хотим создать Сниппет(данные от формы)
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.user = request.user
            snippet.save()
            return redirect('snippets-list')


@login_required()
def snippet_my(request):
    context = {'pagename': 'Мои сниппеты'}
    snippets = Snippet.objects.filter(user=request.user)
    context["snippets"] = snippets
    return render(request, 'pages/view_snippets.html', context)


def snippets_page(request):
    snippets = Snippet.objects.all()
    lang = request.GET.get("lang")
    sort = request.GET.get("sort")
    user_id = request.GET.get("user_id")
    users_with_snippets = User.objects.all().annotate(num_snippets=Count('snippets')).filter(num_snippets__gte=1)

    if lang:
        snippets = snippets.filter(lang__short_name=lang)
    if user_id:
        snippets = snippets.filter(user__id=user_id)
    if sort:
        snippets = snippets.order_by(sort)
    context = {
        'sort': sort,
        'lang': lang,
        'pagename': 'Просмотр сниппетов',
        'snippets': snippets,
        'users_with_snippets': users_with_snippets
    }
    return render(request, 'pages/view_snippets.html', context)


def snippet_detail(request, snippet_id):
    snippet = Snippet.objects.get(id=snippet_id)
    comment_form = CommentForm()
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippet': snippet,
        # 'comments': snippet.comments.all(),
        'comment_form': comment_form
    }
    return render(request, 'pages/snippet-detail.html', context)


def snippet_delete(request, snippet_id):
    snippet = get_object_or_404(Snippet, id=snippet_id)
    snippet.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def snippet_like(request, snippet_id):
    snippet = get_object_or_404(Snippet, id=snippet_id)
    snippet.like.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def create_user(request):
    context = {'pagename': 'Регистрация пользователя'}
    if request.method == "GET":
        form = UserRegistrationForm()
        context["form"] = form
        return render(request, 'pages/registration.html', context)
    elif request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        context["form"] = form
        return render(request, 'pages/registration.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            # Return error message
            pass
    return redirect('home')


def comment_add(request):
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            snippet_id = request.POST["snippet_id"]
            snippet = Snippet.objects.get(id=snippet_id)
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.snippet = snippet
            comment.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def logout(request):
    auth.logout(request)
    return redirect('home')
