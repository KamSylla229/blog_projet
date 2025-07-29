from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Article
from .forms import ArticleForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Inscription réussie.")
            return redirect('article_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Connexion réussie.")
            return redirect('article_list')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    return render(request, 'blog_app/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "Déconnexion effectuée.")
    return redirect('login')


def article_list(request):
    articles = Article.objects.all().order_by('-date_publication')
    return render(request, 'blog_app/article_list.html', {'articles': articles})

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'blog_app/article_detail.html', {'article': article})

@login_required
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.auteur = request.user
            article.save()
            messages.success(request, "Article créé avec succès.")  # ✅ Message ici
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm()
    return render(request, 'blog_app/article_form.html', {'form': form})


@login_required
def article_update(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if article.auteur != request.user:
        messages.error(request, "Vous n'avez pas la permission d'effectuer cette action.")
        return redirect('article_detail', pk=pk)

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "Article modifié avec succès.")
            return redirect('article_detail', pk=pk)
    else:
        form = ArticleForm(instance=article)

    return render(request, 'blog_app/article_form.html', {'form': form})



@login_required
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if article.auteur != request.user:
        messages.error(request, "Vous n'avez pas la permission d'effectuer cette action.")
        return redirect('article_detail', pk=pk)

    if request.method == 'POST':
        article.delete()
        messages.success(request, "Article supprimé.")
        return redirect('article_list')

    return render(request, 'blog_app/article_confirm_delete.html', {'article': article})
