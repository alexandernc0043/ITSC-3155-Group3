from django.urls import path
from .views.views_user import *
from .views.views_misc import *
from .views.views_courses import *
from .views.views_review import *
from .views.views_professor import *
from .views.views_profile import *
from .views.views_tutor import *
from .views.views_ai import *


urlpatterns = [
    path('', home, name='home'),
    path('login/', login_user, name='login'),
    path('register/', register_user, name='register'),
    path('logout/', logout_user, name='logout'),
    path('pick-courses/', pick_courses, name='courses'),
    path('add-course/<str:pk>', add_course, name='add-course'),
    path('add-tutor/<str:pk>', add_tutor, name='add-tutor'),
    path('review/', review, name='review'),
    path('submit-review/', submit_review, name='submit_review'),
    path('professor-list/', professor_list, name = "professor-list"),
    path('tutor-list/', tutor_list, name = "tutor-list"),
    path('professor-reviews/<int:pk>/', professor_reviews, name='professor-reviews'),
    path('remove-course/<str:pk>', remove_course, name='remove-course'),
    path('remove-tutor/<str:pk>', remove_tutor, name='remove-tutor'),
    path('remove-application/<str:pk>', remove_application, name='remove-application'),
    path('profile/<str:pk>', profile, name='profile'),
    path('profile/<str:pk>/edit-profile', edit_profile, name='edit-profile'),
    path('profile/edit-review/<int:pk>', edit_review, name= "edit_review" ),
    path('about/', about, name='about'),
    path('how/', how, name='how'),
    path('flag/<int:pk>', flag_review, name='flag'),
    path('flagged/<int:pk>', flagged, name='flagged'),
    path('tutor-applications/', tutor_applications, name="tutor_apps"),
    path('update-tutor/<int:course_pk>/<int:tutor_pk>/<str:action>/', update_tutor, name='update_tutor'),
    path('reply-review', reply_review, name="reply"),
     path('generate-summary/', generate_summary, name='generate_summary')
    
   # path('review/<str:pk>/', review, name='review')
]
