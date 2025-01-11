from django.shortcuts import render, redirect 
from django.urls import reverse

# Create your views here.
from .models import VocabularyWord, get_days_so_far
from .forms import AddVocab
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect


import random
import logging

logger = logging.getLogger(__name__)


@login_required
def vocab_list(request):
    word =  VocabularyWord.objects.filter( student=request.user).order_by('-created_at')
    
    context = {
        'words': word,
        'wordcount': word.count(),
        
	}
    
    return render(request, "vocab/vocablist.html", context)

@login_required
def review(request):
    allwords =  VocabularyWord.objects.filter( student=request.user).order_by('-created_at')

    current_day = get_days_so_far() 
    todaywords = VocabularyWord.objects.filter(next_rep_day__lte = current_day, student=request.user).order_by('-created_at')
    
    num_cards_for_today = len(todaywords)
    if num_cards_for_today == 0:
        all_cards = VocabularyWord.objects.filter(student=request.user).order_by('next_rep_day')

    
        if len(allwords) == 0:
                return render(request, 'vocab/review.html', { 'active_tab' : 'review', 'user_has_no_cards' : True })
        next_rep_day = VocabularyWord.objects.filter(student=request.user). order_by('next_rep_day')[0].next_rep_day
        days_until_next_rep = next_rep_day - get_days_so_far()
        
        return render(request, 'vocab/review.html', { 'active_tab' : 'review', 'days_until_next_rep' : days_until_next_rep })

    else:
        result_list = list(todaywords)
        random.shuffle(result_list)
        card = result_list[0]
    
    
    context = {
		'todaywords': todaywords,
        'allwords': allwords,
        'wordcount': allwords.count(),
        'card' : card,
        'active_tab' : 'review', 'num_cards_for_today' : num_cards_for_today,
	}
    
    return render(request, "vocab/review.html", context)

@login_required
def addvocab(request):
        
    if request.method == "POST":
        form = AddVocab(request.POST)
        
        if form.is_valid():
            post = form.save(commit=False)
            post.student = request.user
            post.save()

            return redirect('vocab:vocab_list')


    else:
        form = AddVocab()
    
    return render(request, "vocab/add.html", {'form': form})

@login_required
def grade(request):
    try:
        card_id = request.POST['cardId']
        new_grade = int(request.POST['grade'])
    except KeyError:
        return review(request)
    else:
        c = VocabularyWord.objects.get(pk=card_id, student = request.user)
        logger.debug("Before grading: " + c.__unicode__())    
        c.process_answer(new_grade)
        c.save()
        logger.debug("After grading: " + c.__unicode__())

        return HttpResponseRedirect(reverse('vocab:review'))

@login_required
def editvocab(request, word):
    
    wordedit = VocabularyWord.objects.filter(new_word=word).first() 
        
    if request.method == "POST":
        form = AddVocab(request.POST, instance=wordedit)
        
        if form.is_valid():
            form.save()

            return redirect('vocab:vocab_list')

    else:
        form = AddVocab()
    
    return render(request, "vocab/add.html", {'wordedit':wordedit, 'form':form  })