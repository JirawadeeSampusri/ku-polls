from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.login, name='login'),
    path('list/', views.index, name='index'),
    path('<int:pk>/', views.vote_for_poll, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
