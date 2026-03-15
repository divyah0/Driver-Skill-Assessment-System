from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Chapter, Question, QuizResult
from .forms import RegisterForm
import random

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def chapters(request):
    chapters = Chapter.objects.all()
    return render(request, 'chapters.html', {'chapters': chapters})

@login_required
def quiz(request):
    questions_list = list(Question.objects.all())  # Convert QuerySet to list
    random.shuffle(questions_list)  # Shuffle the list of questions

    if request.method == 'POST':
        score = 0
        total_questions = len(questions_list)
        for question in questions_list:
            selected_option = request.POST.get(f'question_{question.id}')
            if selected_option == question.correct_option:
                score += 1
        percentage = (score / total_questions) * 100
        QuizResult.objects.create(user=request.user, score=percentage)
        if percentage >= 70:
            return render(request, 'result.html', {'score': percentage, 'show_certificate': True})
        else:
            return render(request, 'result.html', {'score': percentage, 'show_certificate': False})

    paginator = Paginator(questions_list, 10)
    page = request.GET.get('page', 1)

    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)

    return render(request, 'quiz.html', {'questions': questions})

@login_required
def quiz_result(request):
    results = QuizResult.objects.filter(user=request.user).order_by('-quiz_date')
    return render(request, 'result.html', {'results': results})

@login_required
def view_correct_answers(request):
    questions = Question.objects.all()

    context = {
        'questions': questions
    }

    return render(request, 'correct_answers.html', context)

@login_required
def certificate(request):
    user_name = request.user.get_full_name()
    
    try:
        quiz_result = QuizResult.objects.filter(user=request.user).latest('quiz_date')
        score = quiz_result.score
    except QuizResult.DoesNotExist:
        score = None

    context = {
        'user_name': user_name,
        'score': score,
    }
    return render(request, 'certificate.html', context)
