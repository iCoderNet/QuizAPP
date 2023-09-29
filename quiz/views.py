from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, "index.html")


def signin(request):
    next = request.GET.get("next", "home")
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        if email!="" and password!="":
            user = User.objects.filter(email=email)
            if len(user) > 0:
                user = authenticate(request,username=email,password=password)
                print(user)
                if user:
                    login(request, user)
                    return redirect(next)
                else:
                    messages.warning(request, "Parol mos kelmadi")
            else:
                messages.warning(request, "Bunday profil topilmadi")
        else:
            messages.warning(request, "Maydonlarni malumotlar bilan to'ldiring")
    
    return render(request, "login.html")


def signout(request):
    logout(request)
    return redirect("home")









@login_required
def quizs(request):
    quiz = Test.objects.all().order_by("-id")
    return render(request, "tests.html", {"quizs": quiz})


@login_required
def quiz(request, tid, tnum):
    test_instance = Test.objects.get(tid=tid)
    question_count = test_instance.question_set.count()
    question = Question.objects.filter(test=test_instance)[tnum-1]
    if question_count == len(UserAnswer.objects.filter(test=test_instance, user=request.user)):return redirect('result', tid=tid)
    if len(UserAnswer.objects.filter(test=test_instance, user=request.user, question=question)) > 0:return redirect('quiz', tid=tid, tnum=tnum+1)
    answers = Answer.objects.filter(question=question)
    alpha = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')     
    content = {
        "tnum": tnum,
        "test_tid": tid,
        "questions_count": question_count,
        "question_id": question.id,
        "question": question,
        "answers": answers,
        "alpha": alpha,
    }
    return render(request, "quiz.html", content)

@login_required
def check_answer(request, tid, id):
    if request.method == "POST":
        test_instance = Test.objects.get(tid=tid)
        question_count = test_instance.question_set.count()
        if question_count == len(UserAnswer.objects.filter(test=test_instance, user=request.user)):return redirect('result', tid=tid)
        qst = Question.objects.get(id=id)
        answer = Answer.objects.get(id=request.POST.get("answer"))
        # correct_answer = Answer.objects.filter(question=qst).get(correct=True)
        UserAnswer.objects.create(
            user     = request.user,
            test     = test_instance,
            question = qst,
            answer   = answer,
        )        
        
        questions = Question.objects.filter(test=test_instance)
        index = list(questions).index(qst)+1
        if question_count == index:
            return redirect('result', tid=tid)

        return redirect('quiz', tid=tid, tnum=index+1)
    
    
    
@login_required
def result(request, tid):
    test_instance = Test.objects.get(tid=tid)
    question_count = test_instance.question_set.count()
    correct_answers = 0
    for ua in UserAnswer.objects.filter(user=request.user, test=test_instance):
        if ua.checkanswer(): correct_answers += 1
    percent = round(100 / question_count * correct_answers)
    content = {
        "all": question_count,
        "correct": correct_answers,
        "failed": question_count-correct_answers,
        "percent": percent,
    }
    return render(request, "celebration.html", content)