from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="home"),
    path('login/', signin, name="login"),
    path('logout/', signout, name="logout"),
    
    
    path('quizs/', quizs, name="quizs"),
    path('quiz/<str:tid>/<int:tnum>', quiz, name="quiz"),
    path('check_answer/<str:tid>/<int:id>', check_answer, name="checkanswer"),
    path('result/<str:tid>', result, name="result"),
]
