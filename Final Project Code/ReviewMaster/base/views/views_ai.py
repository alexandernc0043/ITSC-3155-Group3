
from base.models import Professor, Review
from django.shortcuts import get_object_or_404, render

from django.db.models import Q




from openai import OpenAI
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv() 

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))






def generate_summary(request):
    if request.method == 'POST':
        professor_id = request.POST.get('professor_id')
        professor = get_object_or_404(Professor, id=professor_id)
        reviews = Review.objects.filter(professor=professor, flagged=False) #dont account for flagged reviews

        review_text = "\n".join([review.review for review in reviews if len(review.review) < 1000]) # ignore reviews more than 1000 characters to prevent spam

        if not review_text:
            return render(request, 'base/review/summary.html', {
                'summary': "No reviews were short enough to generate a summary.",
                'professor': professor
            })

        try:
            
            response = client.chat.completions.create(
                model="gpt-4.1",  
                messages=[
                    #prompts sent to the AI
                    {"role": "system", "content": "You are a helpful assistant that summarizes professor reviews."},
                    {"role": "user", "content": f"Summarize in 100 words or less the following student reviews for Professor. If there are no reviews, just say not enough reviews.  {professor.name}:\n\n{review_text}"}
                ]
            )
            
           #text generated by AI
            summary = response.choices[0].message.content

        except Exception as e:
            summary = f"An error occurred while generating the summary: {e}"

        return render(request, 'base/review/summary.html', {'summary': summary, 'professor': professor, 'reviews' : reviews})