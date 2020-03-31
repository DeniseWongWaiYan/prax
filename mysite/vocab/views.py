from django.shortcuts import render, redirect

# Create your views here.
from .models import VocabularyWord
from .forms import AddVocab

def vocab_list(request):
	words = VocabularyWord.objects.filter(student=request.user).order_by('-created_at')
    
    
	context = {
		'words': words,
        'wordcount': words.count()
	}

	return render(request, "vocab/vocablist.html", context)

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