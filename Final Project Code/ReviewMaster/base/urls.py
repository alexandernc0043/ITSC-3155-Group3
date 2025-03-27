from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('pick-courses/',views.pick_courses, name='courses'),
    path('add-course/<str:pk>', views.add_course, name='add-course'),
    path('review/', views.review, name='review'),
    path('submit-review/', views.submit_review, name='submit_review'),
    path('professor-list/', views.professor_list, name = "professor-list"),
    path('professor-reviews/<str:professor_name>/', views.professor_reviews, name='professor-reviews'),
    path('remove-course/<str:pk>', views.remove_course, name='remove-course')

   # path('review/<str:pk>/', views.review, name='review')
]
