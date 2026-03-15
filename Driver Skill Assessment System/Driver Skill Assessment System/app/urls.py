from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('chapters/', views.chapters, name='chapters'),
    path('quiz/', views.quiz, name='quiz'),
    path('quiz/result/', views.quiz_result, name='quiz_result'),
    path('view-correct-answers/', views.view_correct_answers, name='view_correct_answers'),
        path('certificate/', views.certificate, name='certificate'),  

]
