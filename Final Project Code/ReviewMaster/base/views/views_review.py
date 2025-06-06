from base.models import Professor, Review, Course
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required(login_url='/login')
def review(request):
    professors = Professor.objects.all()
    context = {
        'professors': professors,
        'courses': Course.objects.all()
    }
    return render(request, 'base/review/review.html', context)


@login_required(login_url='/login')
def submit_review(request):
    
    if request.method == 'POST':
        
        user = request.user
        
        professor_id = request.POST.get("professor")
        professor = Professor.objects.get(id=professor_id)

        rating = request.POST.get("rating")
        if request.POST.get('course'):
            course = Course.objects.get(id=request.POST.get('course'))
        else:
            course = None

        review = request.POST.get("review")

        review = Review(professor=professor, student=user, rating=rating, review=review, course=course)
        review.save()
        messages.success(request, 'Review successfully submitted!')

    else:
        messages.error(request, 'An error has occurred, please try again!')
    return redirect('review')

@login_required(login_url='/login')
def reply_review(request):
    if request.method == 'POST':

        content = request.POST.get("reply")
        review_id = request.POST.get("review-id")
        review = Review.objects.get(id=review_id)
        review.reply = content
        review.save()
    return redirect(f'professor-reviews/{review.professor.id}')

@login_required(login_url='/login')
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

            return render(request, 'base/review/review.html', context)
    else:
        messages.error(request, 'This page does not exist!')
        return redirect('profile', request.user)

@login_required(login_url='/login')
def flag_review(request, pk):
    review = Review.objects.get(id = pk)
    if request.method == 'POST':
        review.flagged = not review.flagged
        review.save()
        if flagged:
            body = "Review Restored!"
        else:
            body = "Review Flagged!"
        messages.success(request, body)
        return redirect('professor-reviews', review.professor.id)
    professor = review.professor
    context = {
        'review': review,
        'professor': professor
    }
    return render(request, 'base/review/flag_review.html', context)

@login_required(login_url='/login')
def flagged(request,pk):
    professor = Professor.objects.get(id=pk)
    reviews = professor.review_set.filter(flagged=True)
    context = {
        'professor': professor,
        'reviews': reviews
    }
    return render(request, 'base/review/flagged.html', context)