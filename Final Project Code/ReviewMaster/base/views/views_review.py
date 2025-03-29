from base.models import Professor, Review
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def review(request):
    professors = Professor.objects.all()

    context = {
        'professors': professors
    }
    return render(request, 'base/review.html', context)


@login_required
def submit_review(request):
    if request.method == 'POST':
        user = request.user

        professor_id = request.POST.get("professor")
        professor = Professor.objects.get(id=professor_id)

        rating = request.POST.get("rating")

        review = request.POST.get("review")

        review = Review(professor=professor, student=user, rating=rating, review=review)
        review.save()
        messages.success(request, 'Review successfully submitted!')

    else:
        messages.error(request, 'An error has occurred, please try again!')
    return redirect('review')