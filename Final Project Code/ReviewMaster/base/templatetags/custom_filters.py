from django import template

register = template.Library()

@register.filter(name="course_rating")
def course_rating(professor, course):
    return professor.rating_course(course)