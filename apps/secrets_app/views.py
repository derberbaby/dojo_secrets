from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Count
from .models import User, UserManager, Secret, SecretManager

# Create your views here.
def index(request):
    return render(request, 'secrets_app/index.html')

def register(request):
    post_data = request.POST.copy()
    result = User.objects.register(post_data)
    if isinstance(result,list):
        for err in result:
            messages.error(request, err)
        return redirect('/')
    else:
        request.session['user'] = result
        return redirect(reverse('secrets'))

def login(request):
    post_data = request.POST.copy()
    result = User.objects.login(post_data)
    if isinstance(result,list):
        for err in result:
            messages.error(request, err)
        return redirect('/')
    else:
        request.session['user'] = result
        return redirect(reverse('secrets'))

def secrets(request):
    user = User.objects.get(id=request.session['user'])
    secrets = Secret.objects.all().order_by('-created_at')[:5]
    likes = Secret.objects.filter(likes__id=user.id)
    context = {
        'user': user,
        'secrets': secrets,
        'likes': likes
    }
    return render(request, 'secrets_app/secrets.html', context)

def logout(request):
    request.session.pop('user')
    return redirect(reverse('index'))

def post_secret(request):
    post_data = request.POST.copy()
    result = Secret.objects.validate(post_data, request.session['user'])
    if isinstance(result,list):
        for err in result:
            messages.error(request, err)
        return redirect(reverse('secrets'))
    else:
        return redirect(reverse('secrets'))

def like(request, secret_id):
    user = User.objects.get(id=request.session['user'])
    secret = Secret.objects.get(id=secret_id)
    secret.likes.add(user)

    origin = request.META['HTTP_REFERER']
    page = origin.split('/')[3]
    return redirect(reverse(page))

def unlike(request, secret_id):
    user = User.objects.get(id=request.session['user'])
    secret = Secret.objects.get(id=secret_id)
    secret.likes.remove(user)

    origin = request.META['HTTP_REFERER']
    page = origin.split('/')[3]
    return redirect(reverse(page))

def delete(request, secret_id):
    user = User.objects.get(id=request.session['user'])
    secret = Secret.objects.get(id=secret_id)
    secret.delete()

    origin = request.META['HTTP_REFERER']
    page = origin.split('/')[3]
    return redirect(reverse(page))

def popular(request):
    user = User.objects.get(id=request.session['user'])
    secrets = Secret.objects.all().annotate(num_likes=Count('likes')).order_by('-num_likes')
    likes = Secret.objects.filter(likes__id=user.id)
    context = {
        'user': user,
        'secrets': secrets,
        'likes': likes
    }
    return render(request, 'secrets_app/popular.html', context)

def my_secrets(request):
    user = User.objects.get(id=request.session['user'])
    secrets = Secret.objects.filter(user = user.id)
    likes = Secret.objects.filter(likes__id=user.id)
    context = {
        'user': user,
        'secrets': secrets,
        'likes': likes
    }
    return render(request, 'secrets_app/my_secrets.html', context)

def other_secrets(request):
    user = User.objects.get(id=request.session['user'])
    secrets = Secret.objects.exclude(user = user.id).exclude(likes__id=user.id)
    context = {
        'user': user,
        'secrets': secrets
    }
    return render(request, 'secrets_app/other_secrets.html', context)

def home(request):
    return redirect(reverse('secrets'))
