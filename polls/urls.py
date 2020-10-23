from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('',views.display_login, name='display_login'),
    path('accounts/createaccount', views.createaccount, name='createaccount'),
    path('accounts/login', views.login, name='login'),
    path('accounts/display/createaccount', views.display_createaccount, name='display_createaccount'),
    path('accounts/display/login', views.display_login, name='display_login'),    
    path('display/login/', views.login, name='login'), 
    path('list/', views.index, name='index'),
    path('<int:pk>/', views.vote_for_poll, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
