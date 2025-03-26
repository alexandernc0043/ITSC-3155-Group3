from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginuser, name='login'),
    path('register/', views.registeruser, name='register'),
    path('logout/', views.logoutuser, name='logout'),
    path('pick-courses/',views.pick_courses, name='courses'),
    path('add-course/<str:pk>',views.addCourse, name='add-course'),
    path('review/', views.review, name='review'),
    path('submit-review/', views.submit_review, name='submit_review'),
    path('professor-list/', views.professor_list, name = "professor-list"),
    path('professor-reviews/<str:professor_name>/', views.professor_reviews, name='professor-reviews'),
    

]
