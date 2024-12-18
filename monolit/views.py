from lib2to3.fixes.fix_input import context

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from prompt_toolkit.validation import ValidationError

from .forms import ProfileForm, RegistrationForm, UserUpdate, ProfileUpdate, PostForm, AnswerOptionFormSet
from .models import Profile, Post, Vote, AnswerOption


def home_view(request):
    if request.user.is_authenticated:
        return render(request, 'home.html', {'profile': request.user.profile})
    else:
        return render(request, 'home.html')

def register_view(request):
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, "Вы успешно зарегистрировались!")
            return redirect('login')
    else:
        user_form = RegistrationForm()
        profile_form = ProfileForm()
    return render(request, 'register.html', {'userform': user_form, 'profileform': profile_form})

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Вы успешно авторизировались')
            return redirect('home')
        else:
            messages.error(request, "неправильное имя пользователя или пароль")

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из аккаунта')
    return redirect('home')

@login_required
def profile_view(request):
    if request.method == 'POST':
        user_form = UserUpdate(request.POST, instance=request.user)
        profile_form = ProfileUpdate(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Ваш профиль был обновлен')
            return redirect('profile')

    else:
        user_form = UserUpdate(instance=request.user)
        profile_form = ProfileUpdate(instance=request.user.profile)

    context = {
        'userform': user_form,
        'profileform': profile_form,
        'profile': request.user.profile
    }
    return render(request, 'profile.html', context)

@login_required
def delete_account(request):
    if request.method == "POST":
        request.user.delete()
        messages.success(request, 'Ваш аккаунт был успешно удален')
        return redirect('home')

    return render(request, 'deleteaccount.html')

# Create your views here.

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post_list.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        answer_formset = AnswerOptionFormSet(request.POST)
        if post_form.is_valid() and answer_formset.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            for answer_form in answer_formset:
                answer_option = answer_form.save(commit=False)
                answer_option.post = post
                answer_option.save()
            return redirect('post_detail', post_id=post.id)
    else:
        post_form = PostForm()
        answer_formset = AnswerOptionFormSet(queryset=AnswerOption.objects.none())
    return render(request, 'create_post.html', {'post_form': post_form, 'answer_formset': answer_formset})

@login_required
def post_detail(request, post_id):
    user = request.user
    if not user:
        messages.error(request, 'Сначала войдите в систему, что бы голосовать')
        return redirect('home')
    post = get_object_or_404(Post, id=post_id)
    print(post)
    answer_options = post.answer_options.all()
    print(answer_options)
    return render(request, 'post_detail.html', {'post': post, 'answer_options': answer_options})

@login_required
def vote_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method =='POST':
        selected_option_id = request.POST.get('answer_option')
        selected_option = get_object_or_404(AnswerOption, id=selected_option_id, post=post)

        votes, created = Vote.objects.get_or_create(user = request.user, post=post, defaults={'answer_option': selected_option})
        if created:
            selected_option.votes += 1
            selected_option.save()
            return redirect('post_detail', post_id=post.id)
        else:
            messages.error(request, 'вы уже проголосовали за этот пост')
            return redirect('post_detail', post_id = post.id)

    return redirect('post_detail', post_id=post.id)
