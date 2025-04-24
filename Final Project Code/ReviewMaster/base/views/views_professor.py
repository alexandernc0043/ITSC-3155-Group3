from base.models import Professor, Review
from django.shortcuts import render

def professor_list(request):
    professors = Professor.objects.all()
    context = {
        'professors': professors,
        'reviews': Review.objects.filter()
    }

    return render(request, 'base/professor/professor_list.html', context)


def professor_reviews(request, pk):
    professor = Professor.objects.get(id=pk)
    reviews = Review.objects.filter(professor=professor, flagged=False)

    return render(request, 'base/professor/professor_reviews.html', {'professor': professor, 'reviews': reviews})