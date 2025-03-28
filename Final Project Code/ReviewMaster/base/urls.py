from django.urls import path
from .views.views_user import *
from .views.views_misc import *
from .views.views_courses import *
from .views.views_review import *
from .views.views_professor import *
from .views.views_profile import *


urlpatterns = [
    path('', home, name='home'),
    path('login/', login_user, name='login'),
    path('register/', register_user, name='register'),
    path('logout/', logout_user, name='logout'),
    path('pick-courses/',pick_courses, name='courses'),
    path('add-course/<str:pk>', add_course, name='add-course'),
    path('review/', review, name='review'),
    path('submit-review/', submit_review, name='submit_review'),
    path('professor-list/', professor_list, name = "professor-list"),
    path('professor-reviews/<str:professor_name>/', professor_reviews, name='professor-reviews'),
    path('remove-course/<str:pk>', remove_course, name='remove-course'),
    path('profile/<str:pk>', profile, name='profile'),
    path('profile/<str:pk>/edit-profile', edit_profile, name='edit-profile')

   # path('review/<str:pk>/', review, name='review')
]
