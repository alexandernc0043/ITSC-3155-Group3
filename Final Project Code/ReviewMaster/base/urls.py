from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginuser, name='login'),
    path('register/', views.registeruser, name='register'),
    path('logout/', views.logoutuser, name='logout'),
    path('pick-courses/',views.pick_courses, name='courses'),
    path('add-course/<str:pk>',views.addCourse, name='add-course'),
    path('remove-course/<str:pk>',views.removeCourse, name='remove-course')

   # path('review/<str:pk>/', views.review, name='review')
]
