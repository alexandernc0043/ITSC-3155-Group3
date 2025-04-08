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


@login_required
def edit_review(request, pk):
    user = request.user
    user_reviews = Review.objects.filter(student=user)

    if user_reviews.filter(pk=pk).exists():  
        if request.method == 'POST':
            old_review = Review.objects.get(id=pk)
            new_review = request.POST.get("review")
            new_rating = request.POST.get("rating")

            if new_rating is None or new_rating == old_review.rating:
                old_review.rating = old_review.rating
            else:
                old_review.rating = new_rating
            
            old_review.review = new_review
            old_review.save()
            messages.success(request, 'Review edited!')
            return redirect('profile', request.user)
        else:
            review = Review.objects.filter(id=pk).first()

            context = {
                'review': review
            }

            return render(request, 'base/review.html', context)
    else:
        messages.error(request, 'This page does not exist!')
        return redirect('profile', request.user)